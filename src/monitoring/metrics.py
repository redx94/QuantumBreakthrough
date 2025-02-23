from dataclasses import dataclass
from typing import Dict, Any
import time
import psutil
import logging
from prometheus_client import Counter, Gauge, Histogram, Summary
from contextlib import contextmanager

@dataclass
class MetricsCollector:
    """Collect and export metrics for monitoring."""
    
    circuit_executions = Counter('circuit_executions_total', 'Total circuit executions')
    error_rate = Gauge('error_rate', 'Current error rate')
    execution_time = Histogram('execution_time_seconds', 'Time spent executing circuits')
    memory_usage = Gauge('memory_usage_bytes', 'Current memory usage')
    
    def record_execution(self, circuit_depth: int, execution_time: float):
        """Record metrics for a circuit execution."""
        self.circuit_executions.inc()
        self.execution_time.observe(execution_time)
        self.memory_usage.set(psutil.Process().memory_info().rss)
        
    def record_error_rate(self, error_rate: float):
        """Record current error rate."""
        self.error_rate.set(error_rate)

class QuantumMetricsCollector:
    def __init__(self):
        self._initialize_metrics()
        self.collection_enabled = True

    def _initialize_metrics(self) -> None:
        """Initialize comprehensive metrics collection."""
        self.circuit_depth = Histogram('circuit_depth', 
                                     'Circuit depth distribution',
                                     buckets=(1, 2, 5, 10, 20, 50, 100))
        self.error_rate = Summary('error_rate', 
                                'Error rate distribution',
                                ['error_type'])
        self.execution_time = Histogram('execution_time_seconds',
                                      'Circuit execution time',
                                      buckets=(.001, .005, .01, .05, .1, .5))

    @contextmanager
    def measure_execution_time(self, circuit_id: str):
        """Context manager for measuring execution time."""
        start_time = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start_time
            self.execution_time.observe(duration)
