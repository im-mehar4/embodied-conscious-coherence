"""
Test 1: Reactive vs Symbolically Stabilized Control

Probes:
- Axiom 6 (Symbolic Stabilization)
- Axiom 5 (Regulated Recovery)

This exploratory simulation compares a purely reactive continuous controller
with a discretized categorical controller under identical dynamics and noise.

This is not a proof of consciousness, intelligence, or optimal control.
Results are qualitative and sensitive to parameter choices.
"""

import numpy as np
import matplotlib.pyplot as plt

class CartPoleSimulation:
    def __init__(self, agent_type="zombie"):
        self.agent_type = agent_type
        self.angle = 0.0  # Pole angle (0 is vertical)
        self.velocity = 0.0
        self.history = []
        
        # Physics constants
        self.gravity = 0.1
        self.friction = 0.99
        self.force_mag = 0.05

    def get_action(self, noisy_angle):
        """
        Decides whether to push LEFT (-1) or RIGHT (+1)
        """
        if self.agent_type == "zombie":
            # ZOMBIE: Reacts to perfect, raw, continuous input.
            # If it leans 0.00001 left, it pushes right.
            # Brittle behavior: Over-correction.
            return -1 if noisy_angle > 0 else 1

        elif self.agent_type == "coherent":
            # COHERENT: Uses a Symbolic Bottleneck.
            # It discretizes the world into 3 Symbols:
            # 0: STABLE (Do nothing)
            # 1: DANGER_RIGHT
            # -1: DANGER_LEFT

            # NOTE: This discretization represents structural categorization,
            # not semantic meaning or language.
          
            # The "Symbolic Threshold" (The Governor)
            threshold = 0.05 
            
            if noisy_angle > threshold:
                return -1 # Correct Right Lean
            elif noisy_angle < -threshold:
                return 1  # Correct Left Lean
            else:
                return 0  # Symbol is "Stable" -> Do nothing

    def step(self, t):
        # 1. Generate Environment Noise (The "Adversarial Attack")
        # In a calm room, noise is 0. In a storm, it's high.
        noise = np.random.normal(0, 0.02)
        
        # 2. The Agent sees the angle + noise
        perceived_angle = self.angle + noise
        
        # 3. Agent decides action
        action = self.get_action(perceived_angle)
        
        # 4. Physics Update
        # Force applied by agent
        force = action * self.force_mag
        
        # Update velocity (Gravity pulls it down, Agent pushes it up)
        self.velocity += force + (self.angle * 0.01) 
        self.velocity *= self.friction # Damping
        
        # Update angle
        self.angle += self.velocity
        
        # Log data
        self.history.append(self.angle)

# --- RUN THE TEST ---

steps = 300

# 1. Run Zombie
zombie_sim = CartPoleSimulation("zombie")
for t in range(steps):
    zombie_sim.step(t)

# 2. Run Coherent
coherent_sim = CartPoleSimulation("coherent")
for t in range(steps):
    coherent_sim.step(t)

# --- VISUALIZATION REFACTOR ---

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for i, (name, data) in enumerate(history.items()):
    data = np.array(data)
    ax = axes[i]
    
    # Plot the 3 Streams
    ax.plot(data[:, 0], label='Sensory', color='red', linewidth=2, alpha=0.8)
    ax.plot(data[:, 1], label='Somatic', color='green', linewidth=2, alpha=0.8)
    ax.plot(data[:, 2], label='Symbolic', color='blue', linestyle='--', linewidth=2)
    
    ax.axvline(x=shock_time, color='black', linestyle=':', label='Shock Event')
    ax.set_title(name)
    ax.grid(True, alpha=0.3)
    
    # FIX: Different scales for different regimes
    if name == "Unstable (Explosive)":
        # Let this one autoscale so we see the "Latching" effect (it will go up to ~20)
        ax.set_ylim(-2, 25) 
        ax.text(shock_time + 5, 20, "SYSTEM LATCHED", color='red', fontsize=10, fontweight='bold')
    else:
        ax.set_ylim(-2, 8) # Focused view for stable systems

    if i == 0: ax.legend(loc='upper right')

plt.tight_layout()
plt.show()
