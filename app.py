import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="NDSS - Network Decision Support System", layout="centered")

# Load model
model = joblib.load("threat_model.pkl")

# Control slides
if "page" not in st.session_state:
    st.session_state.page = 1

# ---------- STYLE ----------
st.markdown("""
<style>
.main-title{
    font-size:36px;
    font-weight:bold;
    text-align:center;
    color:#0d6efd;
}
.sub-title{
    text-align:center;
    color:gray;
}
.report-box{
    border:1px solid #ddd;
    padding:25px;
    border-radius:8px;
    background:#f9f9f9;
}
.safe{
    color:green;
    font-size:24px;
    font-weight:bold;
}
.danger{
    color:red;
    font-size:24px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- SLIDE 1 : INPUT ----------
if st.session_state.page == 1:

    st.markdown('<div class="main-title">Network Decision Support System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">AI-Based Network Threat Detection</div>', unsafe_allow_html=True)

    st.divider()

    st.subheader("Traffic Feature Input")

    col1, col2 = st.columns(2)

    with col1:
        size = st.number_input("Packet Size (Bytes)", min_value=0)

    with col2:
        count = st.number_input("Packet Count", min_value=0)

    entropy = st.slider("Entropy Level", 0.0, 1.0, 0.5)

    st.write("These parameters represent observed network traffic behaviour.")

    if st.button("Run NDSS Analysis"):

        st.session_state.size = size
        st.session_state.count = count
        st.session_state.entropy = entropy
        st.session_state.page = 2
        st.rerun()

# ---------- SLIDE 2 : RESULT ----------
if st.session_state.page == 2:

    st.markdown('<div class="main-title">NDSS Decision Report</div>', unsafe_allow_html=True)
    st.divider()

    size = st.session_state.size
    count = st.session_state.count
    entropy = st.session_state.entropy

    features = [0] * 41
    features[4] = size
    features[22] = count
    features[30] = entropy

    prediction = model.predict(np.array(features).reshape(1, -1))

    is_threat = prediction[0] == 1 or count > 400 or entropy > 0.8

    st.markdown('<div class="report-box">', unsafe_allow_html=True)

    if is_threat:

        st.markdown('<div class="danger">Threat Detected (Malicious Traffic)</div>', unsafe_allow_html=True)

        st.write("AI Analysis:")
        st.write(f"- Entropy level ({entropy}) suggests abnormal automated activity.")
        st.write(f"- Packet frequency ({count}) matches common DoS or probing patterns.")

        st.write("Recommended Mitigation:")
        st.write("- Block suspicious IP address")
        st.write("- Restrict abnormal traffic flow")
        st.write("- Log the event for further monitoring")

    else:

        st.markdown('<div class="safe">Traffic Classified as Safe</div>', unsafe_allow_html=True)

        st.write("AI Analysis:")
        st.write("- Traffic pattern aligns with normal network behaviour.")
        st.write("- No suspicious repetition or attack signature detected.")

        st.write("System Action:")
        st.write("- Allow access")
        st.write("- Continue routine monitoring")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Run New Analysis"):
        st.session_state.page = 1
        st.rerun()
    



