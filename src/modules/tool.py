from src.modules.logger import LOGGER
from src.modules.system_monitor import SystemMonitor



class Tool():
    def __init__(self,logger:LOGGER,system_monitor:SystemMonitor) -> None:
        self.logger = logger
        self.system_monitor = system_monitor
        