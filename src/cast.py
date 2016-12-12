import logging
import pychromecast

logger = logging.getLogger(__name__)


class Caster:
    def __init__(self, stream_url, preferred_chromecast=None):
        self.stream_url = stream_url

        logger.info("Searching for Chromecast devices...")
        chromecast_list = pychromecast.get_chromecasts_as_dict().keys()
        logger.debug("Found Chromecasts: %s", chromecast_list)

        if not chromecast_list:
            raise RuntimeError("Unable to find a Chromecast on the local network.")

        chromecast_name = None
        if preferred_chromecast:
            preferred_index = chromecast_list.index(preferred_chromecast)
            if preferred_index:
                chromecast_name = preferred_chromecast
            else:
                logger.warn("Couldn't find preferred chromecast")
                
        if chromecast_name is None:
            chromecast_name = chromecast_list[0]
            if len(chromecast_list) > 1:
                logger.warn("Multiple Chromecast devices detected")
                logger.warn("Found Chromecasts: %s", ', '.join(chromecast_list))
                logger.warn("Defaulting to Chromecast '%s'", chromecast_name)

        logger.info("Connecting to Chromecast '%s'", chromecast_name)
        self.chromecast = pychromecast.get_chromecast(
            friendly_name=chromecast_name)
        self.chromecast.wait()
        logger.info("Connected to Chromecast '%s'", chromecast_name)

    def start_stream(self):
        logger.info("Starting stream of URL %s on Chromecast '%s'",
                    self.stream_url, self.device_name)

        self.chromecast.quit_app()

        mc = self.chromecast.media_controller
        mc.play_media(self.stream_url, 'audio/flac', stream_type="LIVE")

    @property
    def device_name(self):
        return self.chromecast.device.friendly_name
