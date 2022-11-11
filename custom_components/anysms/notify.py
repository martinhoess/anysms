"""AnySMS platform for notify component."""
from __future__ import annotations

from http import HTTPStatus
import logging
from typing import Any

import requests
import voluptuous as vol

from homeassistant.components.notify import PLATFORM_SCHEMA, BaseNotificationService
from homeassistant.const import (
    CONF_CLIENT_ID,
    CONF_API_KEY,
    CONF_CODE,
    CONF_RECIPIENT,
    CONF_SENDER,
    CONTENT_TYPE_TEXT_PLAIN,
)
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

BASE_API_URL = "https://www.any-sms.biz/gateway/send_sms.php"
DEFAULT_SENDER = "hass"
DEFAULT_GATEWAY = 20
TIMEOUT = 5

ERROR_1 = "Wrong username or password"
ERROR_2 = "Wrong IP"
ERROR_3 = "No sufficient credit MAIN account"
ERROR_4 = "No sufficient credit SUB account"
ERROR_5 = "SMS could not be accepted / sent"
ERROR_6 = "Gateway to this network not available"
ERROR_9 = "SPAM block (Same text to the same number within 3 minutes)"
ERROR_18 = "Missing price information in the SMS (for advertising premium numbers)"

HEADERS = {"Content-Type": CONTENT_TYPE_TEXT_PLAIN}

PLATFORM_SCHEMA = vol.Schema(
    vol.All(
        PLATFORM_SCHEMA.extend(
            {
                vol.Required(CONF_CLIENT_ID): cv.positive_int,
                vol.Required(CONF_API_KEY): cv.string,
                vol.Optional(CONF_CODE, default=DEFAULT_GATEWAY): vol.In([20, 28, 29]),
                vol.Required(CONF_RECIPIENT): cv.string,
                vol.Required(CONF_SENDER, default=DEFAULT_SENDER): cv.string
            }
        )
    )
)


def get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> AnySMSNotificationService | None:
    """Get the AnySMS notification service."""
    if not _authenticate(config):
        _LOGGER.error("You are not authorized to access AnySMS")
        return None
    return AnySMSNotificationService(config)


class AnySMSNotificationService(BaseNotificationService):
    """Implementation of a notification service for the AnySMS service."""

    def __init__(self, config: ConfigType) -> None:
        """Initialize the service."""
        self.customerid: int = config[CONF_CLIENT_ID]
        self.api_key: str = config[CONF_API_KEY]
        self.gateway: int = config[CONF_CODE]
        self.sender: str = config[CONF_SENDER]
        self.recipient: str = config[CONF_RECIPIENT]


    def send_message(self, message: str = "", **kwargs: Any) -> None:
        """Send a message to a user."""
        params = {'id': self.customerid, 'pass': self.api_key, 'gateway': self.gateway, 'absender': self.sender, 'nummer': self.recipient}

        utf = not message.isascii()

        if utf: 
            params['long'] = 1 if len(message) > 160 else 0
        else:
            params['long'] = 1 if len(message) > 70 else 0

        params['utf'] = 1 if utf else 0
        params['text'] = message

        resp = requests.get(
            BASE_API_URL,
            params=params,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        if resp.status_code == HTTPStatus.OK and "err:0" in resp.text:
            return

        # ToDo
        # _LOGGER.error(
        #     "Error %s : %s (Code %s)", resp.status_code, '', ''
        # )


def _authenticate(config: ConfigType) -> bool:
    """Authenticate with AnySMS."""
    params = {'id': config[CONF_CLIENT_ID], 'pass': config[CONF_API_KEY], 'test': 1}

    resp = requests.get(
        BASE_API_URL,
        headers=HEADERS,
        params=params,
        timeout=TIMEOUT,
    )
    return resp.status_code == HTTPStatus.OK and "err:0" in resp.text
