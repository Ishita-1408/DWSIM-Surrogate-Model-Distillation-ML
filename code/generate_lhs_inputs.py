import numpy as np
import pandas as pd

# =========================
# FORCE SAMPLE SIZE
# =========================
n_samples = 600

print("🔥 Generating", n_samples, "samples...")

# =========================
# Define ranges
# =========================
ranges = {
    "T_feed": (80, 130),
    "P_feed": (1.0, 2.0),
    "z_benzene": (0.2, 0.8),
    "reflux_ratio": (1.2, 5.0),
    "stages": (10, 30),
    "feed_stage": (3, 25),
    "bottoms_flow": (20, 80)
}

# =========================
# Generate LHS manually
# =========================
lhs = np.random.rand(n_samples, len(ranges))

data = {}
for i, (key, (low, high)) in enumerate(ranges.items()):
    data[key] = low + (high - low) * lhs[:, i]

df = pd.DataFrame(data)

# Round discrete variables
df["stages"] = df["stages"].astype(int)
df["feed_stage"] = df["feed_stage"].astype(int)

# Save file
df.to_csv("../Dataset/lhs_input_cases.csv", index=False)

print("✅ LHS input file generated successfully!")