# ⚡ WattShift — Smart Energy Tariff & Solar Dispatch Engine

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Package Manager](https://img.shields.io/badge/managed%20by-uv-DE5FE9?logo=astral&logoColor=white)](https://github.com/astral-sh/uv)
[![Framework](https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Resilient, event-driven optimization engine for dynamic energy tariffs (Polish Transmission System Operator - PSE) correlated with solar irradiation forecasts (Open-Meteo).**

---

## 🎯 The Problem

Dynamic energy tariffs fluctuate significantly on a 15-minute basis. During peak renewable generation, grid electricity prices approach zero (or go negative), while morning and evening peaks introduce extreme costs.

Homeowners and light industrial sites (heat pumps, home battery storage, EV chargers) face key operational challenges:
1. **Lack of Real-Time Ingestion:** Electricity market operators publish data daily, but downstream systems lack event-driven integrations.
2. **Disconnected Solar Production:** Charging a battery from the grid right before strong solar irradiance wastes renewable capacity and capital.
3. **Vendor Lock-in:** Hardware inverters are closed ecosystems lacking open webhook/REST dispatch APIs.

---

## 💡 The Solution

**WattShift** bridges the gap between public grid telemetry and distributed energy automation:

* **15-Minute Market Ingestion:** Async ingestion of Polish Grid Operator (**PSE**) dynamic RCE rates (96 intervals/day).
* **Hyperlocal Solar Forecasting:** Pulls hourly Direct Normal Irradiance (DNI) and temperature metrics from **Open-Meteo**.
* **Arbitrage & Dispatch Engine:** Computes optimal consumption windows (e.g., EV charging, heat pump buffering) and identifies high-cost peak periods.
* **Modern Developer Experience:** Built entirely around typed, async Python 3.12+, `uv`, and structured Pydantic data schemas.

---

## 🏗️ Architecture Overview

┌────────────────────────┐
                  │  PSE Market API (OData)│ (15-min dynamic RCE)
                  └───────────┬────────────┘
                              │
                              ▼
┌──────────────────────┐      ┌─────────────────────────┐
│ Open-Meteo Solar API │ ───> │  Ingestion & Validation │ (Async httpx + Pydantic v2)
└──────────────────────┘      └───────────┬─────────────┘
│
▼
┌─────────────────────────┐
│    Optimization Engine  │ (Polars / Window Rolling)
└───────────┬─────────────┘
│
┌─────────────────────┴─────────────────────┐
▼                                           ▼
┌───────────────────────────┐               ┌───────────────────────────┐
│     REST / Webhook API    │               │  Event Notification Queue │
│      (FastAPI Engine)     │               │   (AWS SQS / EventBridge) │
└───────────────────────────┘               └───────────────────────────┘


---

## 🛠️ Tech Stack

* **Language:** Python 3.12+ (Typed, Asynchronous)
* **Package Management & Tooling:** [uv](https://github.com/astral-sh/uv) (Rust-backed package runner and resolver)
* **API & Data Models:** FastAPI, Pydantic v2
* **HTTP Client:** `httpx` (Async I/O)
* **Target Cloud Deployment:** AWS (Lambda / ECS Fargate, SQS, Terraform IaC)

---

## 🚀 Quickstart

### Prerequisites

Ensure you have [uv](https://github.com/astral-sh/uv) installed:

```bash
# macOS / Linux
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
Installation & Run
Clone the repository:

Bash
git clone [https://github.com/](https://github.com/)pkotynia/wattshift.git
cd wattshift
Install project in editable mode:

Bash
uv pip install -e .
Fetch latest PSE 15-minute prices:

Bash
uv run python -m wattshift.pse_client
Fetch solar irradiation forecast:

Bash
uv run python -m wattshift.weather_client
🗺️ Roadmap
[x] PSE 15-minute dynamic price ingestion (OData API)

[x] Open-Meteo solar irradiance & ambient temperature client

[ ] Optimization core: Sliding-window cheapest hour calculator

[ ] Docker containerization & local integration tests

[ ] Infrastructure as Code: AWS deployment recipe via Terraform

[ ] Home Assistant / MQTT integration webhook dispatcher

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.