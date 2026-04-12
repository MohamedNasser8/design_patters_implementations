from abc import ABC, abstractmethod
from datetime import datetime
from logging import Logger
import os   
from enum import Enum

class LoggerType(Enum):
    CONSOLE = "console"
    FILE = "file"

class BaseLogger(ABC):
    def __init__(self, name: str):
        self.logger = Logger(name)

    @abstractmethod
    def log(self, message: str, level: str = 'info') -> None:
        pass

    def format_message(self, message: str, level: str = 'info') -> str:
        return f"{datetime.now().isoformat()} - {level.upper()} - {message}\n"


class ConsoleLogger(BaseLogger):
    _instance = None
    
    def __new__(cls, name: str = "ConsoleLogger") -> 'ConsoleLogger':
        if cls._instance is None:
            cls._instance = super(ConsoleLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, name: str = "ConsoleLogger"):
        # Only initialize once
        if not hasattr(self, '_initialized'):
            super().__init__(name)
            self._initialized = True

    def log(self, message: str, level: str = 'info') -> None:
        print(self.format_message(message, level), end='')


class FileLogger(BaseLogger):
    _instance = None
    
    def __new__(cls, filename: str = "app.log", max_size: int = 1024 * 1024 * 5) -> 'FileLogger':
        if cls._instance is None:
            cls._instance = super(FileLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, filename: str = "app.log", max_size: int = 1024 * 1024 * 5):
        # Only initialize once
        if not hasattr(self, '_initialized'):
            super().__init__("FileLogger")
            self.filename = filename
            self.max_size = max_size
            self._ensure_log_directory()
            self._initialized = True
    
    def _ensure_log_directory(self) -> None:
        """Create logs directory if it doesn't exist"""
        os.makedirs("../logs", exist_ok=True)
    
    def _get_log_filepath(self) -> str:
        """Get the current log file path with date"""
        return f"../logs/{self.filename}_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    def _rotate_if_needed(self, filepath: str) -> None:
        """Rotate log file if it exceeds max_size"""
        if os.path.exists(filepath) and os.path.getsize(filepath) >= self.max_size:
            # Create a backup with timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            backup_path = f"{filepath}.{timestamp}.bak"
            os.rename(filepath, backup_path)

    def log(self, message: str, level: str = 'info') -> None:
        filepath = self._get_log_filepath()
        self._rotate_if_needed(filepath)
        
        with open(filepath, 'a') as f:
            f.write(self.format_message(message, level))


def get_logger(name: str, logger_type: LoggerType = LoggerType.CONSOLE) -> BaseLogger:
    return ConsoleLogger(name) if logger_type == LoggerType.CONSOLE else FileLogger(name)