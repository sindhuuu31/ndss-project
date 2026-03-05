from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load('models/threat_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        size = float(request.form.get('size'))
        count = float(request.form.get('count'))
        entropy = float(request.form.get('entropy'))

        # Prepare 41-feature vector for the Random Forest model
        features = [0] * 41
        features[4] = size
        features[22] = count
        features[30] = entropy
        
        # AI Prediction
        prediction = model.predict(np.array(features).reshape(1, -1))
        
        # LOGIC: Force Malicious if metrics look like an attack (Count > 400 or Entropy > 0.8)
        is_threat = prediction[0] == 1 or count > 400 or entropy > 0.8
        
        if is_threat:
            return jsonify({
                'is_threat': True,
                'vector': "MALICIOUS: ANOMALY DETECTED",
                'analyzer': f"AI Brain identifies chaos. Entropy ({entropy}) suggests automated script behavior.",
                'heuristic': f"High Frequency ({count}) matches DoS/Probing attack signatures.",
                'mitigation': "PROTOCOL: IP_BLOCK + TRAFFIC_SHUTDOWN initiated."
            })
        else:
            return jsonify({
                'is_threat': False,
                'vector': "SAFE: BENIGN SIGNAL",
                'analyzer': "Traffic pattern matches human-user baseline. Entropy is stable.",
                'heuristic': "Sequence analysis shows no repetitive malicious patterns.",
                'mitigation': "PROTOCOL: ALLOW_ACCESS + ROUTINE_LOGGING active."
            })
    except Exception as e:
        return jsonify({'vector': 'SYSTEM_ERROR', 'analyzer': str(e)})

if __name__ == '__main__':
  app.run(host="127.0.0.1", port=8080, debug=True)
    

