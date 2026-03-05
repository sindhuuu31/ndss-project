import streamlit as st
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="NDSS System", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>

body{
background:#1f9e9a;
}

.title{
text-align:center;
font-size:45px;
font-weight:bold;
color:#5ff1e6;
}

.panel{
background:#1f2b38;
padding:40px;
border-radius:20px;
box-shadow:0px 0px 10px black;
}

label{
font-weight:bold;
font-size:18px;
color:white;
}

.result-safe{
font-size:38px;
font-weight:bold;
color:#00ff9d;
text-align:center;
}

.result-malicious{
font-size:38px;
font-weight:bold;
color:#ff4d6d;
text-align:center;
}

.analysis{
font-size:18px;
color:white;
padding:20px;
}

</style>
""", unsafe_allow_html=True)

# ---------- RANDOM FOREST MODEL ----------
X = np.array([
[200,50,0.2],
[300,60,0.3],
[400,80,0.4],
[1500,700,0.9],
[1700,900,0.85],
[1200,600,0.8]
])

y = np.array([0,0,0,1,1,1])

model = RandomForestClassifier()
model.fit(X,y)

# ---------- SESSION ----------
if "page" not in st.session_state:
    st.session_state.page = 1


# ---------- SLIDE 1 : INPUT PANEL ----------
if st.session_state.page == 1:

    st.markdown('<div class="title">NDSS Security Input</div>', unsafe_allow_html=True)
    st.write("")

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    packet_size = st.number_input("Packet Size", min_value=1)
    packet_count = st.number_input("Packet Count", min_value=1)
    entropy = st.slider("Entropy Level",0.0,1.0,0.5)

    st.write("")

    if st.button("Run Analysis"):
        st.session_state.packet_size = packet_size
        st.session_state.packet_count = packet_count
        st.session_state.entropy = entropy
        st.session_state.page = 2
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- SLIDE 2 : DECISION ENGINE ----------
elif st.session_state.page == 2:

    st.markdown('<div class="title">NDSS Decision Engine</div>', unsafe_allow_html=True)

    size = st.session_state.packet_size
    count = st.session_state.packet_count
    entropy = st.session_state.entropy

    prediction = model.predict([[size,count,entropy]])[0]

    if prediction == 1:
        st.markdown('<div class="result-malicious">MALICIOUS TRAFFIC DETECTED</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-safe">SAFE NETWORK TRAFFIC</div>', unsafe_allow_html=True)

    st.write("")

    if st.button("View AI Analysis"):
        st.session_state.page = 3
        st.rerun()


# ---------- SLIDE 3 : AI ANALYSIS ----------
elif st.session_state.page == 3:

    st.markdown('<div class="title">AI Threat Analysis</div>', unsafe_allow_html=True)

    size = st.session_state.packet_size
    count = st.session_state.packet_count
    entropy = st.session_state.entropy

    prediction = model.predict([[size,count,entropy]])[0]

    if prediction == 1:

        explanation = f"""
• Packet Count ({count}) is abnormally high.

• Entropy Level ({entropy}) indicates unpredictable packet behavior.

• Packet Size ({size}) combined with high frequency suggests automated attack traffic.

The Random Forest model therefore predicts **Malicious Activity**.
"""

    else:

        explanation = f"""
• Packet Count ({count}) is within normal limits.

• Entropy Level ({entropy}) indicates stable network traffic.

• Packet Size ({size}) does not show abnormal transmission pattern.

The Random Forest model therefore predicts **Safe Network Behaviour**.
"""

    st.markdown(f'<div class="analysis">{explanation}</div>', unsafe_allow_html=True)

    st.write("")

    if st.button("Restart System"):
        st.session_state.page = 1
        st.rerun()
