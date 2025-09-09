import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Define synthetic data based on your logic
# Columns: [is_level2, magic_weapon, magic_armor, steel_armor]
X = np.array([
    [1, 1, 1, 0],  # High win rate, low TTK (Best combo in Level 2)
    [0, 0, 0, 1],  # High win rate, low TTK (Best combo in Level 1)
    [1, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 1, 0, 0],  # Medium-high win rate
    [0, 0, 0, 0],
    [0, 0, 1, 0],  # Medium win rate, low TTK
    [1, 1, 0, 1],
    [1, 0, 1, 0],  # Medium-low win rate
    [0, 1, 0, 1],  # Medium win rate, low TTK
    [1, 0, 1, 1],  # Medium win rate, higher TTK
    [0, 1, 0, 0],  # Low win rate
    [1, 0, 0, 1],  # Low win rate, high TTK (Wrong gear in Level 2)
    [0, 1, 1, 0],  # Low win rate, high TTK (Wrong gear in Level 1)
])

# Corresponding win rate targets (float between 0 and 1)
win_rate = np.array([
    0.98,  # Best combo
    0.95,  # Best combo
    0.95,
    0.98,
    0.68,  # Mid combo
    0.65,  # Mid combo
    0.6,  
    0.48,
    0.45,
    0.45,
    0.45,   # Poor combo
    0.45,  # Poor combo
    0.25,
    0.23,
])

# Corresponding avg ttk (lower is better)
avg_ttk = np.array([
    1.2,  # Best combo
    1.1,  # Best combo
    1.1,
    1.2,
    1.3,  # Mid combo
    1.4,
    1.4,
    1.3,
    2.1,
    2.2,
    2.3,  # Poor combo
    2.3,  # Poor combo
    2.4,
    2.5,
])

# Create models
win_model = RandomForestRegressor(n_estimators=100, random_state=42)
ttk_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train
win_model.fit(X, win_rate)
ttk_model.fit(X, avg_ttk)

# Save both models
joblib.dump({'win_model': win_model, 'ttk_model': ttk_model}, 'reco_model.pkl')

print("Model training completed and saved as reco_model.pkl")