"""
Heos notification service.
"""
import logging

from homeassistant.components.notify import (BaseNotificationService, DOMAIN)
from homeassistant.const import (CONF_HOST, CONF_NAME)
from homeassistant.helpers import validate_config

REQUIREMENTS = ['https://github.com/andryd/heos/archive/v0.0.1.zip#heos==0.0.1',
                'gTTS']

_LOGGER = logging.getLogger(__name__)


def get_service(hass, config):
    """Return the notify service."""
    if not validate_config({DOMAIN: config}, {DOMAIN: [CONF_HOST, CONF_NAME]},
                           _LOGGER):
        return None

    host = config.get(CONF_HOST, None)

    if not host:
        _LOGGER.error('No host provided.')
        return None

    from heos import Heos
    from heos import HeosException

    client = Heos()

    try:
        if not host:
            host = client.discover()
        client.connect()
    except HeosException:
        _LOGGER.error('Connection failed.')
        return None
    except OSError:
        _LOGGER.error('Host unreachable.')
        return None

    return HeosNotificationService(client)


class HeosNotificationService(BaseNotificationService):
    """Implement the notification service for Heos service."""

    def __init__(self, client):
        """Initialize the service."""
        self._client = client

    # pylint: disable=unused-argument
    def send_message(self, message="", **kwargs):
        """Send a message to Heos."""
        from gtts import gTTS
        from heos import HeosException

        tts = gTTS(text=message, lang='en')
        tts.save("hello.mp3")

        try:
            # HTTP server
            #
            # self._client.play_url('http://{}:8123/)
            pass
        except HeosException:
            _LOGGER.error('Pairing failed.')
        except OSError:
            _LOGGER.error('Host unreachable.')
