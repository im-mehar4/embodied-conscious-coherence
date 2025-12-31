"""
Test 2: Structural Integrity and Binding Regimes

Probes:
- Prediction 1 (Systems without binding fail recovery-based tests)
- Axiom 4 (Counterfactual Sensitivity)

This exploratory simulation compares three multi-stream architectures:
1. Fragmented (unbound)
2. Coherent (balanced binding with regulation)
3. Unstable (over-bound, positive feedback)

A counterfactual perturbation is injected into a single stream, and
system-wide responses are observed.

This test examines qualitative differences in perturbation propagation,
reorganization, and recovery.

This is not a proof of consciousness, intelligence, or biological realism.
Results are illustrative and sensitive to parameter choices.
"""

import numpy as np
import matplotlib.pyplot as plt

class StreamSystem:
    def __init__(self, mode="coherent"):
        self.mode = mode
        
        # DEFINITION 1: STREAMS
        # State Vector x = [Sensory, Somatic, Symbolic]
        self.x = np.zeros(3)
        
        # Internal dampening (decay rate) for each stream
        # 0.9 means it retains 90% of its state (memory)
        self.decay = np.array([0.8, 0.8, 0.95]) 
        
        # DEFINITION 2: BINDING MATRIX (Interaction Weights)

        # NOTE: In the fragmented condition, streams exist but are not dynamically bound.
        # The symbolic stream has no regulatory influence without coupling.
        if mode == "fragmented":
            # No cross-talk. Diagonal matrix.
            self.W = np.array([
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0]
            ])
            
        elif mode == "coherent":
            # Balanced coupling.
            # Sensory <-> Somatic (Strong loop)
            # Symbolic -> Down-regulates both (Negative feedback)
            self.W = np.array([
                [ 0.0,  0.4, -0.2],  # Sensory affected by Somatic & Symbol
                [ 0.4,  0.0, -0.2],  # Somatic affected by Sensory & Symbol
                [ 0.1,  0.1,  0.0]   # Symbol observes both
            ])
            
        elif mode == "unstable":
            # Over-coupling (Positive feedback loops everywhere)
            self.W = np.array([
                [ 0.0,  0.9,  0.5],
                [ 0.9,  0.0,  0.5],
                [ 0.5,  0.5,  0.0]
            ])

    def step(self, shock=None):
        # 1. Apply Decay (Self-dynamics)
        self.x = self.x * self.decay
        
        # 2. Calculate Cross-Talk (Binding)
        # We use a tanh activation to simulate biological saturation constraints
        # (Neurons can't fire infinitely fast)
        interaction = np.tanh(np.dot(self.W, self.x))
        
        # 3. Update State
        self.x += interaction
        
        # 4. Inject Shock (Counterfactual Perturbation)
        if shock is not None:
            self.x += shock
            
        # Add tiny baseline noise (life is never perfectly still)
        self.x += np.random.normal(0, 0.01, 3)
        
        return self.x

# --- SIMULATION PARAMETERS ---

steps = 100
shock_time = 30
shock_vector = np.array([5.0, 0.0, 0.0]) # Massive shock to SENSORY stream only

# Initialize Systems
systems = {
    "Fragmented (Unbound)": StreamSystem("fragmented"),
    "Coherent (Bound)":     StreamSystem("coherent"),
    "Unstable (Explosive)": StreamSystem("unstable")
}

# Data Storage
history = {name: [] for name in systems}

# --- RUN LOOP ---

for t in range(steps):
    shock = shock_vector if t == shock_time else None
    
    for name, sys in systems.items():
        state = sys.step(shock)
        history[name].append(state.copy())

# --- VISUALIZATION ---

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for i, (name, data) in enumerate(history.items()):
    data = np.array(data)
    ax = axes[i]
    
    # Plot the 3 Streams
    ax.plot(data[:, 0], label='Sensory', color='red', linewidth=2)
    ax.plot(data[:, 1], label='Somatic', color='green', linewidth=2)
    ax.plot(data[:, 2], label='Symbolic', color='blue', linestyle='--', linewidth=2)
    
    # Visuals
    ax.axvline(x=shock_time, color='black', linestyle=':', label='Shock')
    ax.set_title(name)
    ax.set_ylim(-6, 6)
    ax.grid(True, alpha=0.3)
    if i == 0: ax.legend()

plt.tight_layout()
plt.show()
