import tensorflow as tf
import numpy as np

class ErrorCorrectionAgent:
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.model = self._build_model()
        
    def _build_model(self):
        """Build a simple policy network."""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(self.state_dim,)),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(self.action_dim, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy')
        return model
        
    def get_action(self, state):
        """Choose an action based on current state."""
        state = np.reshape(state, [1, -1])
        action_probs = self.model.predict(state)[0]
        return np.random.choice(self.action_dim, p=action_probs)
        
    def train(self, states, actions, advantages):
        """Update the policy based on advantages."""
        self.model.fit(states, actions, sample_weight=advantages, verbose=0)
