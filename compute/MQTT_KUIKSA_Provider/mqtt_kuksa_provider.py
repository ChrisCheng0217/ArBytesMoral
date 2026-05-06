import asyncio
import queue
import paho.mqtt.client as mqtt
from kuksa_client.grpc import VSSClient, Datapoint

# ---------------- CONFIG ----------------
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

MQTT_TOPICS_CARLA = [
    "carla/vehicle/speed",
    "carla/vehicle/lat",
    "carla/vehicle/lon",
    "carla/vehicle/alt",
    "carla/vehicle/wetness",
    "mcu/temperature"
]

MQTT_TOPIC_COLOR = "compute/color"

KUKSA_HOST = "localhost"
KUKSA_PORT = 55555

MQTT_TO_KUKSA = {
    "carla/vehicle/speed": "Vehicle.Speed",
    "carla/vehicle/lat": "Vehicle.CurrentLocation.Latitude",
    "carla/vehicle/lon": "Vehicle.CurrentLocation.Longitude",
    "carla/vehicle/alt": "Vehicle.CurrentLocation.Altitude",
    "carla/vehicle/wetness": "Vehicle.Exterior.Humidity",
    "mcu/temperature": "Vehicle.Cabin.HVAC.AmbientAirTemperature"
}

SIGNAL_COLOR = "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Color"

# THREAD SAFE queue
mqtt_queue = queue.Queue()

# ---------------- MQTT ----------------
def on_connect(client, userdata, flags, rc):
    print(f"MQTT connected: {rc}")
    for t in MQTT_TOPICS_CARLA:
        client.subscribe(t)

def on_message(client, userdata, msg):
    mqtt_queue.put((msg.topic, msg.payload))

# ---------------- MQTT → KUKSA ----------------
def kuksa_writer_blocking():
    """Runs in thread via asyncio.to_thread"""
    with VSSClient(KUKSA_HOST, KUKSA_PORT) as vss:
        print("KUKSA writer started")

        while True:
            topic, payload = mqtt_queue.get()

            try:
                value = float(payload.decode().strip())

                vss_path = MQTT_TO_KUKSA.get(topic)
                if vss_path:
                    vss.set_current_values({
                        vss_path: Datapoint(value)
                    })
                    print(f"[KUKSA WRITE] {vss_path} = {value}")

            except Exception as e:
                print(f"Error: {e}")

# ---------------- KUKSA → MQTT ----------------
async def color_listener(mqtt_client):
    with VSSClient(KUKSA_HOST, KUKSA_PORT) as vss:
        print("Color listener started")

        for updates in vss.subscribe_current_values([SIGNAL_COLOR]):
            try:
                val = updates[SIGNAL_COLOR].value or 0
                mqtt_client.publish(MQTT_TOPIC_COLOR, str(val))
                print(f"[COLOR] {val}")
            except Exception as e:
                print(f"Color error: {e}")

# ---------------- MAIN ----------------
async def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()

    await asyncio.gather(
        asyncio.to_thread(kuksa_writer_blocking),
        color_listener(mqtt_client)
    )

if __name__ == "__main__":
    asyncio.run(main())
