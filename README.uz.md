<div align="center">
  <h1>
    <img src="https://www.g-service.ru/local/templates/gs/dist/img/svg/logo.svg" width="28" alt="" style="vertical-align: -4px;">
    G-Service · Home Assistant
  </h1>
  <p>
    <b>"Igra-Service" provayderi uchun norasmiy Home Assistant integratsiyasi</b><br>
    <i>Avtorizatsiyasiz shaxsiy hisob maʼlumotlarini olish — provayder tarmogʻidagi IP orqali</i>
  </p>
  <p>
    🌐 <a href="README.md">Русский</a> · <a href="README.en.md">English</a> · <a href="README.zh.md">简体中文</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.kz.md">Қазақша</a> · <b>Oʻzbekcha</b>
  </p>
  <p>
    <a href="https://github.com/mordvn/ha_g-service/releases"><img src="https://img.shields.io/github/v/release/mordvn/ha_g-service?color=blueviolet" alt="Oxirgi versiya"></a>
    <a href="https://github.com/mordvn/ha_g-service/releases"><img src="https://img.shields.io/github/release-date/mordvn/ha_g-service?color=blueviolet" alt="Chiqarilgan sana"></a>
  </p>
  <p>
    <img src="media/demo.png" width="450" alt="Home Assistantʼdagi sensorlar">
  </p>
</div>

---

## 🌐 Mundarija

