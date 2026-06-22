"""Constants for the G-Service integration."""

DOMAIN = "g_service"
DEFAULT_NAME = "G-Service"
CONF_URL = "url"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_URL = "https://www.g-service.ru/"
SCAN_INTERVAL = 7200  # 2 hours (default)
DEFAULT_SCAN_INTERVAL = 7200  # 2 hours

# Sensor attributes
ATTR_ACCOUNT = "account"
ATTR_BALANCE = "balance"
ATTR_STATUS = "status"
ATTR_PLAN = "plan"
ATTR_REWARDS = "rewards"
ATTR_IP = "ip"
ATTR_SERVICES = "services"
ATTR_DAYS_LEFT = "days_remaining"

# Tariff price page
PLANS_URL = "https://www.g-service.ru/internet/"
DAYS_IN_MONTH = 30

# Access status keywords (Russian)
ACCESS_BLOCKED_KEYWORDS = ["заблок", "огранич", "отключ", "нет доступа"]
ACCESS_OPEN_KEYWORDS = ["открыт", "доступ", "актив", "работает"]
