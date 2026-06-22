# CarMate + CARLA Setup Guide

This guide explains how to set up and run CarMate with the CARLA simulator using multiple connected systems.

The setup requires three components:

- A primary Linux machine that runs CarMate, Docker services, and Ollama
- A secondary Windows machine that runs the CARLA simulator
- An optional Azure IoT Dev Kit / MCU for hardware integration using ThreadX

The Linux and Windows machines should be connected using an Ethernet cable.  
The MCU, if used, communicates over Wi-Fi.

---

# Step 1 — Start Ollama

CarMate requires Ollama for AI responses. If you want to use a different LLM model instead of `phi3`, see [Guide to change the LLM Model](#guide-to-change-the-llm-model).

On the Linux machine, run:

```bash
ollama serve
ollama pull phi3
```

---

# Step 2 — Configure Ethernet Connection

Connect the Linux and Windows machines using an Ethernet cable.

## Windows Machine (CARLA)

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

## Linux Machine (CarMate)

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

# Step 3 — Start CARLA

On the Windows machine, download CARLA 0.9.14:

https://tiny.carla.org/carla-0-9-14-windows

Extract the folder and Launch the simulator:

```bash
CarlaUE4.exe
```

Wait until the simulation finishes loading.

---

# Step 4 — Start the CarMate Stack

On the Linux machine:

```bash
cd ~/compute
sudo docker compose up -d
```

---

# Step 5 — Open the CarMate UI

Open a browser on the Linux machine and go to:

```text
http://localhost:5000
```

---

# Optional MCU / Azure IoT Dev Kit Setup

This section is only required if you want hardware integration with CarMate.

Make sure:

- The Linux machine and MCU are connected to the same Wi-Fi network
- You know the Wi-Fi IP address of the Linux machine

Find the Linux Wi-Fi IP address using:

```bash
ip a
```

---

# Configure `network.rs`

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

# Build and Flash the Firmware

ThreadX Rust repository:

https://github.com/Eclipse-SDV-Hackathon-Chapter-Three/threadx-rust

Build command:

```bash
cd threadx-rust/threadx-app/cross/app

cargo run --release \
  --target thumbv7em-none-eabihf \
  --bin network
```

## Guide to change the LLM Model

The carmate_agents script supports multiple local and cloud-based AI providers. You can change your active AI backend or switch model variants directly inside the configuration section of the script.

### 1. Download the New Model. Setup/Pull the Model

For Local Ollama Backend: Pull your desired model variant to your local machine:
Bash

```bash
ollama pull phi3
# or alternative models like: ollama pull mistral
```

For Cloud Backends (OpenAI, Gemini, Grok, Groq):
Ensure you have a valid API Key from the respective provider platform before moving to the next step.

### 2. Update CarMate Configuration

Open the agent configuration file using your preferred text editor:
Bash

```bash
nano compute/carmate_agents/carmate_agents.py
```

Locate the HARDCODED AI CONFIGURATION section at the top of the file:

1. Change the Provider: Update AI_PROVIDER to your choice: "ollama", "openai", "gemini", "grok", or "groq".

2. Provide your API Key: If using a cloud model, paste your token inside the API_KEYS dictionary matching your chosen provider.

3. (Optional) Tweak Specific Model Variants: If you want to use a specific model tag (e.g., swapping gpt-4o-mini for gpt-4o), modify the string value inside MODEL_MAP.

```bash

# =====================================================
# HARDCODED AI CONFIGURATION (Change here)
# =====================================================
# Options: "ollama", "openai", "gemini", "grok", "groq"
AI_PROVIDER = "openai"

# Insert your API keys here directly if using cloud models
API_KEYS = {
    "openai": "sk-proj-YOUR_ACTUAL_OPENAI_KEY_HERE",
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

### 3. Rebuild and Restart the Stack

Because the updated code configuration file gets built directly into the Docker image filesystem context, you must build when bringing up the compose environment to apply the code changes:

```bash
cd ~/compute
sudo docker compose down
sudo docker compose up -d --build
```