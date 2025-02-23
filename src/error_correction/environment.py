from qiskit import QuantumCircuit, Aer, execute
from qiskit.providers.aer.noise import NoiseModel
from qiskit.quantum_info import state_fidelity
import numpy as np

class QuantumErrorEnv:
    def __init__(self, num_qubits=2, error_rate=0.01):
        self.num_qubits = num_qubits
        self.error_rate = error_rate
        self.noise_model = self._create_noise_model()
        self.backend = Aer.get_backend('aer_simulator')
        
    def _create_noise_model(self):
        """Create a simple noise model with depolarizing error."""
        noise_model = NoiseModel()
        # Add depolarizing error to all gates
        error = noise_model.add_all_qubit_quantum_error(
            noise_model.depolarizing_error(self.error_rate, 1), 
            ['u1', 'u2', 'u3']
        )
        return noise_model
        
    def reset(self):
        """Reset the environment and return initial state."""
        self.circuit = QuantumCircuit(self.num_qubits)
        self.circuit.h(0)
        self.circuit.cx(0, 1)
        return self._get_state()
        
    def step(self, action):
        """Execute one step in the environment."""
        # Apply correction based on action
        if action == 1:
            self.circuit.x(0)
        elif action == 2:
            self.circuit.z(0)
        # ... more actions ...
        
        # Get results and calculate reward
        state = self._get_state()
        reward = self._calculate_reward()
        done = True  # Episode ends after correction
        
        return state, reward, done, {}
        
    def _get_state(self):
        """Get current quantum state as environment state."""
        result = execute(self.circuit, 
                        self.backend,
                        noise_model=self.noise_model).result()
        return result.get_statevector()
        
    def _calculate_reward(self):
        """Calculate reward based on state fidelity."""
        perfect_state = execute(self.circuit, 
                              self.backend).result().get_statevector()
        noisy_state = self._get_state()
        return state_fidelity(perfect_state, noisy_state)
