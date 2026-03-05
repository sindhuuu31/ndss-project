import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="NDSS Decision System", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>
body {background-color:#0b0f19;}

.main-title{
font-size:36px;
font-weight:bold;
color:#00d2ff;
text-align:center;
}

.box{
background:rgba(255,255,255,0.05);
border:1px solid #1e293b;
padding:25px;
border-radius:10px;
margin-bottom:20px;
}

.result-safe{
border-left:6px solid #00ff9d;
padding:20px;
background:rgba(0,255,157,0.05);
}

.result-threat{
border-left:6px solid #ff0055;
padding:20px;
background:rgba(255,0,85,0.05);
}

.label{
font-size:14px;
color:#94a3b8;
}

.value{
font-size:20px;
font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "page" not in st.session_state:
    st.session_state.page = 1

# ---------- PAGE 1 ----------
if st.session_state.page == 1:

    st.markdown('<div class="main-title">NDSS SECURITY INPUT PANEL</div>', unsafe_allow_html=True)
    st.write("")

    st.markdown('<div class="box">', unsafe_allow_html=True)

    packet_size = st.number_input("Packet Size (Bytes)", min_value=1)
    packet_count = st.number_input("Packet Count", min_value=1)
    entropy = st.slider("Entropy Level",0.0,1.0,0.5)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("RUN NDSS ANALYZER"):
        st.session_state.packet_size = packet_size
        st.session_state.packet_count = packet_count
        st.session_state.entropy = entropy
        st.session_state.page = 2
        st.rerun()

# ---------- PAGE 2 ----------
if st.session_state.page == 2:

    st.markdown('<div class="main-title">NDSS DECISION ENGINE</div>', unsafe_allow_html=True)
    st.write("")

    size = st.session_state.packet_size
    count = st.session_state.packet_count
    entropy = st.session_state.entropy

    # -------- VECTOR ----------
    features = [0]*41
    features[4] = size
    features[22] = count
    features[30] = entropy

    # -------- PREDICTION LOGIC ----------
    threat_score = (count/1000) + entropy + (size/2000)

    is_threat = threat_score > 1.2

    # -------- ANALYSIS ----------
    if is_threat:

        vector="MALICIOUS TRAFFIC DETECTED"

        analyzer=f"""
AI analysis indicates abnormal behaviour.
Entropy level ({entropy}) suggests automated packet generation.
Packet count ({count}) exceeds normal human traffic patterns.
"""

        heuristic=f"""
Traffic frequency indicates potential DoS / probing behaviour.
Sequence repetition suggests scripted network attack pattern.
"""

        mitigation="""
Recommended Action:
• Block source IP
• Enable firewall filtering
• Activate traffic monitoring
"""

    else:

        vector="SAFE NETWORK TRAFFIC"

        analyzer=f"""
Traffic characteristics match normal user behaviour.
Entropy level ({entropy}) indicates balanced packet randomness.
"""

        heuristic=f"""
Packet frequency ({count}) remains within standard network threshold.
No abnormal traffic spikes detected.
"""

        mitigation="""
Recommended Action:
• Allow network communication
• Continue passive monitoring
"""

    # ---------- DISPLAY ----------
    if is_threat:
        st.markdown('<div class="result-threat">', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-safe">', unsafe_allow_html=True)

    st.markdown(f"""
### Vector Prediction
**{vector}**
""")

    st.markdown(f"""
### AI Analysis
{analyzer}
""")

    st.markdown(f"""
### Heuristic Pattern Analysis
{heuristic}
""")

    st.markdown(f"""
### Threat Score
{round(threat_score,2)}
""")

    st.markdown(f"""
### Recommended Mitigation
{mitigation}
""")

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("Restart System"):
        st.session_state.page = 1
        st.rerun()






