<div align="center">
  <h1>
    <img src="https://www.g-service.ru/local/templates/gs/dist/img/svg/logo.svg" width="28" alt="" style="vertical-align: -4px;">
    G-Service · Home Assistant
  </h1>
  <p>
    <b>Unofficial integration of the "Igra-Service" provider for Home Assistant</b><br>
    <i>Parse account data without authentication — by IP inside the provider's network</i>
  </p>
  <p>
    🌐 <a href="README.md">Русский</a> · <b>English</b> · <a href="README.zh.md">简体中文</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.kz.md">Қазақша</a> · <a href="README.uz.md">Oʻzbekcha</a>
  </p>
  <p>
    <a href="https://github.com/mordvn/ha_g-service/releases"><img src="https://img.shields.io/github/v/release/mordvn/ha_g-service?color=blueviolet" alt="Latest Release"></a>
    <a href="https://github.com/mordvn/ha_g-service/releases"><img src="https://img.shields.io/github/release-date/mordvn/ha_g-service?color=blueviolet" alt="Release Date"></a>
  </p>
  <p>
    <img src="media/demo.png" width="450" alt="Sensors in Home Assistant">
  </p>
</div>

---

## 🌐 Table of Contents

- [✨ Features](#-features)
- [📦 Installation](#-installation)
- [🔧 Update Interval Configuration](#-update-interval-configuration)
- [📊 Sensors](#-sensors)
- [🧠 "Days Remaining" Smart Sensor](#-days-remaining-smart-sensor)
- [💡 Lovelace Examples](#-lovelace-examples)
- [⚙️ How It Works](#️-how-it-works)
- [📋 Requirements](#-requirements)
- [🐛 Report a Problem](#-report-a-problem)

---

## ✨ Features

- **7 sensors** — balance, account number, tariff plan, access status, IP address, bonuses, days until block
- **No authentication** — data is taken from the provider's public HTML page, accessible by IP inside the G-Service network
- **Config Flow** — setup through the Home Assistant interface, no YAML required
- **Configurable update interval** — from 1 minute to 24 hours (default 2 hours)
- **No extra dependencies** — uses only `aiohttp`, which is already included in Home Assistant

---

## 📦 Installation

### Via Config Flow (recommended)

```bash
# 1. Copy the folder to custom_components
cp -r custom_components/g_service /config/custom_components/

# 2. Restart Home Assistant
#    Settings → System → Restart

# 3. Add the integration
#    Settings → Devices & Services → Add Integration
#    Find «G-Service (Игра-Сервис)» → Add
```

That's it! Sensors will appear automatically. No keys, tokens, or logins required.

### Via HACS (manual installation)

<details>
<summary>Instructions</summary>

1. Open HACS → **Integrations**
2. Click `…` → **Custom repositories**
3. Add `https://github.com/mordvn/ha_g-service` as type **Integration**
4. Click **Install**
5. Restart HA and add via **Settings → Devices & Services**

</details>

---

## 🔧 Update Interval Configuration

After installation, click **Configure** (⚙️) on the integration card:

| Parameter | Value |
|-----------|-------|
| **Default** | 7200 s (2 hours) |
| **Minimum** | 60 s (1 minute) |
| **Maximum** | 86400 s (24 hours) |

---

## 📊 Sensors

| Entity ID | Description | Icon | Unit |
|-----------|-------------|------|------|
| `sensor.g_service_balance` | **Balance** | `mdi:currency-rub` | ₽ |
| `sensor.g_service_days_remaining` | **Days until block** | `mdi:calendar-clock` | days |
| `sensor.g_service_account` | **Account number** | `mdi:account-card-details` | — |
| `sensor.g_service_plan` | **Tariff plan** (e.g. Gigabit) | `mdi:speedometer` | — |
| `sensor.g_service_access` | **Access status** | `mdi:shield-check` | — |
| `sensor.g_service_ip` | **IP address** | `mdi:ip-network` | — |
| `sensor.g_service_bonuses` | **Bonuses** | `mdi:gift` | — |

---

## 🧠 "Days Remaining" Smart Sensor

This sensor **calculates** a forecast based on the tariff price from the provider's website.

### How It Works

1. Gets the tariff name from the account page (e.g., "Gigabit")
2. Finds its price on the `/internet/` page (e.g., 1270 ₽/month)
3. Calculates: `days_remaining = balance / (tariff_price_per_month / 30)`

```
Balance: 957 ₽
Tariff "Gigabit": 1270 ₽/month → 42.3 ₽/day
→ 957 / 42.3 ≈ 22.6 days
```

### If the Tariff Price Is Not Found

If your plan is legacy or not listed on the public page, the sensor automatically switches to fallback mode: it analyzes the balance change history and calculates the average daily decrement rate.

### Possible Values

| Value | Meaning |
|-------|---------|
| `22.6` | Approximately 22.6 days until block |
| `0` | Access is already blocked |
| `None` | Not enough data |

### Notes

- When the account is topped up, the balance history is reset to avoid skewing the calculation
- Works immediately after installation — no need to wait for history to accumulate (if the tariff is found)

---

## 💡 Lovelace Examples

### Simple Panel

```yaml
type: entities
title: G-Service (Игра-Сервис)
entities:
  - entity: sensor.g_service_balance
  - entity: sensor.g_service_days_remaining
  - entity: sensor.g_service_access
  - entity: sensor.g_service_account
  - entity: sensor.g_service_plan
  - entity: sensor.g_service_ip
  - entity: sensor.g_service_bonuses
```

### Balance Gauge

```yaml
type: gauge
entity: sensor.g_service_balance
unit: ₽
min: 0
max: 500
severity:
  green: 200
  yellow: 100
  red: 0
```

### Conditional Card

```yaml
type: conditional
conditions:
  - entity: sensor.g_service_access
    state_not: 'открыт, абон.'
card:
  type: markdown
  content: >
    ⚠️ **Warning!** Your internet access is restricted!
    Balance: {{ states('sensor.g_service_balance') }} ₽
    Please top up in your G-Service account.
```

---

## ⚙️ How It Works

The integration makes GET requests to two pages of the provider's website and parses the HTML using regular expressions. No authentication — the provider itself returns customer data based on their IP address.

**Data Sources:**

| URL | What We Parse |
|-----|---------------|
| `https://www.g-service.ru/` | Header (account, balance) and modal window (tariff, access, IP, bonuses) |
| `https://www.g-service.ru/internet/` | Tariff prices for days-remaining calculation |

HTML parsing is not a silver bullet. If the provider changes the page structure, the integration will break.

### Architecture

```
┌─────────────────────┐     GET https://www.g-service.ru/
│  Home Assistant      │ ──────────────────────────────────►  G-Service
│  DataUpdateCoordinator│ ◄──────────────────────────────────  Server
│  (polls every 2h)    │     HTML page with data
├─────────────────────┤     GET https://www.g-service.ru/internet/
│  _parse_html()       │ ◄──────────────────────────────────  Tariffs
│  ↓                   │
│  balance, account,   │
│  access, plan,       │
│  ip, bonuses         │
├─────────────────────┤
│  _parse_tariff_prices│     Tariff price parsing
│  ↓                   │     Match price by plan name
│  _compute_days_left()│     balance / (monthly_price / 30)
│  ↓                   │     OR balance history (fallback)
│  days_remaining      │
└─────────────────────┘

```

---

## 📋 Requirements

- **Home Assistant** 2023.8.0 or newer
- **Connected to the G-Service network** — Home Assistant must be on the provider's network (WiFi or ethernet) so that g-service.ru sees your IP as a subscriber
- No additional libraries — everything is included in HA out of the box

---

## 🐛 Report a Problem

Found a bug? Did the provider update the site and break the integration?

→ [Create an issue on GitHub](https://github.com/mordvn/ha_g-service/issues)

Please include:

- HA version
- Integration version
- Errors from the log (`home-assistant.log`)

---

## 🌍 Supported UI Languages

The integration supports Home Assistant UI localization (sensor names, settings):

| Flag | Language | File |
|------|----------|------|
| 🇬🇧 | **English** | [`en.json`](custom_components/g_service/translations/en.json) |
| 🇷🇺 | **Russian** | [`ru.json`](custom_components/g_service/translations/ru.json) |

The UI language is selected automatically based on your Home Assistant system language.

---

<div align="center">

<sub>Unofficial integration. Not affiliated with G-Service (Igra-Service).</sub>

</div>
