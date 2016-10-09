"""
Denon Heos notification service.
"""
import logging

import voluptuous

import homeassistant.helpers.config_validation as cv
from homeassistant.components.notify import (
        PLATFORM_SCHEMA, BaseNotificationService)
from homeassistant.const import CONF_HOST
# from homeassistant.helpers import validate_config

REQUIREMENTS = ['https://github.com/andryd/heos/archive/v0.1.2.zip#heos==0.1.2',
                'gTTS',
                'lxml',
                'httplib2']

CONF_VOLUME = 'volume'
CONF_LANG = 'lang'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    voluptuous.Optional(CONF_HOST): cv.string,
    voluptuous.Optional(CONF_LANG, default='en'): cv.string,
    voluptuous.Optional(CONF_VOLUME): cv.integer,
})

_LOGGER = logging.getLogger(__name__)

def get_service(hass, config):
    """Return the notify service."""

    host = config.get(CONF_HOST)
    lang = config.get(CONF_LANG)
    volume = config.get(CONF_VOLUME)

    from heos import Heos, HeosException

    client = {}

    if host is None:
        _LOGGER.info('No host provided, will try to discover...')
    heos = Heos(host)

    _LOGGER.info('Using language "{}".'.format(lang))

    return HeosNotificationService(heos, lang, volume)


class HeosNotificationService(BaseNotificationService):
    """Implement the notification service for Heos service."""

    def __init__(self, heos, lang, volume):
        """Initialize the service."""
        self._heos = heos
        self._lang = lang
        self._volume = volume

    # pylint: disable=unused-argument
    def send_message(self, message="", **kwargs):
        """Send a message to Heos."""
        from gtts import gTTS
        from heos import Heos, HeosException
        import io

        content = io.BytesIO()
        _LOGGER.info('Heos got message "{}"'.format(message))
        try:
            tts = gTTS(text=message, lang=self._lang)
            tts.write_to_fp(content)
        except Exception as e:
            _LOGGER.error('Could not convert text to speech.')
            content.close()
            return

        self._heos.play_content(content.getvalue(), 'audio/mpeg')
        content.close()
