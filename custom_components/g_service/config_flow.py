"""Config flow for G-Service integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, CONF_SCAN_INTERVAL


class GServiceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for G-Service."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step — no configuration needed, just create entry."""
        if user_input is not None:
            return self.async_create_entry(title="G-Service (Игра-Сервис)", data={})

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> GServiceOptionsFlowHandler:
        """Return the options flow handler."""
        return GServiceOptionsFlowHandler()


class GServiceOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle G-Service options — allows changing scan interval post-setup.

    ``config_entry`` is provided automatically by the framework.
    """

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=current_interval,
                ): vol.All(vol.Coerce(int), vol.Range(min=60, max=86400)),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )
