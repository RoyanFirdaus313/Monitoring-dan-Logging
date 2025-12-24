import time
import psutil
from prometheus_client import start_http_server, Gauge, Counter

# Inisialisasi Metrik
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')
CPU_USAGE = Gauge('system_cpu_usage', 'Persentase Penggunaan CPU')
RAM_USAGE = Gauge('system_ram_usage', 'Persentase Penggunaan RAM')
MODEL_ACCURACY = Gauge('model_accuracy_score', 'Skor Akurasi Model Terakhir')

def track_metrics():
    while True:
        CPU_USAGE.set(psutil.cpu_percent())
        RAM_USAGE.set(psutil.virtual_memory().percent)
        # Simulasi metrik lainnya
        time.sleep(5)

if __name__ == '__main__':
    start_http_server(8000)
    print("Exporter berjalan di port 8000")
    track_metrics()
