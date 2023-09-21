from .utils import MetaSingleton
from enum import Enum


class LevelEnum(Enum):
    info = "INFO"
    critical = "CRITICAL"
    # TODO: Add more options (ERROR, WARN)


class Logging(metaclass=MetaSingleton):
    def __init__(self, file_name: str) -> None:
        self.file_name: str = file_name

    def _write_log(self, level: LevelEnum, msg: str) -> None:
        """Write to the log file"""

        with open(self.file_name, "a") as log_file:
            log_file.write(f"[{level.name}] {msg}\n")  # [CRITICAL] message goes here...

    # create level specific methods
    def info(self, msg):
        self._write_log(LevelEnum.info, msg)

    # TODO: Add more level specific methods
    # - CRITICAL
    # - ERROR
    # - WARNING
