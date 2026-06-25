# CarMate + CARLA Setup Guide

This guide explains how to set up and run CarMate with the CARLA simulator using multiple connected systems.

The setup requires three components:

- A primary Linux machine that runs CarMate and Docker services, plus either local Ollama or access to a public LLM provider
- A secondary Windows machine that runs the CARLA simulator
- (Optional) An Azure IoT Dev Kit / MCU for hardware integration using ThreadX

The Linux and Windows machines should be connected using an Ethernet cable.  
The MCU, if used, communicates over Wi-Fi.

---

## Step 1: Choose the LLM Backend

CarMate needs one AI backend for responses. Choose either the local Ollama backend or a public LLM provider.

### Option A: Local Ollama Model

Use this option if you want to run the LLM locally on the Linux machine.

Start Ollama and pull the model configured in CarMate:

```bash
ollama serve
ollama pull phi3
# or another local model, for example:
ollama pull mistral
```

In `compute/carmate_agents/carmate_agents.py`, keep the provider set to Ollama and set the local model name:

```python
AI_PROVIDER = "ollama"

MODEL_MAP = {
    "ollama": "phi3",
    # keep the other provider entries unchanged
}
```

### Option B: Public LLM Models

Use this option if you want CarMate to call a public LLM provider instead of running Ollama locally. CarMate currently supports OpenAI, Gemini, Grok, and Groq.

Get a valid API key from the provider platform, then open the agent configuration file:

```bash
nano compute/carmate_agents/carmate_agents.py
```

Locate the `HARDCODED AI CONFIGURATION` section at the top of the file:

1. Set `AI_PROVIDER` to `"openai"`, `"gemini"`, `"grok"`, or `"groq"`.
2. Put your API key into the matching entry in `API_KEYS`.
3. Optionally change the provider model string in `MODEL_MAP`.

```python
# Options: "ollama", "openai", "gemini", "grok", "groq"
AI_PROVIDER = "openai"

API_KEYS = {
    "openai": "YOUR_OPENAI_API_KEY",
    "gemini": "YOUR_GEMINI_API_KEY",
    "grok": "YOUR_XAI_API_KEY",
    "groq": "YOUR_GROQ_API_KEY",
}

MODEL_MAP = {
    "ollama": "phi3",
    "openai": "gpt-4o-mini",
    "gemini": "gemini-1.5-flash",
    "grok": "grok-beta",
    "groq": "llama-3.3-70b-versatile",
}
```

The Docker image includes this configuration file, so Step 4 uses `--build` to apply any backend or model changes.

---

## Step 2: Configure Ethernet Connection

Connect the Linux and Windows machines using an Ethernet cable.

### Windows Machine (CARLA)

Configure the Ethernet adapter with the following static IP settings:

```text
IP Address: 192.168.43.249
Subnet Mask: 255.255.255.0
Gateway: Leave empty
```

To configure this:

1. Open Control Panel
2. Go to Network and Sharing Center
3. Click “Change adapter settings”
4. Right-click the Ethernet adapter → Properties
5. Select “Internet Protocol Version 4 (TCP/IPv4)”
6. Click Properties
7. Enter the IP configuration above

### Linux Machine (CarMate UI)

First identify the Ethernet interface:

```bash
ip a
```

The interface name is usually something like:

```text
eth0
enp3s0
ens33
```

Assign a static IP address:

```bash
sudo ip addr add 192.168.43.245/24 dev eth0
sudo ip link set eth0 up
```

Verify the configuration:

```bash
ip a
```
Verify the connectiong with ping from the linux laptop:

```bash
ping 192.168.43.241
```

---

## Step 3: Start CARLA

### If you dont want to use the carla then skip this part

On the Windows machine, download CARLA 0.9.16:

https://github.com/carla-simulator/carla

Extract the folder and Launch the simulator:

```bash
CarlaUE4.exe
```

Wait until the simulation finishes loading.

---

## Step 4: Start the CarMate Stack

By default, the container is configured to spin up the **Mock Server** automatically. If you want to use the **Real CARLA Server** as your permanent default, On you linux machine you need to modify the Dockerfile directly before building the image.

Open `/compute/carla_provider/Dockerfile` and locate the final line:

```dockerfile
# Default: Runs in MOCK mode
CMD ["python", "carla_mqtt_bridge.py", "--nocarla"]
```

and then run this command, If you want to use the real carla server then skip the above part and directly run this command :

```bash
cd ~/compute
sudo docker compose up -d --build
```

---

## Step 5: Open the CarMate UI

Open a browser on the Linux machine and go to:

```text
http://localhost:5000
```

---

## (Optional) Step 6: Azure IoT Dev Kit (MCU Node) Setup

This section is only required if you want hardware integration with CarMate.

Make sure:

- The Linux machine and MCU are connected to the same Wi-Fi network
- You know the Wi-Fi IP address of the Linux machine

Find the Linux Wi-Fi IP address using:

```bash
ip a
```

---

### Configure `network.rs`

Open:

```text
threadx-app/cross/app/src/bin/network.rs
```

Update the broker IP at Line number 391:

```rust
let broker_ip: core::net::Ipv4Addr =
    core::net::Ipv4Addr::new(192, 168, 43, 241);
```

Update the Wi-Fi credentials on the above line:

```rust
let ssid: &'static str = "YOUR_SSID";
let password = "YOUR_PASSWORD";
```

---

### Build and Flash the Firmware

ThreadX Rust repository:

https://github.com/Eclipse-SDV-Hackathon-Chapter-Three/threadx-rust

Build command:

```bash
cd threadx-rust/threadx-app/cross/app

cargo run --release \
  --target thumbv7em-none-eabihf \
  --bin network
```

