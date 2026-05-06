```{=html}
<!-- SPDX-License-Identifier: Apache-2.0 -->
```
# 🚛💬 SDV Blueprint - CarMate

👉 **Getting Started:** If you want to begin setup and deployment,
follow this guide first:\
📘 [CarMate Getting Started Guide](./compute/GettingStarted.md)

------------------------------------------------------------------------

## 📌 Project Overview

### 🏷️ Project Name / Tagline

CarMate - An in-vehicle AI assistant for lonely truck drivers.

------------------------------------------------------------------------

### 🧭 Initial Project Background

This project is based on an existing SDV (Software-Defined Vehicle)
concept originally developed by **CarByte**.

The current implementation extends this foundation as part of the SDV
Lab Challenge, focusing on improving integration with modern automotive
simulation tools and reducing external cloud dependencies.

------------------------------------------------------------------------

## ⚙️ Key Modifications in This Version

This version introduces the following major architectural changes:

-   🔗 **Integration with digital.auto Playground (Eclipse AutoWrx
    ecosystem)**\
    The system now connects to the digital.auto Playground, enabling
    simulation-based SDV development and testing.

-   🤖 **Local LLM instead of OpenAI API**\
    The conversational AI system was migrated from a cloud-based OpenAI
    model to a locally hosted LLM.\
    This improves:

    -   🔒 Data privacy (no external API calls)\
    -   📡 Offline capability\
    -   💸 Lower dependency on external services\
    -   🧠 Better control over model behavior in embedded environments

-   🧩 **CarMate AI concept retained**\
    The in-vehicle AI assistant (CarMate) remains the core application
    layer of the system.

------------------------------------------------------------------------

## 💡 Core Idea

### 🚛 Problem Statement:

Truck drivers often experience isolation during long drives while also
facing safety risks from manual infotainment interaction.

------------------------------------------------------------------------

### 🤖 Solution Concept: CarMate

CarMate is a local AI-powered in-vehicle assistant designed to improve
driving comfort, safety, and interaction.

------------------------------------------------------------------------

#### 🧠 1. Local AI Conversational Companion

-   Runs on a **locally deployed LLM** instead of cloud APIs\
-   Provides natural, context-aware dialogue\
-   Operates without requiring internet connectivity\
-   Ensures improved privacy and system autonomy

------------------------------------------------------------------------

#### 🚗 2. Vehicle & Simulation Integration

-   Interfaces with vehicle data and simulation environments\
-   Integrated with **digital.auto Playground (AutoWrx)**\
-   Supports real-time interaction with simulated vehicle signals

------------------------------------------------------------------------

#### 🗣️ 3. Hands-Free Interaction

-   Fully voice-controlled interface\
-   Supports natural language commands such as:
    -   "Change the ambient color"\
    -   "What is my current speed?"

------------------------------------------------------------------------

## 🌟 Benefits of This Implementation

-   🔒 Increased privacy through local LLM execution\
-   🌐 Reduced dependency on external AI services\
-   🧪 Strong SDV simulation integration via digital.auto Playground\
-   🧩 Simplified and more maintainable system architecture\
-   🚦 Safe, hands-free in-vehicle interaction model

------------------------------------------------------------------------

## 🏗️ Technical View

### 🚘 1. Vehicle Data Layer

-   Handles vehicle and simulation signals\
-   Integrated via digital.auto Playground

------------------------------------------------------------------------

### 🧠 2. AI Layer (Local LLM)

-   Processes natural language input locally\
-   Generates responses without cloud dependency\
-   Acts as the core intelligence unit of CarMate

------------------------------------------------------------------------

### 🔗 3. Simulation Integration Layer

-   Bridges system with SDV simulation environment\
-   Enables testing and validation in digital.auto ecosystem

------------------------------------------------------------------------

### 🎤 4. User Interaction Layer

-   Voice-based interface for driver interaction\
-   Ensures safe, hands-free usage

------------------------------------------------------------------------

## 🎯 System Goals

-   🔒 Fully local AI processing (no cloud dependency)\
-   🚗 SDV-ready simulation integration\
-   🧩 Modular and extensible architecture\
-   🚦 Safe and intuitive driver interaction

------------------------------------------------------------------------

## 📜 License

Licensed under the Apache License 2.0.\
SPDX-License-Identifier: Apache-2.0

------------------------------------------------------------------------

## ©️ Copyright

Copyright (c) 2025 CarByte and contributors.