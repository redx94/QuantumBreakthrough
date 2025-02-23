from typing import Dict, List, Optional
import time
from dataclasses import dataclass, field
from collections import defaultdict
import logging

@dataclass
class ErrorEvent:
    timestamp: float
    error_type: str
    message: str
    circuit_metadata: Optional[Dict] = None
    stack_trace: Optional[str] = None

class ErrorTracker:
    """Tracks and analyzes quantum circuit errors."""
    
    def __init__(self):
        self.errors: List[ErrorEvent] = []
        self.error_counts = defaultdict(int)
        self.logger = logging.getLogger(__name__)

    def record_error(self, error_type: str, message: str, 
                    circuit_metadata: Optional[Dict] = None,
                    stack_trace: Optional[str] = None) -> None:
        """Record a new error event."""
        event = ErrorEvent(
            timestamp=time.time(),
            error_type=error_type,
            message=message,
            circuit_metadata=circuit_metadata,
            stack_trace=stack_trace
        )
        self.errors.append(event)
        self.error_counts[error_type] += 1
        self.logger.error(f"{error_type}: {message}")

    def get_error_statistics(self) -> Dict:
        """Get statistical analysis of recorded errors."""
        return {
            'total_errors': len(self.errors),
            'error_types': dict(self.error_counts),
            'error_rate': len(self.errors) / max(1, sum(self.error_counts.values())),
            'most_common_error': max(self.error_counts.items(), 
                                   key=lambda x: x[1], 
                                   default=('none', 0))
        }

    def clear_history(self) -> None:
        """Clear error history."""
        self.errors.clear()
        self.error_counts.clear()