- [✨ Xususiyatlar](#-xususiyatlar)
- [📦 Oʻrnatish](#-oʻrnatish)
- [🔧 Yangilanish oraligʻini sozlash](#-yangilanish-oraligʻini-sozlash)
- [📊 Sensorlar](#-sensorlar)
- [🧠 «Bloklashgacha qolgan kunlar» aqlli sensori](#-bloklashgacha-qolgan-kunlar-aqlli-sensori)
- [💡 Lovelace misollari](#-lovelace-misollari)
- [⚙️ Qanday ishlaydi](#️-qanday-ishlaydi)
- [📋 Talablar](#-talablar)
- [🐛 Muammo haqida xabar berish](#-muammo-haqida-xabar-berish)

---

## ✨ Xususiyatlar

- **7 ta sensor** — balans, shaxsiy hisob raqami, tarif, ulanish holati, IP-manzil, bonuslar, bloklashgacha qolgan kunlar
- **Avtorizatsiya talab qilinmaydi** — maʼlumotlar provayderning umumiy HTML sahifasidan olinadi, G-Service tarmogʻida IP orqali mavjud
- **Config Flow** — Home Assistant interfeysi orqali sozlash, YAML kerak emas
- **Sozlanishi mumkin boʻlgan yangilanish oraligʻi** — 1 daqiqadan 24 soatgacha (standart: 2 soat)
- **Qoʻshimcha kutubxonalar kerak emas** — faqat Home Assistantʼga kiritilgan `aiohttp` ishlatiladi

---

## 📦 Oʻrnatish

### Config Flow orqali (tavsiya etiladi)

```bash
# 1. Papkani custom_components ichiga nusxalang
cp -r custom_components/g_service /config/custom_components/

# 2. Home Assistantʼni qayta ishga tushiring
#    Settings → System → Restart

# 3. Integratsiyani qoʻshing
#    Settings → Devices & Services → Add Integration
#    «G-Service (Игра-Сервис)» ni toping → Qoʻshish
```

Tamom! Sensorlar avtomatik ravishda paydo boʻladi. Kalitlar, tokenlar yoki loginlar kerak emas.

### HACS orqali (qoʻlda oʻrnatish)

<details>
<summary>Yoʻriqnoma</summary>

1. HACS → **Integrations** boʻlimini oching
2. `…` → **Custom repositories** tugmasini bosing
3. `https://github.com/mordvn/ha_g-service` manzilini **Integration** turi bilan qoʻshing
4. **Install** tugmasini bosing
5. HAʼni qayta ishga tushirib, **Settings → Devices & Services** orqali qoʻshing

</details>

---

## 🔧 Yangilanish oraligʻini sozlash

Oʻrnatgandan soʻng, integratsiya kartasidagi **Configure** (⚙️) tugmasini bosing:

| Parametr | Qiymat |
|----------|--------|
| **Standart** | 7200 s (2 soat) |
| **Minimal** | 60 s (1 daqiqa) |
| **Maksimal** | 86400 s (24 soat) |

---

## 📊 Sensorlar

| Entity ID | Tavsifi | Belgi | Oʻlchov birligi |
|-----------|---------|-------|-----------------|
| `sensor.g_service_balance` | **Balans** | `mdi:currency-rub` | ₽ |
| `sensor.g_service_days_remaining` | **Bloklashgacha qolgan kunlar** | `mdi:calendar-clock` | kun |
| `sensor.g_service_account` | **Shaxsiy hisob raqami** | `mdi:account-card-details` | — |
| `sensor.g_service_plan` | **Tarif** (masalan, Gigabit) | `mdi:speedometer` | — |
| `sensor.g_service_access` | **Ulanish holati** | `mdi:shield-check` | — |
| `sensor.g_service_ip` | **IP-manzil** | `mdi:ip-network` | — |
| `sensor.g_service_bonuses` | **Bonuslar** | `mdi:gift` | — |

---

## 🧠 «Bloklashgacha qolgan kunlar» aqlli sensori

Ushbu sensor provayder saytidagi tarif narxi asosida **bashoratni hisoblab chiqadi**.

### Qanday ishlaydi

1. Shaxsiy hisob sahifasidan tarif nomini oladi (masalan, «Gigabit»)
2. `/internet/` sahifasida uning narxini topadi (masalan, 1270 ₽/oy)
3. Hisoblaydi: `bloklashgacha_kun = balans / (oylik_tarif_narxi / 30)`

```
Balans: 957 ₽
Tarif «Gigabit»: 1270 ₽/oy → 42.3 ₽/kun
→ 957 / 42.3 ≈ 22.6 kun
```

### Tarif narxi topilmasa

Agar tarifingiz eskirgan boʻlsa yoki umumiy roʻyxatda boʻlmasa, sensor avtomatik ravishda zaxira rejimiga oʻtadi: balans oʻzgarish tarixini tahlil qiladi va oʻrtacha kunlik sarf tezligini hisoblaydi.

### Mumkin boʻlgan qiymatlar

| Qiymat | Maʼnosi |
|--------|---------|
| `22.6` | Taxminan 22.6 kundan keyin bloklash |
| `0` | Ulanish allaqachon bloklangan |
| `None` | Maʼlumotlar yetarli emas |

### Xususiyatlari

- Hisob toʻldirilganda, hisob-kitobni buzmaslik uchun balans tarixi tozalanadi
- Oʻrnatgandan soʻng darhol ishlaydi — tarix toʻplanishini kutish shart emas (agar tarif topilsa)

---

## 💡 Lovelace misollari

### Oddiy panel

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

### Balans koʻrsatkichi

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

### Shartli karta

```yaml
type: conditional
conditions:
  - entity: sensor.g_service_access
    state_not: 'открыт, абон.'
card:
  type: markdown
  content: >
    ⚠️ **Diqqat!** Internetga ulanish cheklangan!
    Balans: {{ states('sensor.g_service_balance') }} ₽
    Iltimos, G-Service shaxsiy kabinetida hisobingizni toʻldiring.
```

---

## ⚙️ Qanday ishlaydi

Integratsiya provayder saytining ikki sahifasiga GET soʻrovlarini yuboradi va HTML-ni muntazam ifodalar yordamida tahlil qiladi. Avtorizatsiya talab qilinmaydi — provayder abonent maʼlumotlarini IP-manzil boʻyicha avtomatik ravishda qaytaradi.

**Maʼlumot manbalari:**

| URL | Nima tahlil qilinadi |
|-----|---------------------|
| `https://www.g-service.ru/` | Sarlavha (shaxsiy hisob, balans) va modal oyna (tarif, ulanish, IP, bonuslar) |
| `https://www.g-service.ru/internet/` | Bloklashgacha qolgan kunlarni hisoblash uchun tarif narxlari |

HTML tahlili — kumush oʻq emas. Agar provayder sahifa tuzilishini oʻzgartirsa, integratsiya ishlamay qolishi mumkin.

### Arxitektura

```
┌─────────────────────┐     GET https://www.g-service.ru/
│  Home Assistant      │ ──────────────────────────────────►  G-Service
│  DataUpdateCoordinator│ ◄──────────────────────────────────  Server
│  (har 2 soatda)      │     HTML maʼlumot sahifasi
├─────────────────────┤     GET https://www.g-service.ru/internet/
│  _parse_html()       │ ◄──────────────────────────────────  Tariflar
│  ↓                   │
│  balance, account,   │
│  access, plan,       │
│  ip, bonuses         │
├─────────────────────┤
│  _parse_tariff_prices│     Tarif narxlarini tahlil qilish
│  ↓                   │     Tarif nomi boʻyicha moslashtirish
│  _compute_days_left()│     balans / (oylik_narx / 30)
│  ↓                   │     YOKI balans tarixi (zaxira)
│  days_remaining      │
└─────────────────────┘

```

---

## 📋 Talablar

- **Home Assistant** 2023.8.0 yoki undan yangi
- **G-Service tarmogʻiga ulangan** — Home Assistant provayder tarmogʻida boʻlishi kerak (WiFi yoki ethernet), shunda g-service.ru IPʼingizni abonent sifatida koʻradi
- Qoʻshimcha kutubxonalar kerak emas — HA barcha kerakli komponentlarni oʻz ichiga oladi

---

## 🐛 Muammo haqida xabar berish

Xato topdingizmi? Provayder saytni yangilab, integratsiya ishlamay qoldimi?

→ [GitHubʼda Issue oching](https://github.com/mordvn/ha_g-service/issues)

Iltimos, quyidagilarni ilova qiling:

- HA versiyasi
- Integratsiya versiyasi
- Jurnaldagi xatolar (`home-assistant.log`)

---

## 🌍 Qoʻllab-quvvatlanadigan interfeys tillari

Integratsiya Home Assistant interfeysining lokalizatsiyasini qoʻllab-quvvatlaydi (sensor nomlari, sozlamalar):

| Bayroq | Til | Fayl |
|--------|-----|------|
| 🇬🇧 | **Ingliz tili** | [`en.json`](custom_components/g_service/translations/en.json) |
| 🇷🇺 | **Rus tili** | [`ru.json`](custom_components/g_service/translations/ru.json) |

Interfeys tili Home Assistant tizim tiliga qarab avtomatik ravishda tanlanadi.

---

<div align="center">

<sub>Norasmiy integratsiya. G-Service (Igra-Service) bilan aloqador emas.</sub>

</div>
