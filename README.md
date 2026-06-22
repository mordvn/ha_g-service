<div align="center">
  <h1>
    <img src="https://www.g-service.ru/local/templates/gs/dist/img/svg/logo.svg" width="28" alt="" style="vertical-align: -4px;">
    G-Service · Home Assistant
  </h1>
  <p>
    <b>Неофициальная интеграция провайдера «Игра-Сервис» для Home Assistant</b><br>
    <i>Парсинг данных лицевого счёта без авторизации — по IP внутри сети провайдера</i>
  </p>
  <p>
    🌐 <b>Русский</b> · <a href="README.en.md">English</a> · <a href="README.zh.md">简体中文</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.kz.md">Қазақша</a> · <a href="README.uz.md">Oʻzbekcha</a>
  </p>
  <p>
    <a href="https://github.com/mordvn/ha_g-service/releases"><img src="https://img.shields.io/github/v/release/mordvn/ha_g-service?color=blueviolet" alt="Latest Release"></a>
    <a href="https://github.com/mordvn/ha_g-service/releases"><img src="https://img.shields.io/github/release-date/mordvn/ha_g-service?color=blueviolet" alt="Release Date"></a>
     </p>
  <p>
    <img src="media/demo.png" width="450" alt="Сенсоры в Home Assistant">
  </p>
</div>

---

## 🌐 Содержание

- [✨ Возможности](#-возможности)
- [📦 Установка](#-установка)
- [🔧 Настройка интервала обновления](#-настройка-интервала-обновления)
- [📊 Сенсоры](#-сенсоры)
- [🧠 Адаптивный сенсор «Дней до блокировки»](#-адаптивный-сенсор-дней-до-блокировки)
- [💡 Примеры Lovelace](#-примеры-lovelace)
- [⚙️ Как это работает](#️-как-это-работает)
- [📋 Требования](#-требования)
- [🐛 Сообщить о проблеме](#-сообщить-о-проблеме)

---

## ✨ Возможности

- **Config Flow** — настройка через интерфейс Home Assistant, ни строчки YAML
- **7 сенсоров** — баланс, лицевой счёт, тариф, статус доступа, IP-адрес, бонусы, дней до блокировки
- **Без авторизации** — данные берутся из публичной HTML-страницы провайдера, доступной по IP внутри сети G-Service
- **Настраиваемый интервал обновления** — от 1 минуты до 24 часов (по умолчанию 2 часа)
- **Никаких зависимостей** — используется только `aiohttp`, который уже есть в Home Assistant

---

## 📦 Установка

### Через Config Flow (рекомендуется)

```bash
# 1. Скопируй папку в custom_components
cp -r custom_components/g_service /config/custom_components/

# 2. Перезапусти Home Assistant
#    Settings → System → Restart

# 3. Добавь интеграцию
#    Settings → Devices & Services → Add Integration
#    Найди «G-Service (Игра-Сервис)» → Добавить
```

Всё! Сенсоры появятся автоматически. Никаких ключей, токенов или логинов.

### Через HACS (ручное добавление)

<details>
<summary>Инструкция</summary>

1. Открой HACS → **Integrations**
2. Нажми `…` → **Custom repositories**
3. Добавь `https://github.com/mordvn/ha_g-service` с типом **Integration**
4. Нажми **Install**
5. Перезапусти HA и добавь через **Settings → Devices & Services**

</details>

---

## 🔧 Настройка интервала обновления

После установки нажми **Configure** (⚙️) на карточке интеграции:

| Параметр | Значение |
|----------|----------|
| **По умолчанию** | 7200 с (2 часа) |
| **Минимум** | 60 с (1 минута) |
| **Максимум** | 86400 с (24 часа) |

---

## 📊 Сенсоры

| Entity ID | Описание | Иконка | Ед. изм. |
|-----------|----------|--------|----------|
| `sensor.g_service_balance` | **Баланс** | `mdi:currency-rub` | ₽ |
| `sensor.g_service_days_remaining` | **Дней до блокировки** | `mdi:calendar-clock` | дн |
| `sensor.g_service_account` | **Лицевой счёт** | `mdi:account-card-details` | — |
| `sensor.g_service_plan` | **Тариф** (напр. Гигабит) | `mdi:speedometer` | — |
| `sensor.g_service_status` | **Статус доступа** | `mdi:shield-check` | — |
| `sensor.g_service_ip` | **IP-адрес** | `mdi:ip-network` | — |
| `sensor.g_service_bonuses` | **Бонусы** | `mdi:gift` | — |

---

## 🧠 Сенсор «Дней до блокировки»

Сенсор **вычисляет** прогноз на основе цены тарифа со страницы провайдера.

### Как работает

1. Берёт название тарифа из личного кабинета (например, «Гигабит»)
2. Находит его цену на странице `/internet/` (например, 1270 ₽/мес)
3. Считает: `дней_до_блокировки = баланс / (цена_тарифа_в_месяц / 30)`

```
Баланс: 957 ₽
Тариф «Гигабит»: 1270 ₽/мес → 42.3 ₽/день
→ 957 / 42.3 ≈ 22.6 дня
```

### Возможные значения

| Значение | Что означает |
|----------|--------------|
| `22.6` | Примерно 22.6 дня до блокировки |
| `0` | Доступ уже заблокирован |
| `None` | Недостаточно данных |

### Особенности

- Работает сразу после установки — не нужно ждать накопления истории (если тариф найден)

---

## 💡 Примеры Lovelace

### Простая панель

```yaml
type: entities
title: G-Service (Игра-Сервис)
entities:
  - entity: sensor.g_service_balance
  - entity: sensor.g_service_days_remaining
  - entity: sensor.g_service_status
  - entity: sensor.g_service_account
  - entity: sensor.g_service_plan
  - entity: sensor.g_service_ip
  - entity: sensor.g_service_bonuses
```

### Gauge для баланса

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

### Карточка с условным отображением

```yaml
type: conditional
conditions:
  - entity: sensor.g_service_status
    state_not: 'открыт, абон.'
card:
  type: markdown
  content: >
    ⚠️ **Внимание!** Доступ к интернету ограничен!
    Баланс: {{ states('sensor.g_service_balance') }} ₽
    Пополните счёт в личном кабинете G-Service.
```

---

## ⚙️ Как это работает

Интеграция делает GET-запросы к двум страницам сайта провайдера и парсит HTML с помощью регулярных выражений. Никакой авторизации — провайдер сам отдаёт данные абонента по его IP-адресу.

**Источники данных:**

| URL | Что парсим |
|-----|-----------|
| `https://www.g-service.ru/` | Хедер (ЛС, баланс) и модальное окно (тариф, доступ, IP, бонусы) |
| `https://www.g-service.ru/internet/` | Цены тарифов для расчёта дней до блокировки |

### Архитектура

```
┌─────────────────────┐     GET https://www.g-service.ru/
│  Home Assistant      │ ──────────────────────────────────►  G-Service
│  DataUpdateCoordinator│ ◄──────────────────────────────────  Сервер
│  (опрос каждые 2ч)   │     HTML-страница с данными
├─────────────────────┤     GET https://www.g-service.ru/internet/
│  _parse_html()       │ ◄──────────────────────────────────  Тарифы
│  ↓                   │
│  balance, account,   │
│  status, plan,       │
│  ip, bonuses         │
├─────────────────────┤
│  _parse_tariff_prices│     Парсинг цен тарифов
│  ↓                   │     Поиск цены по имени тарифа
│  _compute_days_left()│     баланс / (цена_месяц / 30)
│  ↓                   │     или история баланса (fallback)
│  days_remaining      │
└─────────────────────┘

```

---

## 📋 Требования

- **Home Assistant** 2023.8.0 или новее
- **Подключение к сети G-Service** — Home Assistant должен быть в сети провайдера (WiFi или ethernet), чтобы g-service.ru видел ваш IP как абонентский
- Никаких дополнительных библиотек — всё из коробки HA

---

## 🐛 Сообщить о проблеме

Нашёл баг? Провайдер обновил сайт и интеграция сломалась?

→ [Создай issue на GitHub](https://github.com/mordvn/ha_g-service/issues)

Пожалуйста, приложи:

- версию HA
- версию интеграции
- ошибки из лога

---

## 🌍 Поддерживаемые языки интерфейса

Интеграция поддерживает локализацию интерфейса Home Assistant (названия сенсоров, настройки):

| Флаг | Язык | Файл |
|------|------|------|
| 🇷🇺 | **Русский** | [`ru.json`](custom_components/g_service/translations/ru.json) |
| 🇬🇧 | **English** | [`strings.json`](custom_components/g_service/strings.json) (по умолчанию) |

Язык интерфейса выбирается автоматически на основе системного языка Home Assistant.

---

<div align="center">

<sub>Неофициальная интеграция. Не связана с G-Service (Игра-Сервис).</sub>

</div>
