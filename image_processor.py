from PIL import Image
import sys
import os
from flask import Flask, request, render_template_string, redirect, url_for, flash
from werkzeug.utils import secure_filename

# --- Flask App Setup ---
app = Flask(__name__)
# Secret key needed for flashing messages
app.secret_key = os.urandom(24) # Replace with a strong, static key in production

# Configure upload folder (relative to the script location)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Optional: Limit allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- HTML Template ---
HTML_TEMPLATE = """
<!doctype html>
<title>Upload new File</title>
<h1>Upload an Image</h1>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul class=flashes>
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
"""

def process_image(image_path):
    """
    Memuat dan memproses gambar dari path yang diberikan.
    Returns True on success, False on failure.
    """
    try:
        # Buka file gambar
        img = Image.open(image_path)

        # Tampilkan beberapa informasi dasar tentang gambar (opsional) - logs to server console
        print(f"Gambar berhasil dimuat: {image_path}")
        print(f"Format: {img.format}, Ukuran: {img.size}, Mode: {img.mode}")

        # --- Placeholder untuk pemrosesan gambar ---
        # Tambahkan logika pemrosesan gambar Anda di sini
        # Contoh: img.show() # Might not work well in a server environment
        # Contoh: processed_img = img.convert('L')
        # Contoh: processed_img.save(os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + os.path.basename(image_path)))
        # -----------------------------------------

        print("Pemrosesan gambar selesai (placeholder).")
        return True # Indicate success

    except FileNotFoundError:
        print(f"Error: File gambar tidak ditemukan di '{image_path}'", file=sys.stderr)
        return False # Indicate failure
    except Exception as e:
        print(f"Error saat memproses gambar: {e}", file=sys.stderr)
        return False # Indicate failure

# --- Flask Routes ---
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(save_path)
                flash(f'File "{filename}" uploaded successfully.')
                # Process the uploaded image
                if process_image(save_path):
                    flash(f'Image "{filename}" processed (see server console).')
                    # Optionally, you could display the processed image or results here
                else:
                    flash(f'Error processing image "{filename}".')
                return redirect(url_for('upload_file')) # Redirect back to the upload form
            except Exception as e:
                flash(f'Error saving or processing file: {e}')
                return redirect(request.url)
        else:
            flash('File type not allowed')
            return redirect(request.url)

    # For GET requests, just render the template
    return render_template_string(HTML_TEMPLATE)

# --- Run the App ---
if __name__ == "__main__":
    # Remove the old command-line logic
    # input_image_path = None
    # ... (rest of the old CLI code removed) ...

    # Run the Flask development server
    # Accessible at http://127.0.0.1:5000 by default
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print("Starting Flask server...")
    app.run(debug=True) # debug=True enables auto-reloading and error pages

