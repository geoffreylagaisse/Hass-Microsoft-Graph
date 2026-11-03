"""Config flow for Microsoft Graph."""
import logging

from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.const import CONF_CLIENT_ID, CONF_CLIENT_SECRET
import voluptuous as vol

from .const import DEFAULT_SCOPES, DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN

_LOGGER = logging.getLogger(__name__)


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle Microsoft Graph OAuth2 authentication."""

    DOMAIN = DOMAIN

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    @property
    def extra_authorize_data(self) -> dict:
        """Extra data that needs to be appended to the authorize url."""
        return {
            "scope": " ".join(DEFAULT_SCOPES),
        }

    async def async_oauth_create_entry(self, data: dict):
        """Create an entry for the flow.

        Ok to override if you want to fetch extra info or even add another step.
        """
        data[CONF_CLIENT_ID] = self.hass.data[DOMAIN][CONF_CLIENT_ID]
        data[CONF_CLIENT_SECRET] = self.hass.data[DOMAIN][CONF_CLIENT_SECRET]

        return self.async_create_entry(title=self.flow_impl.name, data=data)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()

            self.hass.data[DOMAIN] = {
                CONF_CLIENT_ID: user_input[CONF_CLIENT_ID],
                CONF_CLIENT_SECRET: user_input[CONF_CLIENT_SECRET],
            }

            self.async_register_implementation(
                self.hass,
                config_entry_oauth2_flow.LocalOAuth2Implementation(
                    self.hass,
                    DOMAIN,
                    user_input[CONF_CLIENT_ID],
                    user_input[CONF_CLIENT_SECRET],
                    OAUTH2_AUTHORIZE,
                    OAUTH2_TOKEN,
                ),
            )
            user_input["implementation"] = DOMAIN

            flow = await self.async_step_pick_implementation(user_input)
            return flow

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_CLIENT_ID): str,
                    vol.Required(CONF_CLIENT_SECRET): str,
                }
            ),
            errors=errors,
        )
