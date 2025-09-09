from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# Load both win rate and TTK models
models = joblib.load('reco_model.pkl')
win_model = models['win_model']
ttk_model = models['ttk_model']

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    print(data)

    # === Prepare features for prediction ===
    features = [
        1 if data['level'] == 'level2' else 0,
        1 if data['equipped_weapon'].lower() == 'magic wand' else 0,
        1 if data['equipped_armor'].lower() == 'magic armor' else 0,
        1 if data['equipped_armor'].lower() == 'steel armor' else 0,
    ]

    # === Predict win rate & avg TTK ===
    predicted_win_rate = win_model.predict([features])[0]
    predicted_avg_ttk = ttk_model.predict([features])[0]

    # === Extract variables ===
    is_level1 = data['level'] == 'level1'
    is_level2 = data['level'] == 'level2'
    coins = data['coins']
    purchased_items = [item.lower() for item in data.get('purchased_items', [])]

    recommended_items = []

    # === Level 1 Recommendations ===
    if (
        predicted_win_rate < 0.5 and
        predicted_avg_ttk > 2.0 and
        is_level1 and
        coins < 500
    ):
        if 'basic_gun' in purchased_items and 'steel_armor' not in purchased_items:
            recommended_items = ['Colect some money for Steel Armor and equip Basic Gun']
        elif 'basic_gun' in purchased_items and 'steel_armor' in purchased_items:
            recommended_items = ['Equip Basic Gun and Steel Armor']

    if (
        predicted_win_rate < 0.6 and
        predicted_avg_ttk >= 1.9 and
        is_level1
    ):
        recommended_items = ['Equip Basic Gun']

    elif (
        predicted_win_rate < 0.5 and
        predicted_avg_ttk > 2.0 and
        is_level1 and
        coins >= 500
    ):
        if 'basic_gun' in purchased_items and 'steel_armor' not in purchased_items:
            recommended_items = ['Buy & Equip Steel Armor and equip Basic Gun']
        elif 'basic_gun' in purchased_items and 'steel_armor' in purchased_items:
            recommended_items = ['Equip Basic Gun and Steel Armor']

    elif (
        predicted_win_rate < 0.7 and
        predicted_avg_ttk <= 1.6 and
        is_level1 and
        coins >= 500
    ):
        if 'steel_armor' in purchased_items :
            recommended_items = ['Equip Steel Armor.']
        elif 'steel_armor' not in purchased_items :
            recommended_items = ['Buy and Equip Steel Armor']

    elif (
        predicted_win_rate < 0.7 and
        predicted_avg_ttk <= 1.6 and
        is_level1 and
        coins < 500
    ):
        if 'steel_armor' in purchased_items :
            recommended_items = ['Equip Steel Armor.']
        elif 'steel_armor' not in purchased_items :
            recommended_items = ['Collect Some Money and Buy Steel Armor']

    elif (
        predicted_win_rate >= 0.85 and
        predicted_avg_ttk <= 1.5 and
        is_level1
    ):
        recommended_items = ['Best Equipments are Equiped For Level 1']

    # === Level 2 Recommendations (Critical Case) ===
    elif (
        predicted_win_rate < 0.5 and
        predicted_avg_ttk >= 1.9 and
        is_level2 and
        coins > 1200
    ):
        if 'magic_wand' not in purchased_items and 'magic_armor' not in purchased_items:
            recommended_items = ['Buy & Equip Magic Wand and Magic Armor']
        elif 'magic_wand' in purchased_items and 'magic_armor' in purchased_items:
            recommended_items = ['Equip Magic Wand and Magic Armor']

    elif (
        predicted_win_rate < 0.5 and
        predicted_avg_ttk >= 1.9 and
        is_level2 and
        coins > 700
    ):
        if 'magic_wand' not in purchased_items:
            recommended_items = ['Buy & Equip Magic Wand']
        elif 'magic_wand' in purchased_items:
            recommended_items = ['Equip Magic Wand']

    elif (
        predicted_win_rate < 0.5 and
        predicted_avg_ttk > 2.0 and
        is_level2 and
        coins > 500
    ):
        if 'magic_armor' not in purchased_items:
            recommended_items = ['Buy & Equip Magic Armor or Collect Some Money for Magic Wand']
        elif 'magic_armor' in purchased_items:
            recommended_items = ['Equip Magic Armor']

    # === Level 2 Recommendations (Mild Case) ===
    elif (
        predicted_win_rate < 0.6 and
        predicted_avg_ttk >= 1.9 and
        is_level2 and
        coins > 700
    ):
        if 'magic_wand' not in purchased_items:
            recommended_items = ['Buy & Equip Magic Wand']
        elif 'magic_wand' in purchased_items:
            recommended_items = ['Equip Magic Wand']

    elif (
        predicted_win_rate < 0.75 and
        predicted_avg_ttk <= 1.6 and
        is_level2 and
        coins > 500
    ):
        if 'magic_armor' in purchased_items:
            recommended_items = ['Equipe Magic Armor']
        elif 'magic_armor' not in purchased_items:
            recommended_items = ['Equip Magic Armor.']

    elif (
        predicted_win_rate >= 0.75 and
        predicted_avg_ttk <= 1.5 and
        is_level2
    ):
        recommended_items = ['Best Items Equiped for Level 2']

    # === Fallback ===
    if not recommended_items:
        recommended_items = ['Not Enough Money for Any of Items. Collect Some Money']

    return jsonify({
        'win_rate': round(float(predicted_win_rate), 2),
        'avg_ttk': round(float(predicted_avg_ttk), 2),
        'recommended_items': recommended_items
    })

if __name__ == '__main__':
    app.run(debug=True)
