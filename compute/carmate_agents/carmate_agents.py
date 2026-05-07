import asyncio
import zenoh
import threading
import time
import ollama

import common_uuri

from uprotocol.communication.inmemoryrpcserver import InMemoryRpcServer
from uprotocol.communication.requesthandler import RequestHandler
from uprotocol.communication.upayload import UPayload
from uprotocol.v1.uattributes_pb2 import UPayloadFormat
from uprotocol.v1.umessage_pb2 import UMessage
from uprotocol.v1.uri_pb2 import UUri

from up_transport_zenoh.uptransportzenoh import UPTransportZenoh


# =====================================================
# MAP
# =====================================================
RESOURCE_MAP = {
    1001: "speed",
    1002: "lat",
    1003: "lon",
    1004: "alt",
    1005: "wetness",
    2001: "temperature"
}

vehicle_data = {
    "speed": "34",
    "lat": "45",
    "lon": "555",
    "alt": "455",
    "wetness": "45",
    "temperature": "23"
}


# =====================================================
# EXTRACT ID
# =====================================================
def extract_resource_id(key_expr):
    return int(str(key_expr).split("/")[4])


# =====================================================
# TOOL
# =====================================================
def get_vehicle_data(type: str) -> str:
    print("\n---------------- TOOL CALLED ----------------")
    print("Request:", type)
    print("Current Vehicle Data:", vehicle_data)

    return str(vehicle_data.get(type, "type not supported"))


# =====================================================
# OLLAMA
# =====================================================
def run_ollama(prompt: str):
    system_prompt = f"""
You are a friendly in-car AI assistant in a Software-Defined Vehicle.

Your personality:
- Warm, friendly, slightly emotional 😊
- Natural conversational tone (like a co-driver)
- Encourages follow-up questions to keep conversation going
- Never robotic, never like a database
- Suitable for voice (TTS-friendly)

STRICT RULES:
- Use ONLY the vehicle data provided below
- Never guess or invent values
- Keep responses 2 to 3 short sentences
- Always try to naturally invite continuation (question or suggestion)
- Do NOT output JSON or technical formatting

CURRENT VEHICLE DATA:
- speed: {vehicle_data['speed']} km/h
- lat: {vehicle_data['lat']}
- lon: {vehicle_data['lon']}
- altitude: {vehicle_data['alt']} m
- wetness: {vehicle_data['wetness']}
- temperature: {vehicle_data['temperature']} °C

RESPONSE STYLE EXAMPLES:
- "We’re cruising at 34 km/h right now 😊. Everything feels smooth on the road. Want me to keep an eye on traffic conditions for you?"
- "It’s around 23°C inside the vehicle — pretty comfortable 👍. How are you feeling about the drive so far?"
- "I’m seeing a bit of moisture outside 🌧️. Roads might be slightly slippery — should I keep monitoring road conditions for you?"

Always end with a light question or invitation to continue the conversation.
"""

    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


# =====================================================
# AI ORCHESTRATOR
# =====================================================
def run_ai(prompt: str):
    print("\n🚀 AI REQUEST:", prompt)

    response = run_ollama(prompt)

    print("\n🤖 RAW MODEL RESPONSE:")
    print(response)

    for key in vehicle_data.keys():
        if key in response.lower():
            value = get_vehicle_data(key)
            final = f"The current {key} is {value}."

            print("\n🤖 FINAL RESPONSE:", final)
            return final

    print("\n🤖 FINAL RESPONSE:", response)
    return response


# =====================================================
# ZENOH CALLBACK (DATA STREAM ONLY)
# =====================================================
def callback(sample):
    key = str(sample.key_expr)

    try:
        value = bytes(sample.payload).decode().strip()
    except:
        value = str(sample.payload)

    try:
        resource_id = extract_resource_id(key)
        topic = RESOURCE_MAP.get(resource_id, "unknown")
    except:
        topic = "unknown"

    print("\n🔥 RECEIVED")
    print("Topic:", topic)
    print("Value:", value)

    if topic != "unknown":
        vehicle_data[topic] = value
        print("💾 UPDATED:", topic, "=", value)


# =====================================================
# RPC TRANSPORT SETUP
# =====================================================
METHOD_URI = common_uuri.create_method_uri()
print(f"[SERVER] Listening on: {METHOD_URI}")

source_rpc = UUri(authority_name="voice-command", ue_id=18)

transport_rpc = UPTransportZenoh.new(
    common_uuri.get_zenoh_config(),
    source_rpc
)


# =====================================================
# FIXED REQUEST HANDLER (NON-BLOCKING)
# =====================================================
class MyRequestHandler(RequestHandler):

    def handle_request(self, msg: UMessage) -> UPayload:
        text = msg.payload.decode("utf-8")
        print("\n📩 RPC REQUEST:", text)

        # ✅ run AI in separate thread (CRITICAL FIX)
        reply = self._run_ai_threadsafe(text)

        if not reply:
            reply = "ERROR: empty response"

        print("\n📤 SENDING REPLY:", reply)

        return UPayload(
            data=reply.encode("utf-8"),
            format=UPayloadFormat.UPAYLOAD_FORMAT_TEXT
        )

    def _run_ai_threadsafe(self, text: str):
        result = []

        def worker():
            try:
                result.append(run_ai(text))
            except Exception as e:
                result.append(f"AI ERROR: {str(e)}")

        t = threading.Thread(target=worker)
        t.start()
        t.join()   # waits safely without blocking event loop issues

        return result[0] if result else None


# =====================================================
# RPC SERVER
# =====================================================
async def register_rpc():
    print("[SERVER] Starting RPC server...")

    rpc_server = InMemoryRpcServer(transport_rpc)

    await rpc_server.register_request_handler(
        METHOD_URI,
        MyRequestHandler()
    )

    print("[SERVER] RPC handler registered")

    # Zenoh subscriber (ONLY ONE SESSION)
    config = zenoh.Config()
    session = zenoh.open(config)

    session.declare_subscriber(
        "up/publisher/**",
        callback
    )

    print("[SERVER] Listening...\n")

    while True:
        await asyncio.sleep(1)


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    asyncio.run(register_rpc())