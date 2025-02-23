from typing import Dict, Any, List
import time
import psutil
import numpy as np
from dataclasses import dataclass, field
from collections import deque

@dataclass
class PerformanceMetrics:
    execution_times: deque = field(default_factory=lambda: deque(maxlen=1000))
    memory_usage: deque = field(default_factory=lambda: deque(maxlen=1000))
    circuit_depths: deque = field(default_factory=lambda: deque(maxlen=1000))

class PerformanceMonitor:
    def __init__(self, metrics_window: int = 1000):
        self.metrics = PerformanceMetrics()
        self.start_time = time.time()
        self.alert_thresholds = {
            'max_execution_time': 5.0,  # seconds
            'max_memory_usage': 1024,   # MB
            'max_circuit_depth': 100
        }
    
    def record_execution(self, execution_time: float) -> None:
        self.metrics.execution_times.append(execution_time)
    
    def record_memory(self) -> None:
        self.metrics.memory_usage.append(
            psutil.Process().memory_info().rss / 1024 / 1024
        )
    
    def record_circuit_depth(self, depth: int) -> None:
        self.metrics.circuit_depths.append(depth)
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            'avg_execution_time': np.mean(self.metrics.execution_times),
            'avg_memory_usage': np.mean(self.metrics.memory_usage),
            'avg_circuit_depth': np.mean(self.metrics.circuit_depths),
            'total_runtime': time.time() - self.start_time
        }
    
    def track_circuit_execution(self, circuit_id: str):
        """Track circuit execution performance"""
        try:
            start_time = time.time()
            yield
        finally:
            duration = time.time() - start_time
            self.metrics.execution_times.append({
                'circuit_id': circuit_id,
                'duration': duration,
                'timestamp': time.time()
            })
    
    def analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends and patterns"""
        return {
            'execution_trend': self._calculate_trend(self.metrics.execution_times),
            'memory_trend': self._calculate_trend(self.metrics.memory_usage),
            'depth_trend': self._calculate_trend(self.metrics.circuit_depths),
            'anomalies': self._detect_anomalies()
        }
    
    def _calculate_trend(self, data: List[float]) -> Dict[str, float]:
        if len(data) < 2:
            return {'slope': 0.0, 'variance': 0.0}
        return {
            'slope': np.polyfit(range(len(data)), data, 1)[0],
            'variance': np.var(data)
        }
