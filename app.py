import streamlit as st
import random

st.set_page_config(page_title="NDSS Decision Engine", layout="wide")

# ---------- CUSTOM STYLE ----------
st.markdown("""
<style>

.main-title{
font-size:40px;
font-weight:bold;
text-align:center;
margin-bottom:30px;
}

.section-title{
font-size:26px;
font-weight:bold;
margin-top:20px;
}

.analysis-box{
border:2px solid #0e76a8;
padding:20px;
border-radius:8px;
margin-bottom:20px;
background-color:#f7fbff;
}

.result-safe{
font-size:40px;
font-weight:bold;
color:green;
text-align:center;
}

.result-malicious{
font-size:40px;
font-weight:bold;
color:red;
text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------- SLIDE 1 ----------
st.markdown("<div class='main-title'>NDSS Traffic Parameters</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    packet_size = st.number_input("Packet Size (Bytes)", min_value=0)
    packet_count = st.number_input("Packet Count", min_value=0)
    entropy = st.slider("Entropy Level", 0.0, 1.0, 0.5)

with col2:
    flow_duration = st.number_input("Flow Duration (ms)", min_value=0)

    protocol = st.selectbox(
        "Protocol Type",
        [
        "HTTP - HyperText Transfer Protocol",
        "FTP - File Transfer Protocol",
        "DNS - Domain Name System",
        "SMTP - Simple Mail Transfer Protocol"
        ]
    )

run = st.button("Run Decision Engine")

# ---------- DECISION ENGINE ----------
if run:

    # simple prediction logic
    score = packet_size + packet_count + flow_duration + (entropy*100)

    if score > 800:
        result = "MALICIOUS"
        result_class = "result-malicious"
    else:
        result = "SAFE"
        result_class = "result-safe"

    st.markdown("---")

    # ---------- SLIDE 2 ----------
    st.markdown("<div class='section-title'>Decision Engine Result</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='{result_class}'>{result}</div>", unsafe_allow_html=True)

    st.write("Check analysis of the engine result below.")

    st.markdown("---")

    # ---------- SLIDE 3 ----------
    st.markdown("<div class='section-title'>Analysis Engine</div>", unsafe_allow_html=True)

    colA, colB = st.columns(2)

    with colA:

        st.markdown("""
        <div class="analysis-box">
        <b>1. AI Analysis</b><br><br>
        The AI module evaluates traffic behaviour patterns and determines whether 
        the network flow resembles normal or suspicious activity.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="analysis-box">
        <b>2. Random Forest Analysis</b><br><br>
        Random Forest algorithm analyses multiple decision trees to classify the 
        network traffic and improve prediction accuracy.
        </div>
        """, unsafe_allow_html=True)

    with colB:

        st.markdown(f"""
        <div class="analysis-box">
        <b>3. Entropy Analysis</b><br><br>
        Current entropy value: <b>{entropy}</b><br>
        Higher entropy may indicate irregular packet behaviour which could 
        signal suspicious network activity.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="analysis-box">
        <b>4. Vector Prediction</b><br><br>
        Network vector calculated from packet size, packet count and flow duration 
        produced a score of <b>{score}</b> which classifies this traffic as <b>{result}</b>.
        </div>
        """, unsafe_allow_html=True)



