import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="NDSS Dashboard", layout="centered")

model = joblib.load("threat_model.pkl")

if "page" not in st.session_state:
    st.session_state.page = 1

# ---------- STYLE ----------
st.markdown("""
<style>
.title{
    text-align:center;
    font-size:34px;
    font-weight:bold;
    color:#1f4e79;
}

.box{
    border:1px solid #d0d0d0;
    border-radius:10px;
    padding:25px;
    margin-top:15px;
    background-color:#f8f9fa;
}

.result-safe{
    border-left:6px solid green;
    padding:15px;
    background:#eef9f1;
    border-radius:6px;
}

.result-danger{
    border-left:6px solid red;
    padding:15px;
    background:#fdeaea;
    border-radius:6px;
}

.section-title{
    font-weight:bold;
    font-size:20px;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SLIDE 1 ----------
if st.session_state.page == 1:

    st.markdown('<div class="title">Network Decision Support System</div>', unsafe_allow_html=True)

    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Traffic Input Parameters</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        size = st.number_input("Packet Size (Bytes)", min_value=0)

    with col2:
        count = st.number_input("Packet Count", min_value=0)

    entropy = st.slider("Entropy Level",0.0,1.0,0.5)

    st.write("These inputs represent network traffic behaviour used for AI-based threat detection.")

    if st.button("Run NDSS Analysis"):
        st.session_state.size = size
        st.session_state.count = count
        st.session_state.entropy = entropy
        st.session_state.page = 2
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- SLIDE 2 ----------
if st.session_state.page == 2:

    size = st.session_state.size
    count = st.session_state.count
    entropy = st.session_state.entropy

    features = [0]*41
    features[4] = size
    features[22] = count
    features[30] = entropy

    prediction = model.predict(np.array(features).reshape(1,-1))
    is_threat = prediction[0] == 1 or count > 400 or entropy > 0.8

    st.markdown('<div class="title">NDSS Decision Report</div>', unsafe_allow_html=True)

    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Traffic Analysis</div>', unsafe_allow_html=True)

    if is_threat:

        st.markdown('<div class="result-danger">⚠ Threat Detected (Malicious Traffic)</div>', unsafe_allow_html=True)

        st.write("• Entropy level suggests automated abnormal behaviour.")
        st.write("• Packet frequency resembles DoS or probing activity.")
        st.write("• Recommended Action: Block suspicious IP and monitor traffic.")

    else:

        st.markdown('<div class="result-safe">✔ Traffic Classified as Safe</div>', unsafe_allow_html=True)

        st.write("• Traffic pattern matches normal user behaviour.")
        st.write("• No malicious sequence detected.")
        st.write("• System Action: Allow access and continue monitoring.")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Run New Analysis"):
        st.session_state.page = 1
        st.rerun()





