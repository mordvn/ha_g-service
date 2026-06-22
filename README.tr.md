<div align="center">
  <h1>
    <img src="https://www.g-service.ru/local/templates/gs/dist/img/svg/logo.svg" width="28" alt="" style="vertical-align: -4px;">
    G-Service · Home Assistant
  </h1>
  <p>
    <b>"Igra-Service" sağlayıcısı için resmi olmayan Home Assistant entegrasyonu</b><br>
    <i>Kimlik doğrulaması gerekmez — sağlayıcı ağındaki IP üzerinden hesap verilerini ayrıştırma</i>
  </p>
  <p>
    🌐 <a href="README.md">Русский</a> · <a href="README.en.md">English</a> · <a href="README.zh.md">简体中文</a> · <b>Türkçe</b> · <a href="README.kz.md">Қазақша</a> · <a href="README.uz.md">Oʻzbekcha</a>
  </p>
  <p>
    <a href="https://github.com/mordvn/ha_g-service/releases"><img src="https://img.shields.io/github/v/release/mordvn/ha_g-service?color=blueviolet" alt="Son Sürüm"></a>
    <a href="https://github.com/mordvn/ha_g-service/releases"><img src="https://img.shields.io/github/release-date/mordvn/ha_g-service?color=blueviolet" alt="Yayın Tarihi"></a>
  </p>
  <p>
    <img src="media/demo.png" width="450" alt="Home Assistant'taki Sensörler">
  </p>
</div>

---

## 🌐 İçindekiler

