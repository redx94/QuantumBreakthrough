import logging
import sys
import logging.handlers
from pathlib import Path
from typing import Optional, Dict, Any
import json
import time
import os

class LoggingManager:
    @staticmethod
    def setup_logging(
        log_level: int = logging.INFO,
        log_file: Optional[str] = None,
        max_bytes: int = 10485760,  # 10MB
        backup_count: int = 5
    ) -> None:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        handlers = [logging.StreamHandler(sys.stdout)]
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, 
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            handlers.append(file_handler)

        for handler in handlers:
            handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        for handler in handlers:
            root_logger.addHandler(handler)

class QuantumLogger:
    def __init__(self, name: str, log_level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self._setup_handlers()
        self.metrics = {}
        
    def _setup_handlers(self):
        # ...existing code...
        
    def log_quantum_event(self, event_type: str, data: Dict[str, Any]):
        """Log quantum-specific events with structured data"""
        try:
            log_entry = {
                "event_type": event_type,
                "quantum_data": data
            }
            self.logger.info(json.dumps(log_entry))
        except Exception as e:
            self.logger.error(f"Failed to log quantum event: {str(e)}")
    
    def log_with_context(self, level: int, message: str, **kwargs):
        """Enhanced contextual logging"""
        try:
            context = {
                "timestamp": time.time(),
                "process_id": os.getpid(),
                **kwargs
            }
            self.logger.log(level, json.dumps({"message": message, "context": context}))
        except Exception as e:
            self.logger.error(f"Logging failed: {str(e)}")
