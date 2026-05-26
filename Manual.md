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

If you want to use a different AI model (e.g., swapping `phi3` for `mistral`), follow these steps on your Linux machine:

### 1. Download the New Model
Pull your desired model using Ollama. For example, to use Mistral:
```bash
ollama pull mistral
```

### 2. Update CarMate Configuration
Open the agent configuration file:
```bash
compute/carmate_agents/carmate_agents.py
```
Navigate to Line 97 and update the model string to match your newly pulled model:
```bash
model = "mistral"
```

### 3. Restart the Stack
Apply the changes by restarting your Docker containers:
```bash
cd ~/compute
sudo docker compose down
sudo docker compose up -d
```
