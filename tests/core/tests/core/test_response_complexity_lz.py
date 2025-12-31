"""
Test 4: Post-Perturbation Complexity Metric (Lempel-Ziv Proxy)

Probes:
- Axiom 4 (Counterfactual Sensitivity)
- Structural distinction between fragmented, unstable, and coherent regimes

This exploratory simulation estimates response complexity using a
compression-based approximation of Lempel-Ziv complexity.

System responses following a counterfactual perturbation are discretized,
compressed, and compared across regimes.

This metric is used as a qualitative proxy for structured, non-random,
non-trivial dynamics. It is not a validated measure of consciousness,
integrated information, or clinical PCI.

Results are illustrative and sensitive to discretization and parameter choices.
"""

import numpy as np
import matplotlib.pyplot as plt
import zlib  # Used for compression (LZ77 algorithm variant)

# --- HELPER: COMPLEXITY METRIC ---
def calculate_lz_complexity(data_matrix):
    """
    Approximates Lempel-Ziv complexity using compression size.
    1. Discretize continuous data into binary (0 or 1).
    2. Convert to a string.
    3. Compress and measure size.
    """
    # 1. Binarize: Is the value increasing or decreasing? (Simple derivative encoding)
    # Or simply: Is it above the mean? Let's use Mean Thresholding.
    threshold = np.mean(data_matrix)
    binary_matrix = (data_matrix > threshold).astype(int)
    
    # 2. Flatten to a single string of bits for the whole system state over time
    binary_string = "".join(map(str, binary_matrix.flatten()))
    
    # 3. Compress using zlib (Standard DEFLATE/LZ77)
    compressed_data = zlib.compress(binary_string.encode('utf-8'))
    
    # Complexity = Size of compressed data / Size of original data
    # Higher Ratio = Harder to compress = Higher Complexity
    return len(compressed_data)

# --- SYSTEM SIMULATION (Reused from Test 2) ---
class StreamSystem:
    def __init__(self, mode="coherent"):
        self.mode = mode
        self.x = np.zeros(3)
        self.decay = np.array([0.8, 0.8, 0.95]) 
        
        if mode == "fragmented":
            self.W = np.zeros((3,3)) # No binding
        elif mode == "coherent":
            self.W = np.array([
                [ 0.0,  0.4, -0.2],
                [ 0.4,  0.0, -0.2],
                [ 0.1,  0.1,  0.0]
            ])
        elif mode == "unstable":
            self.W = np.array([
                [ 0.0,  0.9,  0.5],
                [ 0.9,  0.0,  0.5],
                [ 0.5,  0.5,  0.0]
            ])

    def step(self, shock=None):
        self.x = self.x * self.decay
        interaction = np.tanh(np.dot(self.W, self.x))
        self.x += interaction
        if shock is not None: self.x += shock
        self.x += np.random.normal(0, 0.01, 3) # Tiny noise
        return self.x

# --- RUN EXPERIMENT ---

steps = 150
shock_time = 30
shock_vector = np.array([5.0, 0.0, 0.0])

systems = {
    "Fragmented": StreamSystem("fragmented"),
    "Unstable (Seizure)": StreamSystem("unstable"),
    "Coherent":     StreamSystem("coherent")
}

results = {name: [] for name in systems}

# Run loop
for t in range(steps):
    shock = shock_vector if t == shock_time else None
    for name, sys in systems.items():
        state = sys.step(shock)
        # We record the response AFTER the shock for complexity analysis
        if t >= shock_time:
            results[name].append(state.copy())

# --- CALCULATE COMPLEXITY ---
complexity_scores = {}
print("--- COMPLEXITY SCORES (Higher is better) ---")
for name, data in results.items():
    data_array = np.array(data)
    score = calculate_lz_complexity(data_array)
    complexity_scores[name] = score
    print(f"{name}: {score}")

# --- VISUALIZATION ---
plt.figure(figsize=(10, 6))

# Bar Chart of Complexity
names = list(complexity_scores.keys())
scores = list(complexity_scores.values())
colors = ['gray', 'red', 'blue']

bars = plt.bar(names, scores, color=colors, alpha=0.8)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}', ha='center', va='bottom', fontweight='bold')

plt.title("Lempel-Ziv Complexity of Post-Perturbation Response")
plt.ylabel("Compressed Information Size (Bytes)")
plt.ylim(0, max(scores) * 1.2)
plt.grid(axis='y', alpha=0.3)

# Add definition annotations
plt.figtext(0.5, 0.01, 
            "Fragmented: Signals die out (Low Info).  Unstable: Repetitive loops (Redundant).  Coherent: Structured Integration (High Info).", 
            ha="center", fontsize=9, bbox={"facecolor":"white", "alpha":0.5, "pad":5})

plt.show()
