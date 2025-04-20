# app.py

from flask import Flask, render_template, url_for
import os # Import os module

app = Flask(__name__)

# --- Configuration ---
# Define base directories relative to the app's static folder
STATIC_FOLDER = 'static'
MODELS_DIR = 'model'
IMAGES_DIR = 'images'

@app.route('/')
def index():
    # List of models with display names, filenames, and image filenames
    # Assumes images are in static/images/ and models are in static/models/
    models_data = [
        {'name': 'Mouse', 'filename': 'mouse2.glb', 'image': 'mouse2.jpg'},
        {'name': 'Ganesha Candle Holder', 'filename': 'Ganesha_Candle_Holder.glb', 'image': 'Ganesha_Candle_Holder.png'}, # Example image extension
        {'name': 'Fountain', 'filename': 'Fountain.glb', 'image': 'Fountain.png'},
        {'name': 'Blue White Radiance', 'filename': 'Blue_White_Radiance.glb', 'image': 'Blue_White_Radiance.png'}, # Example image extension
        {'name': 'Key Holder with Phone', 'filename': 'Key_Holder_with_Phone.glb', 'image': 'Key_Holder_with_Phone.png'}, # Example image extension
        # {'name': 'Lamp With Shade', 'filename': 'Lamp With Shade.glb', 'image': 'Lamp With Shade.jpg'},
        # {'name': 'Sofa', 'filename': 'Sofa.glb', 'image': 'Sofa.png'},
        # {'name': 'Office Chair', 'filename': 'Office Chair.glb', 'image': 'Office_Chair.jpg'},

        # Add more models here if needed
        ]

    # --- Data Enrichment (Generate full URLs) ---
    # It's often cleaner to generate the full URLs here rather than repeating
    # url_for logic multiple times in the template.
    processed_models = []
    for model in models_data:
        # Construct paths relative to the static folder
        model_rel_path = os.path.join(MODELS_DIR, model['filename']).replace('\\', '/') # Ensure forward slashes
        image_rel_path = os.path.join(IMAGES_DIR, model['image']).replace('\\', '/') # Ensure forward slashes

        # Check if files exist (optional but good practice)
        model_abs_path = os.path.join(app.static_folder, model_rel_path)
        image_abs_path = os.path.join(app.static_folder, image_rel_path)

        if os.path.exists(model_abs_path) and os.path.exists(image_abs_path):
             processed_models.append({
                'name': model['name'],
                'model_url': url_for('static', filename=model_rel_path),
                'image_url': url_for('static', filename=image_rel_path),
                'alt_text': f"3D model preview image for {model['name']}" # For accessibility
            })
        else:
            print(f"Warning: Missing files for model '{model['name']}'.")
            if not os.path.exists(model_abs_path):
                print(f"  - Model file not found: {model_abs_path}")
            if not os.path.exists(image_abs_path):
                 print(f"  - Image file not found: {image_abs_path}")
            # Optionally skip this model or provide default placeholders
            # continue

    # Pass the processed list with URLs to the template context
    return render_template('index.html', models=processed_models)

if __name__ == '__main__':
    # Ensure the static subdirectories exist if they don't
    os.makedirs(os.path.join(app.static_folder, MODELS_DIR), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, IMAGES_DIR), exist_ok=True)

    # Make sure debug is False in production!
    # Use host='0.0.0.0' to make it accessible on your network if needed
    app.run(debug=True, host='0.0.0.0') # Added host='0.0.0.0'
