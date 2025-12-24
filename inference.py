# inference.py (sekaligus sebagai exporter)
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Counter, Histogram, Gauge
import time

app = Flask(__name__)

# --- METRIKS MONITORING (Minimal 10 untuk Advanced) ---
PREDICTION_COUNTER = Counter('model_prediction_total', 'Total predictions made')
LATENCY_HISTOGRAM = Histogram('model_prediction_latency_seconds', 'Time taken for prediction')
ACCURACY_GAUGE = Gauge('model_last_accuracy_score', 'Accuracy of the last batch')
ERROR_COUNTER = Counter('model_prediction_errors_total', 'Total failed predictions')
# ... tambahkan metriks lain seperti memory_usage, request_size, dll.

model = joblib.load("model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()
    try:
        data = request.get_json()
        df = pd.DataFrame(data)
        
        prediction = model.predict(df)
        
        # Update Metriks
        PREDICTION_COUNTER.inc()
        LATENCY_HISTOGRAM.observe(time.time() - start_time)
        
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        ERROR_COUNTER.inc()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Jalankan exporter di port 8000
    start_http_server(8000)
    # Jalankan API di port 5000
    app.run(host='0.0.0.0', port=5000)
