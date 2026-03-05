import streamlit as st
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="NDSS", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>

body {
background-color:#0b0f19;
}

.title{
text-align:center;
font-size:38px;
font-weight:bold;
color:#00d2ff;
}

.panel{
background:rgba(255,255,255,0.05);
border:1px solid #1e293b;
padding:35px;
border-radius:10px;
}

.result-safe{
text-align:center;
font-size:40px;
font-weight:bold;
color:#00ff9d;
}

.result-malicious{
text-align:center;
font-size:40px;
font-weight:bold;
color:#ff0055;
}

.analysis{
margin-top:30px;
font-size:18px;
color:#cbd5f5;
text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------- RANDOM FOREST MODEL ----------
X = np.array([
[200,50,0.2],
[300,60,0.3],
[1500,800,0.9],
[1700,900,0.85],
[400,100,0.4],
[1200,700,0.8]
])

y = np.array([0,0,1,1,0,1])  # 0 = Safe, 1 = Malicious

model = RandomForestClassifier()
model.fit(X,y)

# ---------- SESSION ----------
if "page" not in st.session_state:
    st.session_state.page = 1


# ---------- PAGE 1 ----------
if st.session_state.page == 1:

    st.markdown('<div class="title">NDSS SECURITY INPUT PANEL</div>', unsafe_allow_html=True)
    st.write("")

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    packet_size = st.number_input("Packet Size (Bytes)", min_value=1)
    packet_count = st.number_input("Packet Count", min_value=1)
    entropy = st.slider("Entropy Level",0.0,1.0,0.5)

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    if st.button("RUN DECISION ENGINE"):

        st.session_state.packet_size = packet_size
        st.session_state.packet_count = packet_count
        st.session_state.entropy = entropy
        st.session_state.page = 2
        st.rerun()


# ---------- PAGE 2 ----------
if st.session_state.page == 2:

    st.markdown('<div class="title">NDSS DECISION ENGINE</div>', unsafe_allow_html=True)
    st.write("")

    size = st.session_state.packet_size
    count = st.session_state.packet_count
    entropy = st.session_state.entropy

    # Random Forest Prediction
    prediction = model.predict([[size,count,entropy]])[0]

    if prediction == 1:

        st.markdown(
        '<div class="result-malicious">MALICIOUS TRAFFIC DETECTED</div>',
        unsafe_allow_html=True
        )

        explanation = f"""
Random Forest analysis detected abnormal network behaviour.

• Packet Count ({count}) is unusually high indicating possible automated traffic.

• Entropy Level ({entropy}) suggests irregular packet randomness common in malicious scripts.

• Packet Size ({size}) combined with high traffic frequency increases attack probability.

Therefore, the system classifies this traffic as **MALICIOUS**.
"""

    else:

        st.markdown(
        '<div class="result-safe">SAFE NETWORK TRAFFIC</div>',
        unsafe_allow_html=True
        )

        explanation = f"""
Random Forest model predicts this traffic as normal network activity.

• Packet Count ({count}) remains within normal traffic limits.

• Entropy Level ({entropy}) indicates stable packet randomness.

• Packet Size ({size}) does not show abnormal transmission behaviour.

Therefore, the system classifies this traffic as **SAFE**.
"""

    st.markdown(f'<div class="analysis">{explanation}</div>', unsafe_allow_html=True)

    st.write("")
    st.write("")

    if st.button("Restart"):
        st.session_state.page = 1
        st.rerun()







