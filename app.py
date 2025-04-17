# c:\Users\renuk\OneDrive\Desktop\AR sample\app.py
import os
import socket
from flask import Flask, render_template, url_for

app = Flask(__name__)

# --- Helper function to get local IP address ---
def get_local_ip():
    """Attempts to detect the local IP address."""
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        return ip
    except socket.error:
        return None
    finally:
        if s:
            s.close()

# --- Product Data ---
# Define your products here. Each dictionary represents one item.
# Make sure the filenames match exactly what's in static/models/
# ADD .usdz FILES FOR iOS AR SUPPORT!
products_data = [
    {
        'id': 'lamp',
        'name': 'Lamp With Shade',
        'description': 'A classic shaded table lamp.',
        'model_glb': 'Lamp With Shade.glb',   # Needs to be in static/models/
        'model_usdz': 'Lamp With Shade.usdz', # Needs to be in static/models/ for iOS AR
        'alt_text': 'A 3D model of a lamp with a shade',
        # 'poster': 'posters/lamp_poster.webp' # Optional: Path relative to static/
    },
    {
        'id': 'astronaut',
        'name': 'Astronaut',
        'description': 'Ready for a spacewalk.',
        'model_glb': 'Astronaut.glb',         # Needs to be in static/models/
        'model_usdz': 'Astronaut.usdz',       # Needs to be in static/models/ for iOS AR
        'alt_text': 'A 3D model of an astronaut',
        # 'poster': 'posters/astronaut_poster.webp'
    },
    # Add more products like this:
    # {
    #     'id': 'robot',
    #     'name': 'Friendly Robot',
    #     'description': 'A helpful mechanical companion.',
    #     'model_glb': 'Robot.glb',
    #     'model_usdz': 'Robot.usdz',
    #     'alt_text': 'A 3D model of a friendly robot',
    # },
]

# --- Data Validation (Recommended) ---
valid_products = []
print("Checking for model files in static/models/...")
models_dir = os.path.join(app.static_folder, 'models') # Correct path to models subdir
if not os.path.isdir(models_dir):
     print(f"  [WARNING] 'static/models/' directory not found. Please create it.")
else:
    for p in products_data:
        glb_file = p.get('model_glb')
        usdz_file = p.get('model_usdz') # Needed for AR

        if not glb_file or not usdz_file:
             print(f"  [WARNING] Skipping '{p.get('name', 'Unknown')}' - missing 'model_glb' or 'model_usdz' key in app.py data.")
             continue

        glb_path = os.path.join(models_dir, glb_file)
        usdz_path = os.path.join(models_dir, usdz_file)

        glb_exists = os.path.exists(glb_path)
        usdz_exists = os.path.exists(usdz_path)

        # Require both GLB and USDZ for full functionality including AR
        if glb_exists and usdz_exists:
            valid_products.append(p)
            # print(f"  [OK] Found models for '{p['name']}'")
        else:
            print(f"  [WARNING] Skipping product '{p['name']}' due to missing files in static/models/:")
            if not glb_exists:
                print(f"    - Missing GLB: {glb_file}")
            if not usdz_exists:
                print(f"    - Missing USDZ: {usdz_file} (Required for iOS AR)")
print("-" * 20)


# --- Routes ---
@app.route('/')
def index():
    """
    Renders the main page displaying product cards with 3D models.
    Passes the validated list of products to the template.
    """
    # Pass the list of valid products to the template context
    return render_template('index.html', products=valid_products)

# --- Run the Application ---
if __name__ == '__main__':
    port = 5000
    local_ip = get_local_ip()

    print(f"Flask server starting...")
    print(f"View in browser: http://127.0.0.1:{port} or http://localhost:{port}")
    if local_ip:
        print(f"View on local network (for mobile testing): http://{local_ip}:{port}")
    else:
        print("Could not automatically detect local IP address.")
        print(f"To view on your local network (for mobile testing), find your IPv4 address using 'ipconfig' in cmd.")
        print(f"Then open http://<YOUR_IPv4_ADDRESS>:{port} in your mobile browser.")

    print("-" * 20)
    print("Ensure model files (.glb AND .usdz for AR) listed in 'products_data'")
    print("are placed inside the 'static/models/' directory.")
    print("-" * 20)

    app.run(debug=True, host='0.0.0.0', port=port)
