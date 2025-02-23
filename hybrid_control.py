#!/usr/bin/env python
# Hybrid Quantum-Classical Control System

def decide_allocation(task_complexity, system_noise, available_quantum_volume):
    if available_quantum_volume > task_complexity and system_noise < 0.1:
        return "quantum"
    return "classical"

if __name__ == "__main__":
    print("Hybrid Control System Activated.")