- [✨ Özellikler](#-özellikler)
- [📦 Kurulum](#-kurulum)
- [🔧 Güncelleme Aralığı Yapılandırması](#-güncelleme-aralığı-yapılandırması)
- [📊 Sensörler](#-sensörler)
- [🧠 Akıllı Sensör «Kalan Günler»](#-akıllı-sensör-kalan-günler)
- [💡 Lovelace Örnekleri](#-lovelace-örnekleri)
- [⚙️ Nasıl Çalışır](#️-nasıl-çalışır)
- [📋 Gereksinimler](#-gereksinimler)
- [🐛 Sorun Bildir](#-sorun-bildir)

---

## ✨ Özellikler

- **7 sensör** — bakiye, abone numarası, tarife planı, erişim durumu, IP adresi, bonuslar, engellenmeye kalan gün sayısı
- **Kimlik doğrulaması gerekmez** — veriler, G-Service ağı içinde IP üzerinden erişilebilen sağlayıcının herkese açık HTML sayfasından alınır
- **Config Flow** — Home Assistant arayüzü üzerinden yapılandırma, YAML gerekmez
- **Yapılandırılabilir güncelleme aralığı** — 1 dakikadan 24 saate kadar (varsayılan: 2 saat)
- **Ek bağımlılık yok** — yalnızca Home Assistant'ın dahili `aiohttp` kütüphanesi kullanılır

---

## 📦 Kurulum

### Config Flow ile (önerilen)

```bash
# 1. Klasörü custom_components klasörüne kopyalayın
cp -r custom_components/g_service /config/custom_components/

# 2. Home Assistant'ı yeniden başlatın
#    Settings → System → Restart

# 3. Entegrasyonu ekleyin
#    Settings → Devices & Services → Add Integration
#    «G-Service (Игра-Сервис)» seçeneğini bulun → Ekle
```

Hepsi bu kadar! Sensörler otomatik olarak görünecektir. Anahtar, token veya giriş bilgisi gerekmez.

### HACS ile (manuel kurulum)

<details>
<summary>Talimatlar</summary>

1. HACS → **Integrations** bölümünü açın
2. `…` → **Custom repositories** seçeneğine tıklayın
3. `https://github.com/mordvn/ha_g-service` adresini **Integration** türüyle ekleyin
4. **Install** düğmesine tıklayın
5. HA'yı yeniden başlatın ve **Settings → Devices & Services** üzerinden ekleyin

</details>

---

## 🔧 Güncelleme Aralığı Yapılandırması

Kurulumdan sonra entegrasyon kartındaki **Configure** (⚙️) düğmesine tıklayın:

| Parametre | Değer |
|-----------|-------|
| **Varsayılan** | 7200 sn (2 saat) |
| **Minimum** | 60 sn (1 dakika) |
| **Maksimum** | 86400 sn (24 saat) |

---

## 📊 Sensörler

| Entity ID | Açıklama | Simge | Birim |
|-----------|----------|-------|-------|
| `sensor.g_service_balance` | **Bakiye** | `mdi:currency-rub` | ₽ |
| `sensor.g_service_days_remaining` | **Engellenmeye kalan gün** | `mdi:calendar-clock` | gün |
| `sensor.g_service_account` | **Abone numarası** | `mdi:account-card-details` | — |
| `sensor.g_service_plan` | **Tarife planı** (örn. Gigabit) | `mdi:speedometer` | — |
| `sensor.g_service_access` | **Erişim durumu** | `mdi:shield-check` | — |
| `sensor.g_service_ip` | **IP adresi** | `mdi:ip-network` | — |
| `sensor.g_service_bonuses` | **Bonuslar** | `mdi:gift` | — |

---

## 🧠 Akıllı Sensör «Kalan Günler»

Bu sensör, sağlayıcının web sitesindeki tarife fiyatına göre bir **tahmin hesaplar**.

### Nasıl Çalışır

1. Hesap sayfasından tarife adını alır (örneğin «Gigabit»)
2. `/internet/` sayfasında fiyatını bulur (örneğin 1270 ₽/ay)
3. Hesaplar: `kalan_gün = bakiye / (aylık_tarife_fiyatı / 30)`

```
Bakiye: 957 ₽
Tarife «Gigabit»: 1270 ₽/ay → 42.3 ₽/gün
→ 957 / 42.3 ≈ 22.6 gün
```

### Tarife Fiyatı Bulunamazsa

Planınız eskiyse veya herkese açık sayfada listelenmemişse, sensör otomatik olarak yedek moda geçer: bakiye değişim geçmişini analiz eder ve ortalama günlük düşüş oranını hesaplar.

### Olası Değerler

| Değer | Anlamı |
|-------|--------|
| `22.6` | Yaklaşık 22.6 gün sonra engelleme |
| `0` | Erişim zaten engellenmiş |
| `None` | Yeterli veri yok |

### Notlar

- Hesaba para yüklendiğinde, hesaplamayı bozmamak için bakiye geçmişi sıfırlanır
- Kurulumdan hemen sonra çalışır — geçmiş birikmesini beklemeniz gerekmez (tarife bulunabiliyorsa)

---

## 💡 Lovelace Örnekleri

### Basit Panel

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

### Bakiye Göstergesi

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

### Koşullu Kart

```yaml
type: conditional
conditions:
  - entity: sensor.g_service_access
    state_not: 'открыт, абон.'
card:
  type: markdown
  content: >
    ⚠️ **Uyarı!** İnternet erişiminiz kısıtlandı!
    Bakiye: {{ states('sensor.g_service_balance') }} ₽
    Lütfen G-Service hesabınıza para yükleyin.
```

---

## ⚙️ Nasıl Çalışır

Entegrasyon, sağlayıcının web sitesindeki iki sayfaya GET istekleri gönderir ve HTML'yi düzenli ifadeler (regex) ile ayrıştırır. Kimlik doğrulaması gerekmez — sağlayıcı, müşteri verilerini IP adresine göre otomatik olarak döndürür.

**Veri Kaynakları:**

| URL | Ne Ayrıştırılır |
|-----|----------------|
| `https://www.g-service.ru/` | Başlık (abone no, bakiye) ve açılır pencere (tarife, erişim, IP, bonuslar) |
| `https://www.g-service.ru/internet/` | Kalan gün hesaplaması için tarife fiyatları |

HTML ayrıştırma her derde deva değildir. Sağlayıcı sayfa yapısını değiştirirse entegrasyon çalışmayı durdurabilir.

### Mimari

```
┌─────────────────────┐     GET https://www.g-service.ru/
│  Home Assistant      │ ──────────────────────────────────►  G-Service
│  DataUpdateCoordinator│ ◄──────────────────────────────────  Sunucu
│  (2 saatte bir sorgular) │     HTML veri sayfası
├─────────────────────┤     GET https://www.g-service.ru/internet/
│  _parse_html()       │ ◄──────────────────────────────────  Tarifeler
│  ↓                   │
│  balance, account,   │
│  access, plan,       │
│  ip, bonuses         │
├─────────────────────┤
│  _parse_tariff_prices│     Tarife fiyatlarını ayrıştırma
│  ↓                   │     Plan adına göre fiyat eşleştirme
│  _compute_days_left()│     bakiye / (aylık_fiyat / 30)
│  ↓                   │     VEYA bakiye geçmişi (yedek)
│  days_remaining      │
└─────────────────────┘

```

---

## 📋 Gereksinimler

- **Home Assistant** 2023.8.0 veya daha yeni
- **G-Service ağına bağlı** — Home Assistant, sağlayıcının ağına bağlı olmalıdır (WiFi veya ethernet), böylece g-service.ru IP'nizi abone olarak tanır
- Ek kütüphane gerekmez — HA tüm gerekli bileşenleri içerir

---

## 🐛 Sorun Bildir

Hata buldunuz mu? Sağlayıcı siteyi güncelledi ve entegrasyon çalışmıyor mu?

→ [GitHub'da bir Issue oluşturun](https://github.com/mordvn/ha_g-service/issues)

Lütfen şunları ekleyin:

- HA sürümü
- Entegrasyon sürümü
- Günlük dosyasındaki hatalar (`home-assistant.log`)

---

## 🌍 Desteklenen Arayüz Dilleri

Entegrasyon, Home Assistant arayüz yerelleştirmesini destekler (sensör adları, ayarlar):

| Bayrak | Dil | Dosya |
|--------|-----|-------|
| 🇬🇧 | **İngilizce** | [`en.json`](custom_components/g_service/translations/en.json) |
| 🇷🇺 | **Rusça** | [`ru.json`](custom_components/g_service/translations/ru.json) |

Arayüz dili, Home Assistant sistem dilinize göre otomatik olarak seçilir.

---

<div align="center">

<sub>Resmi olmayan entegrasyon. G-Service (Igra-Service) ile ilişkili değildir.</sub>

</div>
