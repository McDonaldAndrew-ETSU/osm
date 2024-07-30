import logging
from ui import MapNavigator


class DeviceController:
    def __init__(self, navigator: MapNavigator):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        self.navigator = navigator

    def toggle_map_matching(self, event):
        if event.key.lower() == "m":
            self.navigator.map_matching = not self.navigator.map_matching
            self.logger.info(f"Map matching toggled to: {self.navigator.map_matching}")
