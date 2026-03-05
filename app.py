import streamlit as st
import joblib
import numpy as np

st.title("NDSS - Network Decision Support System")

model = joblib.load("threat_model.pkl")

size = st.number_input("Packet Size")
count = st.number_input("Packet Count")
entropy = st.slider("Entropy Level", 0.0, 1.0, 0.5)

if st.button("Run Analyzer"):

    features = [0] * 41
    features[4] = size
    features[22] = count
    features[30] = entropy

    prediction = model.predict(np.array(features).reshape(1, -1))

    is_threat = prediction[0] == 1 or count > 400 or entropy > 0.8

    if is_threat:
        st.error("MALICIOUS: ANOMALY DETECTED")
        st.write("AI Brain identifies suspicious traffic pattern.")
        st.write("Recommended Mitigation: IP Block + Traffic Shutdown")
    else:
        st.success("SAFE: BENIGN SIGNAL")
        st.write("Traffic pattern matches normal behaviour.")
    


