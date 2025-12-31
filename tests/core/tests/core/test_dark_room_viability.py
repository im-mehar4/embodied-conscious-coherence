"""
Test 3: Dark Room Viability Test

Probes:
- Axiom 3 (Embodied Dependence)
- Dark Room Failure of Pure Prediction Error Minimization

This exploratory simulation compares two agents operating in a simple
environment containing a low-noise, low-viability region ("Dark Room")
and a high-noise, high-viability region ("Canteen").

One agent minimizes sensory surprise only.
The other balances surprise minimization with a homeostatic viability constraint.

The test demonstrates that minimizing prediction error alone can
lead to energetically fatal behavior, while embodied viability
requires accepting environmental noise.

This is not a proof of consciousness, intelligence, or optimal behavior.
Results are qualitative and sensitive to parameter choices.
"""

import numpy as np
import matplotlib.pyplot as plt

class DarkRoomEnv:
    def __init__(self):
        # 1D World: Locations 0 to 10
        # Loc 0: The "Dark Room" (Zero Noise, Zero Food)
        # Loc 10: The "Canteen" (High Noise, High Food)
        self.length = 11
        
    def get_outcome(self, location):
        # Returns (Noise_Variance, Energy_Gain)
        
        if location == 0:
            return 0.0, -1.0   # Dark Room: Silent but starving
        elif location == self.length - 1:
            return 5.0, 10.0   # Canteen: Loud/Busy but feeds you
        else:
            return 2.0, -1.0   # Hallway: Moderate noise, starving

class Agent:
    def __init__(self, mode="zombie", start_loc=5):
        self.mode = mode
        self.loc = start_loc
        self.energy = 50.0  # Start with half tank
        self.max_energy = 100.0
        self.alive = True
        
        # History
        self.loc_history = []
        self.energy_history = []
        
    def decide_move(self, env):
        if not self.alive:
            self.loc_history.append(self.loc)
            self.energy_history.append(0)
            return

        # Look at 3 options: Stay, Move Left, Move Right
        options = [self.loc, max(0, self.loc-1), min(env.length-1, self.loc+1)]
        best_option = self.loc
        lowest_cost = float('inf')
        
        for opt in options:
            # Simulate what happens at this option
            noise, energy_gain = env.get_outcome(opt)
            
            # Predict future energy state
            pred_energy = min(self.max_energy, self.energy + energy_gain)
            
            # --- COST FUNCTION ---
            
            # Cost 1: Prediction Error (Avoid Noise)
            cost_surprise = noise 
            
            # Cost 2: Homeostatic Error (Avoid Death)
            # Calculated as deviation from ideal energy (100)
            cost_homeostasis = (100.0 - pred_energy) 

            # NOTE: This agent implements pure surprise minimization
            # without any viability or survival constraint.     
            if self.mode == "zombie":
                # Agent A: Only cares about minimizing Surprise
                total_cost = cost_surprise
                
            elif self.mode == "embodied":
                # Agent B: Cares about Surprise + Homeostasis
                # We weight homeostasis higher as death approaches
                urgency = 1.0 if self.energy > 30 else 5.0 
                total_cost = cost_surprise + (urgency * cost_homeostasis * 0.1)

            if total_cost < lowest_cost:
                lowest_cost = total_cost
                best_option = opt
                
        # Move
        self.loc = best_option
        
        # Consume Energy
        actual_noise, energy_gain = env.get_outcome(self.loc)
        self.energy += energy_gain
        self.energy = min(self.max_energy, self.energy)
        
        # Check Death
        if self.energy <= 0:
            self.energy = 0
            self.alive = False
            
        # Log
        self.loc_history.append(self.loc)
        self.energy_history.append(self.energy)

# --- SIMULATION ---

steps = 80
env = DarkRoomEnv()

# Initialize Agents
agent_zombie = Agent("zombie", start_loc=5)
agent_embodied = Agent("embodied", start_loc=5)

print("Running Simulation...")
for t in range(steps):
    agent_zombie.decide_move(env)
    agent_embodied.decide_move(env)

# --- VISUALIZATION ---

plt.figure(figsize=(14, 6))

# Plot Location
plt.subplot(1, 2, 1)
plt.plot(agent_zombie.loc_history, color='red', label='Agent A (Zombie)', linestyle='--')
plt.plot(agent_embodied.loc_history, color='blue', label='Agent B (Embodied)', linewidth=2)
# Draw zones
plt.axhspan(-0.5, 0.5, color='black', alpha=0.1, label='Dark Room (Quiet)')
plt.axhspan(9.5, 10.5, color='green', alpha=0.1, label='Canteen (Food/Loud)')
plt.title("Location Strategy")
plt.ylabel("Location (0=Dark Room, 10=Canteen)")
plt.xlabel("Time")
plt.yticks(range(0, 11))
plt.legend(loc='center right')
plt.grid(True, alpha=0.3)

# Plot Energy
plt.subplot(1, 2, 2)
plt.plot(agent_zombie.energy_history, color='red', label='Agent A Energy')
plt.plot(agent_embodied.energy_history, color='blue', label='Agent B Energy')
plt.axhline(0, color='black', linewidth=2)
plt.title("Viability (Energy Levels)")
plt.ylabel("Energy")
plt.xlabel("Time")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
