import pytest
import numpy as np
from src.adaptive_error_correction.environment import QuantumEnvironment, EnvironmentConfig

@pytest.fixture
def env():
    config = EnvironmentConfig(num_qubits=2, noise_level=0.01)
    return QuantumEnvironment(config)

def test_environment_initialization(env):
    assert env.num_qubits == 2
    assert env.noise_level == 0.01
    assert env.action_size == 4

def test_reset(env):
    state = env.reset()
    assert isinstance(state, np.ndarray)
    assert len(state) == 2 ** env.num_qubits

def test_step(env):
    env.reset()
    next_state, reward, done, info = env.step(0)
    assert isinstance(next_state, np.ndarray)
    assert isinstance(reward, float)
    assert isinstance(done, bool)
    assert isinstance(info, dict)

def test_invalid_action(env):
    env.reset()
    with pytest.raises(ValueError):
        env.step(10)  # Invalid action
