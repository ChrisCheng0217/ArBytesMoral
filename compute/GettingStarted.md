# 🚗 CarMate + CARLA Setup Guide

This guide explains how to set up and run the **CarMate** system with a **CARLA simulator** running on a secondary machine.

---

## 🧩 System Overview

*   **💻 CARLA Machine (Secondary Laptop):** Runs CARLA (Windows).
*   **🖥️ CarMate Machine (Primary System):** Runs Docker + SDV stack (Linux).
*   **🔌 Ethernet:** Communication between both systems.
*   **📡 Wi-Fi (WLAN):** Used for MCU communication.
*   **🧠 Ollama (on host):** Required for AI responses.

---

## 🧠 Step 1 — Start Ollama (IMPORTANT FIRST STEP)

CarMate uses Ollama for AI responses. Make sure it is running on the **CarMate (Linux) machine**:

```bash
ollama serve
```

---

## ⚙️ Step 2 — Set Ethernet IP (CARLA Machine)

Set a static IP on the **CARLA laptop (Windows)**:
`192.168.43.249`

### 🪟 Windows Setup
1.  Open: **Control Panel** → **Network and Sharing Center** → **Change adapter settings**.
2.  Right-click **Ethernet** → **Properties**.
3.  Select: **Internet Protocol Version 4 (IPv4)**.
4.  **Set the following values:**
    *   **IP Address:** `192.168.43.249`
    *   **Subnet Mask:** `255.255.255.0`
    *   **Default Gateway:** (leave empty)

---  

## 🚗 Step 3— Run CARLA
On the **CARLA machine** (Windows) download Carla 0.9.14 here -> https://tiny.carla.org/carla-0-9-14-windows

And run the simulation - 
```powershell
CarlaUE4.exe
```
---

## 🐳 Step 4 — Start CarMate Stack

On the **CarMate machine** (Linux), navigate to the compute directory and launch the containers:
```bash
cd ~/compute
sudo docker compose up -d
```

---

## 🌐 Step 5 — Open CarMate UI

On the **CarMate machine**, open your web browser and access the interface:

[http://localhost:5000](http://localhost:5000)

---

👉 **MCU Setup:** Follow the MCU setup guide here:  
[MCU Setup Guide](./mcu_sw/GettingStarted.md)

