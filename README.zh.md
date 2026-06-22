<div align="center">
  <h1>
    <img src="https://www.g-service.ru/local/templates/gs/dist/img/svg/logo.svg" width="28" alt="" style="vertical-align: -4px;">
    G-Service · Home Assistant
  </h1>
  <p>
    <b>「Igra-Service」供应商的非官方 Home Assistant 集成</b><br>
    <i>无需认证即可解析账户数据 — 只需在供应商网络内通过 IP 访问</i>
  </p>
  <p>
    🌐 <a href="README.md">Русский</a> · <a href="README.en.md">English</a> · <b>简体中文</b> · <a href="README.tr.md">Türkçe</a> · <a href="README.kz.md">Қазақша</a> · <a href="README.uz.md">Oʻzbekcha</a>
  </p>
  <p>
    <a href="https://github.com/mordvn/ha-g-service/releases"><img src="https://img.shields.io/github/v/release/mordvn/ha-g-service?color=blueviolet" alt="最新版本"></a>
    <a href="https://github.com/mordvn/ha-g-service/releases"><img src="https://img.shields.io/github/release-date/mordvn/ha-g-service?color=blueviolet" alt="发布日期"></a>
  </p>
  <p>
    <img src="media/demo.png" width="450" alt="Home Assistant 中的传感器">
  </p>
</div>

---

## 🌐 目录

