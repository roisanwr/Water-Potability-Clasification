import numpy as np
import joblib
from flask import Flask, request, render_template_string

# --- 1. SETUP APLIKASI ---
app = Flask(__name__)

# Load Model dan Scaler yang sudah kamu simpan sebelumnya
# Pastikan file .pkl ada di folder yang sama dengan app.py
try:
    model = joblib.load('knn_water_model.pkl')
    scaler = joblib.load('scaler_water.pkl')
    print("✅ Model dan Scaler berhasil dimuat!")
except FileNotFoundError:
    print("❌ ERROR: File model (.pkl) tidak ditemukan.")
    print("Pastikan kamu sudah menjalankan notebook training dan mendownload filenya.")
    exit()

# --- 2. TEMPLATE HTML (Tampilan Website) ---
# Kita masukkan HTML langsung di sini agar jadi 1 file saja
html_template = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cek Kualitas Air (Water Potability)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f0f8ff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .container { max-width: 800px; margin-top: 50px; margin-bottom: 50px; }
        .card { border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .header-title { color: #007bff; font-weight: bold; }
        .variable-info { font-size: 0.9em; color: #555; background: #e9ecef; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .result-box { margin-top: 20px; padding: 20px; border-radius: 10px; text-align: center; font-size: 1.5em; font-weight: bold; }
        .safe { background-color: #d4edda; color: #155724; border: 2px solid #c3e6cb; }
        .unsafe { background-color: #f8d7da; color: #721c24; border: 2px solid #f5c6cb; }
    </style>
</head>
<body>

<div class="container">
    <div class="card p-4">
        <h2 class="text-center header-title mb-4">💧 Cek Kualitas Air Minum</h2>

        <div class="variable-info">
            <h5>📚 Penjelasan Variabel:</h5>
            <ul>
                <li><strong>pH (0-14):</strong> Tingkat keasaman air. (Minum: 6.5 - 8.5)</li>
                <li><strong>Hardness:</strong> Kekerasan air (kandungan kalsium/magnesium).</li>
                <li><strong>Solids (TDS):</strong> Total padatan terlarut (mineral, garam, logam).</li>
                <li><strong>Chloramines:</strong> Disinfektan klorin untuk membunuh bakteri.</li>
                <li><strong>Sulfate:</strong> Senyawa sulfat (bisa dari mineral atau industri).</li>
                <li><strong>Conductivity:</strong> Daya hantar listrik air (terkait jumlah ion).</li>
                <li><strong>Organic Carbon:</strong> Kandungan karbon organik (sisa makhluk hidup).</li>
                <li><strong>Trihalomethanes:</strong> Zat kimia sampingan dari klorinasi.</li>
                <li><strong>Turbidity:</strong> Kekeruhan air (kejernihan).</li>
            </ul>
        </div>

        <form action="/predict" method="POST">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label>pH (0 - 14)</label>
                    <input type="number" step="0.01" class="form-control" name="ph" placeholder="Contoh: 7.0" required min="0" max="14">
                </div>
                <div class="col-md-4 mb-3">
                    <label>Hardness (mg/L)</label>
                    <input type="number" step="0.01" class="form-control" name="Hardness" placeholder="Contoh: 200" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label>Solids / TDS (ppm)</label>
                    <input type="number" step="0.01" class="form-control" name="Solids" placeholder="Contoh: 20000" required>
                </div>
            </div>

            <div class="row">
                <div class="col-md-4 mb-3">
                    <label>Chloramines (ppm)</label>
                    <input type="number" step="0.01" class="form-control" name="Chloramines" placeholder="Contoh: 7.0" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label>Sulfate (mg/L)</label>
                    <input type="number" step="0.01" class="form-control" name="Sulfate" placeholder="Contoh: 330" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label>Conductivity (μS/cm)</label>
                    <input type="number" step="0.01" class="form-control" name="Conductivity" placeholder="Contoh: 400" required>
                </div>
            </div>

            <div class="row">
                <div class="col-md-4 mb-3">
                    <label>Organic Carbon (ppm)</label>
                    <input type="number" step="0.01" class="form-control" name="Organic_carbon" placeholder="Contoh: 15" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label>Trihalomethanes (μg/L)</label>
                    <input type="number" step="0.01" class="form-control" name="Trihalomethanes" placeholder="Contoh: 66" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label>Turbidity (NTU)</label>
                    <input type="number" step="0.01" class="form-control" name="Turbidity" placeholder="Contoh: 4.0" required>
                </div>
            </div>

            <button type="submit" class="btn btn-primary w-100 mt-3">🔍 Cek Kelayakan Air</button>
        </form>

        {% if prediction_text %}
        <div class="result-box {{ result_class }}">
            {{ prediction_text }}
        </div>
        <div class="text-center mt-2">
            <a href="/" class="btn btn-outline-secondary btn-sm">Reset</a>
        </div>
        {% endif %}

    </div>
</div>

</body>
</html>
"""

# --- 3. LOGIKA BACKEND ---
@app.route('/', methods=['GET'])
def index():
    return render_template_string(html_template)

@app.route('/predict', methods=['POST'])
def predict():
    # 1. Ambil data dari form HTML
    try:
        features = [
            float(request.form['ph']),
            float(request.form['Hardness']),
            float(request.form['Solids']),
            float(request.form['Chloramines']),
            float(request.form['Sulfate']),
            float(request.form['Conductivity']),
            float(request.form['Organic_carbon']),
            float(request.form['Trihalomethanes']),
            float(request.form['Turbidity'])
        ]
        
        # 2. Ubah jadi array numpy 2D
        final_features = [np.array(features)]
        
        # 3. Lakukan SCALING (Wajib untuk KNN!)
        # Kita pakai scaler yang sama dengan saat training
        final_features_scaled = scaler.transform(final_features)
        
        # 4. Prediksi dengan Model
        prediction = model.predict(final_features_scaled)
        
        # 5. Tentukan hasil output
        if prediction[0] == 1:
            result_text = "✅ Air ini LAYAK MINUM (Potable)"
            css_class = "safe"
        else:
            result_text = "⚠️ Air ini TIDAK LAYAK MINUM (Not Potable)"
            css_class = "unsafe"

        return render_template_string(html_template, prediction_text=result_text, result_class=css_class)

    except Exception as e:
        return render_template_string(html_template, prediction_text=f"Terjadi Kesalahan: {e}", result_class="unsafe")

# --- 4. JALANKAN APLIKASI ---
if __name__ == "__main__":
    app.run(debug=True)