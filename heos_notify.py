"""
Heos notification service.
"""
import logging

from homeassistant.components.notify import (BaseNotificationService, DOMAIN)
# from homeassistant.const import (CONF_HOST, CONF_NAME)
# from homeassistant.helpers import validate_config

REQUIREMENTS = ['https://github.com/andryd/heos/archive/v0.1.2.zip#heos==0.1.2',
                'gTTS', 'lxml', 'httplib2']

_LOGGER = logging.getLogger(__name__)


def get_service(hass, config):
    """Return the notify service."""
    # if not validate_config({DOMAIN: config}, {DOMAIN: [CONF_HOST, CONF_NAME]},
    #                        _LOGGER):
    #     return None

    # host = config.get(CONF_HOST, None)
    host = None
    # lang = config.get(CONF_LANG, None)
    # volume = config.get(CONF_VOL, None)
    lang = None

    from heos import Heos, HeosException

    client = {}

    if host:
        heos = Heos(host)
    else:
        _LOGGER.info('No host provided, will try to discover...')
        heos = Heos()

    if not lang:
        lang = 'en'
        _LOGGER.info('No language provided, using "{}".'.format(lang))

    # except HeosException:
    #     _LOGGER.error('Connection failed.')
    #     return None
    # except OSError:
    #     _LOGGER.error('Host unreachable.')
    #     return None

    return HeosNotificationService(heos, lang)


class HeosNotificationService(BaseNotificationService):
    """Implement the notification service for Heos service."""

    def __init__(self, heos, lang):
        """Initialize the service."""
        self._heos = heos
        self._lang = lang

    # pylint: disable=unused-argument
    def send_message(self, message="", **kwargs):
        """Send a message to Heos."""
        from gtts import gTTS
        from heos import Heos, HeosException
        import io

        content = io.BytesIO()
        _LOGGER.info('Heos got message "{}"'.format(message))
        tts = gTTS(text=message, lang=self._lang)
        # tts.save("hello.mp3")
        tts.write_to_fp(content)

        self._heos.play_content(content.getvalue(), 'audio/mpeg')
        content.close()
