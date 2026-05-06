# 📡 MCU Setup Guide (ThreadX)

This guide ensures your Microcontroller Unit (MCU) is correctly configured to communicate with the CarMate stack over your local network.

---

## 📶 Step 1 — Connect to Wi-Fi
Before configuring the code, ensure your **CarMate (Linux) machine** is connected to the same Wi-Fi network that the MCU will use.

1. Connect your Linux laptop to the target Wi-Fi.
2. Open a terminal and find your laptop's local IP address:
   ```bash
   ip a
   ```
3. Locate your wireless interface (e.g., wlan0) and note the inet address (e.g., 192.168.1.15).

---

## 📄 Step 2 — Configure network.rs

You must manually point the MCU to your laptop's IP address and provide the network credentials.

**File Path:** `threadx-app/cross/app/src/bin/network.rs`

### 🔧 Update Server IP (Line 392)
Navigate to **line 392** and replace the existing IP with your Linux machine's IP address:
```rust
// line 392
let broker_ip: core::net::Ipv4Addr = core::net::Ipv4Addr::new(192, 168, 43, 241) // <--- Insert your 'ip a' result here
```
**🔑 Update Network Credentials**

In the same file, locate the Wi-Fi configuration constants and update them to match your router:  
Rust
```rust
// line 388
let ssid: &'static str = "YOUR SSID";
let password = "PASSWORD";
```
---

## 📄 Step 3 -  Building and Deployment

Follow the prerequistes here - https://github.com/Eclipse-SDV-Hackathon-Chapter-Three/threadx-rust

This project requires:

- Rust with `no_std` embedded toolchain
- ThreadX RTOS integration
- STM32 HAL drivers
- Custom board support package for MxAz3166



The application uses `#![no_main]` and `#![no_std]` attributes for bare-metal embedded execution with ThreadX providing the runtime environment.

To build and run this project, navigate to the directory `threadx-rust/threadx-app/cross/app` and run `cargo run --release --target thumbv7em-none-eabihf --bin network`