- [✨ 功能特点](#-功能特点)
- [📦 安装](#-安装)
- [🔧 更新间隔设置](#-更新间隔设置)
- [📊 传感器](#-传感器)
- [🧠 智能传感器「剩余天数」](#-智能传感器剩余天数)
- [💡 Lovelace 示例](#-lovelace-示例)
- [⚙️ 工作原理](#️-工作原理)
- [📋 系统要求](#-系统要求)
- [🐛 报告问题](#-报告问题)

---

## ✨ 功能特点

- **7 个传感器** — 余额、账户编号、资费方案、访问状态、IP 地址、积分、封禁剩余天数
- **无需认证** — 数据从供应商的公开 HTML 页面获取，只要在 G-Service 网络内即可通过 IP 访问
- **Config Flow** — 通过 Home Assistant 界面配置，无需编写 YAML
- **可配置的更新间隔** — 从 1 分钟到 24 小时（默认 2 小时）
- **无额外依赖** — 仅使用 Home Assistant 内置的 `aiohttp`

---

## 📦 安装

### 通过 Config Flow（推荐）

```bash
# 1. 将文件夹复制到 custom_components
cp -r custom_components/g_service /config/custom_components/

# 2. 重启 Home Assistant
#    Settings → System → Restart

# 3. 添加集成
#    Settings → Devices & Services → Add Integration
#    找到 «G-Service (Игра-Сервис)» → 添加
```

这样就完成了！传感器将自动出现。无需密钥、令牌或登录信息。

### 通过 HACS（手动安装）

<details>
<summary>操作说明</summary>

1. 打开 HACS → **Integrations**
2. 点击 `…` → **Custom repositories**
3. 添加 `https://github.com/mordvn/ha-g-service`，类型选择 **Integration**
4. 点击 **Install**
5. 重启 HA，然后通过 **Settings → Devices & Services** 添加

</details>

---

## 🔧 更新间隔设置

安装后，点击集成卡片上的 **Configure**（⚙️）：

| 参数 | 值 |
|------|------|
| **默认** | 7200 秒（2 小时） |
| **最小值** | 60 秒（1 分钟） |
| **最大值** | 86400 秒（24 小时） |

---

## 📊 传感器

| Entity ID | 描述 | 图标 | 单位 |
|-----------|------|------|------|
| `sensor.g_service_balance` | **余额** | `mdi:currency-rub` | ₽ |
| `sensor.g_service_days_remaining` | **封禁剩余天数** | `mdi:calendar-clock` | 天 |
| `sensor.g_service_account` | **账户编号** | `mdi:account-card-details` | — |
| `sensor.g_service_plan` | **资费方案**（如 Gigabit） | `mdi:speedometer` | — |
| `sensor.g_service_access` | **访问状态** | `mdi:shield-check` | — |
| `sensor.g_service_ip` | **IP 地址** | `mdi:ip-network` | — |
| `sensor.g_service_bonuses` | **积分/奖励** | `mdi:gift` | — |

---

## 🧠 智能传感器「剩余天数」

该传感器根据供应商网站上的资费价格**计算**预测值。

### 工作原理

1. 从账户页面获取资费名称（例如「Gigabit」）
2. 在 `/internet/` 页面找到其价格（例如 1270 ₽/月）
3. 计算：`剩余天数 = 余额 / (月费 / 30)`

```
余额：957 ₽
资费「Gigabit」：1270 ₽/月 → 42.3 ₽/天
→ 957 / 42.3 ≈ 22.6 天
```

### 如果找不到资费价格

如果您的方案是旧版或未在公开页面中列出，传感器会自动切换到备用模式：分析余额变化历史并计算平均每日消耗速率。

### 可能的值

| 值 | 含义 |
|----|------|
| `22.6` | 大约 22.6 天后封禁 |
| `0` | 访问已被封禁 |
| `None` | 数据不足 |

### 注意事项

- 充值后，余额历史将被重置，以避免影响计算
- 安装后即可立即使用 — 无需等待积累历史数据（如果资费方案能找到）

---

## 💡 Lovelace 示例

### 简单面板

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

### 余额仪表盘

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

### 条件卡

```yaml
type: conditional
conditions:
  - entity: sensor.g_service_access
    state_not: 'открыт, абон.'
card:
  type: markdown
  content: >
    ⚠️ **警告！** 您的网络访问受到限制！
    余额：{{ states('sensor.g_service_balance') }} ₽
    请登录 G-Service 账户充值。
```

---

## ⚙️ 工作原理

该集成向供应商网站的两个页面发送 GET 请求，并使用正则表达式解析 HTML。无需认证 — 供应商会根据用户的 IP 地址自动返回对应的客户数据。

**数据来源：**

| URL | 解析内容 |
|-----|----------|
| `https://www.g-service.ru/` | 页面头部（账户、余额）和弹窗（资费、访问状态、IP、积分） |
| `https://www.g-service.ru/internet/` | 资费价格，用于计算剩余天数 |

HTML 解析并非万能的。如果供应商更改页面结构，该集成将无法正常工作。

### 架构

```
┌─────────────────────┐     GET https://www.g-service.ru/
│  Home Assistant      │ ──────────────────────────────────►  G-Service
│  DataUpdateCoordinator│ ◄──────────────────────────────────  服务器
│  (每 2 小时轮询)      │     HTML 数据页面
├─────────────────────┤     GET https://www.g-service.ru/internet/
│  _parse_html()       │ ◄──────────────────────────────────  资费列表
│  ↓                   │
│  balance, account,   │
│  access, plan,       │
│  ip, bonuses         │
├─────────────────────┤
│  _parse_tariff_prices│     解析资费价格
│  ↓                   │     根据方案名称匹配价格
│  _compute_days_left()│     余额 / (月费 / 30)
│  ↓                   │     或余额历史（备用方案）
│  days_remaining      │
└─────────────────────┘

```

---

## 📋 系统要求

- **Home Assistant** 2023.8.0 或更新版本
- **连接到 G-Service 网络** — Home Assistant 必须连接到供应商的网络（WiFi 或以太网），以便 g-service.ru 将您的 IP 识别为订阅用户
- 无需额外库 — HA 内置所有必需组件

---

## 🐛 报告问题

发现错误？供应商更新了网站导致集成无法使用？

→ [在 GitHub 上创建 Issue](https://github.com/mordvn/ha-g-service/issues)

请附上以下信息：

- HA 版本
- 集成版本
- 日志中的错误信息（`home-assistant.log`）

---

## 🌍 支持的用户界面语言

集成支持 Home Assistant 界面本地化（传感器名称、设置）：

| 旗帜 | 语言 | 文件 |
|------|------|------|
| 🇬🇧 | **英语** | [`en.json`](custom_components/g_service/translations/en.json) |
| 🇷🇺 | **俄语** | [`ru.json`](custom_components/g_service/translations/ru.json) |

界面语言将根据您的 Home Assistant 系统语言自动选择。

---

<div align="center">

<sub>非官方集成。与 G-Service (Igra-Service) 无任何关联。</sub>

</div>
