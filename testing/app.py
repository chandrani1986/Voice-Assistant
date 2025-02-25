import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure file upload settings
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

# Define a model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image = db.Column(db.String(200), nullable=True)  # Store image path

# Create database tables
with app.app_context():
    db.create_all()

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        image_file = request.files['image']  # Get the uploaded image

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)  # Secure filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)  # Save the image
            
            # Save to the database
            new_user = User(name=name, email=email, image=filename)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('index'))  # Redirect after submission

    return "Error uploading file", 400
if __name__ == "__main__":
    app.run(debug=True)