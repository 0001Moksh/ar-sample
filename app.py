# app.py (or your main Flask file)

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    # List of models with their display names and filenames
    models_data = [
        {'name': 'mouse', 'filename': 'mouse2.glb'},
        {'name': 'Ganesha_Candle_Holder', 'filename': 'Ganesha_Candle_Holder.glb'},
        {'name': 'Fountain', 'filename': 'Fountain.glb'},
        {'name': 'Blue_White_Radiance', 'filename': 'Blue_White_Radiance.glb'},
        {'name': 'Lamp With Shade', 'filename': 'Lamp With Shade.glb'},
        {'name': 'Sofa', 'filename': 'Sofa.glb'},
        {'name': 'Office Chair', 'filename': 'Office Chair.glb'},
        # Add more models here if needed
        # {'name': 'Another Item', 'filename': 'another_item.glb'},
    ]
    # Pass the list to the template context
    return render_template('index.html', models=models_data)

if __name__ == '__main__':
    # Make sure debug is False in production!
    # Use host='0.0.0.0' to make it accessible on your network if needed
    app.run(debug=True)