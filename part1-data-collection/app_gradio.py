import gradio as gr
import numpy as np
import joblib

def predict_steam_players(name, required_age, is_free, initial_price, discount_percent, genre, release_year):
    is_action = 1 if genre == "Action" else 0
    is_adventure = 1 if genre == "Adventure" else 0
    is_rpg = 1 if genre == "RPG" else 0
    is_indie = 1 if genre == "Indie" else 0
    is_strategy = 1 if genre == "Strategy" else 0
    is_other = 1 if genre == "Other" else 0

    features = np.array([[
        int(required_age),
        1 if is_free else 0,
        int(initial_price) if not is_free else 0,
        int(discount_percent) if not is_free else 0,
        is_other, is_action, is_adventure, is_rpg, is_indie, is_strategy,
        int(release_year)
    ]])

    try:
        raw_pred = model.predict(features)[0]
        final_pred = max(raw_pred, 0)
        return f"{name} {int(final_pred):,} Active Players"
    except NameError:
        return "Model not loaded"

interface = gr.Interface (
    fn=predict_steam_players,
    inputs=[
        gr.Textbox(label="Enter Game Title", placeholder="e.g. Clair Obscur"),
        gr.Number(label="Required Age Rating", value=0),
        gr.Checkbox(label="Is it free?"),
        gr.Number(label="Initial Price", value=20),
        gr.Number(label="Discount Percent", value=0),
        gr.Dropdown(["Action", "Adventure", "RPG", "Indie", "Strategy", "Other"], label="Primary Genre", value="Action"),
        gr.Number(label="Release Year", value=2026)
    ],
    outputs=gr.Textbox(label="Model Prediction"),
    title="Steam Concurrent Player Predictor",
    description="Input your game data to test the Linear Regression algorithm :D"
)

if __name__ == "__main__":
    try:
        model = joblib.load("steam_model.pkl")
    except Exception as e:
        print(f"An error occured: {e}")
        exit()
    interface.launch()