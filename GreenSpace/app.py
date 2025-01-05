from flask import Flask, render_template, jsonify, request
from esg_evaluation import ESGEvaluator
from optimization_engine import OptimizationEngine
from dashboard import create_dashboard
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

# Initialize components
esg_evaluator = ESGEvaluator()
optimization_engine = OptimizationEngine()
dashboard = create_dashboard(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/esg_scores')
def get_esg_scores():
    scores = esg_evaluator.get_sample_scores()
    return jsonify(scores)

@app.route('/api/optimized_portfolio')
def get_optimized_portfolio():
    portfolio = optimization_engine.optimize_sample_portfolio()
    return jsonify(portfolio)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Here you would typically process the file and update your data
        # For now, we'll just return a success message
        return jsonify({'message': 'File successfully uploaded and processed'}), 200
    return jsonify({'message': 'File type not allowed'}), 400

# Ensure the Dash app is properly registered with Flask
app = dashboard.server

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if __name__ == '__main__':
    app.run(debug=True)

