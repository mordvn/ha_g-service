"""Sensor platform for G-Service (Игра-Сервис) internet provider.

Parses public account info from the provider's website (visible via provider WiFi
without authentication).
"""

from __future__ import annotations

import asyncio
import logging
import re
from datetime import timedelta
from typing import Any

import aiohttp
import async_timeout

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    ATTR_ACCOUNT,
    ATTR_BALANCE,
    ATTR_DAYS_LEFT,
    ATTR_IP,
    ATTR_PLAN,
    ATTR_REWARDS,
    ATTR_SERVICES,
    ATTR_STATUS,
    CONF_SCAN_INTERVAL,
    DAYS_IN_MONTH,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_URL,
    DOMAIN,
    PLANS_URL,
    ACCESS_BLOCKED_KEYWORDS,
)

_LOGGER = logging.getLogger(__name__)


SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=ATTR_BALANCE,
        name="Баланс",
        native_unit_of_measurement="₽",
        icon="mdi:currency-rub",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_DAYS_LEFT,
        name="Дней до блокировки",
        native_unit_of_measurement="дн",
        icon="mdi:calendar-clock",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    SensorEntityDescription(
        key=ATTR_ACCOUNT,
        name="Лицевой счёт",
        icon="mdi:account-card-details",
    ),
    SensorEntityDescription(
        key=ATTR_PLAN,
        name="Тариф",
        icon="mdi:speedometer",
    ),
    SensorEntityDescription(
        key=ATTR_STATUS,
        name="Доступ",
        icon="mdi:shield-check",
    ),
    SensorEntityDescription(
        key=ATTR_IP,
        name="IP-адрес",
        icon="mdi:ip-network",
    ),
    SensorEntityDescription(
        key=ATTR_REWARDS,
        name="Бонусы",
        icon="mdi:gift",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up G-Service sensors from a config entry."""
    session = async_get_clientsession(hass)

    coordinator = GServiceCoordinator(hass, session, entry)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        GServiceSensor(coordinator, entry, description)
        for description in SENSOR_DESCRIPTIONS
    )


class GServiceCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to fetch G-Service data once for all sensors."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        entry: ConfigEntry,
    ) -> None:
        """Initialize coordinator."""
        scan_interval_seconds = entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )
        update_interval = timedelta(seconds=scan_interval_seconds)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self._session = session

        # Cached tariff prices: plan_name → monthly_price_rub
        self._tariff_prices: dict[str, int] = {}

    async def _fetch_page(self, url: str, label: str) -> str:
        """Fetch a page with a User-Agent header."""
        async with async_timeout.timeout(15):
            async with self._session.get(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    )
                },
            ) as response:
                if response.status != 200:
                    raise UpdateFailed(f"{label} returned status {response.status}")
                return await response.text()

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from G-Service main page and tariff pages."""
        # Fetch main account page
        try:
            html = await self._fetch_page(DEFAULT_URL, "G-Service main page")
        except (aiohttp.ClientError, TimeoutError, asyncio.TimeoutError) as err:
            raise UpdateFailed(f"Error fetching G-Service data: {err}") from err

        data = self._parse_html(html)
        if not data:
            raise UpdateFailed("No data found on G-Service page")

        # Fetch tariff prices page (best-effort, errors are non-fatal)
        try:
            tariffs_html = await self._fetch_page(PLANS_URL, "Tariffs page")
            self._tariff_prices = self._parse_tariff_prices(tariffs_html)
            _LOGGER.debug(
                "Parsed %d tariff prices: %s",
                len(self._tariff_prices),
                self._tariff_prices,
            )
        except Exception as err:
            _LOGGER.warning("Failed to fetch tariff prices from %s: %s", PLANS_URL, err)

        # --- Compute days remaining ---
        if ATTR_BALANCE in data:
            data[ATTR_DAYS_LEFT] = self._compute_days_remaining(
                data[ATTR_BALANCE], data
            )
        else:
            data[ATTR_DAYS_LEFT] = None

        return data

    def _compute_days_remaining(
        self, current_balance: float, data: dict[str, Any]
    ) -> float | None:
        """Compute estimated days until balance runs out using tariff price."""
        # If access is already blocked, no days remaining
        status = data.get(ATTR_STATUS, "")
        if status and any(kw in status.lower() for kw in ACCESS_BLOCKED_KEYWORDS):
            return 0.0

        # Tariff monthly price
        plan_name = data.get(ATTR_PLAN)
        if plan_name and plan_name in self._tariff_prices:
            monthly_price = self._tariff_prices[plan_name]
            daily_rate = monthly_price / DAYS_IN_MONTH
            if daily_rate > 0:
                remaining = current_balance / daily_rate
                _LOGGER.debug(
                    "Using tariff price: %s=%d ₽/month → %.2f ₽/day → %.1f days",
                    plan_name,
                    monthly_price,
                    daily_rate,
                    remaining,
                )
                return max(0.0, round(remaining, 1))

        # Tariff price not found → unknown
        return None

    @staticmethod
    def _parse_tariff_prices(html: str) -> dict[str, int]:
        """Parse tariff monthly prices from the /internet/ page.

        Returns a dict mapping plan names to monthly prices in rubles, e.g.:
            {"Гигабит": 1270, "Гигабит Премиум": 1650, ...}
        """
        prices: dict[str, int] = {}

        name_pattern = re.compile(
            r'<div class="rate-name[^"]*"[^>]*>.*?<span>([А-Яа-яA-Za-z\s+]+?)<'
            r"/span>\s*</div>",
            re.DOTALL,
        )
        price_pattern = re.compile(r"rate-price__value[^>]*>\s*<span>(\d+)</span>")

        names = name_pattern.findall(html)
        prices_raw = price_pattern.findall(html)

        if not names:
            _LOGGER.warning(
                "No tariff names found — tariff page structure may have changed"
            )
            return prices

        if len(names) != len(prices_raw):
            _LOGGER.warning(
                "Tariff count mismatch: %d names vs %d prices — page structure may have changed",
                len(names),
                len(prices_raw),
            )

        for name, price_str in zip(names, prices_raw):
            prices[name] = int(price_str)
            _LOGGER.debug("Parsed tariff: %s → %d ₽/month", name, prices[name])

        return prices

    @staticmethod
    def _parse_html(html: str) -> dict[str, Any]:
        """Parse the HTML page and extract provider data.

        Gracefully handles missing fields — only logs warnings instead of crashing.
        Missing fields simply won't appear in the returned dict.
        """
        data: dict[str, Any] = {}

        # --- Parse header: account and balance ---
        m = re.search(
            r'class="header__balance-text_lc"[^>]*>ЛС:\s*(\d+)',
            html,
        )
        if m:
            data[ATTR_ACCOUNT] = m.group(1)
        else:
            _LOGGER.info(
                "Header account number not found — page structure may have changed"
            )

        m = re.search(
            r'class="header__balance-text_balance">Баланс:</span>\s*<b>([\d\s,.]+)\s*р\.',
            html,
        )
        if m:
            raw = m.group(1).replace(" ", "").replace(",", ".")
            data[ATTR_BALANCE] = float(raw)
        else:
            _LOGGER.info("Header balance not found — page structure may have changed")

        # --- Parse modal: detailed account info ---
        modal_match = re.search(
            r"<!--'start_frame_cache_form-login-info-block'-->(.*?)<!--'end_frame_cache_form-login-info-block'-->",
            html,
            re.DOTALL,
        )
        if not modal_match:
            _LOGGER.warning(
                "Account info modal block not found — provider may have redesigned the page"
            )
            return data

        modal_html = modal_match.group(1)

        field_patterns = {
            ATTR_STATUS: r"Доступ:</span>\s*(.*?)</div>",
            ATTR_PLAN: r"Тариф:</span>\s*(.*?)</div>",
            ATTR_BALANCE: r"Баланс:</span>\s*([\d\s,.]+)\s*р\.\s*</div>",
            ATTR_REWARDS: r"Бонусы:</span>\s*([\d]+)\s*</div>",
            ATTR_IP: r"IP-адрес:</span>\s*([\d.]+)\s*</div>",
            ATTR_ACCOUNT: r"Лицевой счёт:</span>\s*(\d+)\s*</div>",
            ATTR_SERVICES: r"Услуги:</span>\s*(.*?)\s*</div>",
        }

        for key, pattern in field_patterns.items():
            m = re.search(pattern, modal_html)
            if not m:
                _LOGGER.info(
                    "Modal field '%s' not found — page structure may have changed",
                    key,
                )
                continue

            raw = m.group(1).strip()

            if key == ATTR_BALANCE:
                cleaned = raw.replace(" ", "").replace(",", ".")
                try:
                    data[key] = float(cleaned)
                except ValueError:
                    _LOGGER.warning("Failed to parse balance value: '%s'", raw)
            elif key == ATTR_REWARDS:
                try:
                    data[key] = int(raw)
                except ValueError:
                    _LOGGER.warning("Failed to parse bonuses value: '%s'", raw)
            else:
                data[key] = raw

        return data


class GServiceSensor(CoordinatorEntity[GServiceCoordinator], SensorEntity):
    """Sensor for a single G-Service data point."""

    def __init__(
        self,
        coordinator: GServiceCoordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "G-Service",
            "manufacturer": "Игра-Сервис",
            "model": "Личный кабинет",
        }

    @property
    def native_value(self) -> Any:
        """Return the sensor value from coordinator data."""
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def available(self) -> bool:
        """Return True if the sensor has a meaningful value.

        For days_remaining, None means we can't estimate yet.
        We still show it as available so the user sees it's pending.
        """
        return self.coordinator.last_update_success
