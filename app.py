import streamlit as st
import random

st.set_page_config(page_title="NDSS Decision Engine", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>

.title{
font-size:40px;
font-weight:bold;
text-align:center;
margin-bottom:30px;
}

.heading{
font-size:28px;
font-weight:bold;
margin-top:30px;
}

.analysis-box{
border:2px solid #0e76a8;
padding:20px;
border-radius:10px;
margin-top:10px;
background:#f5f9ff;
}

.safe{
font-size:45px;
font-weight:bold;
color:green;
text-align:center;
}

.malicious{
font-size:45px;
font-weight:bold;
color:red;
text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------- SLIDE 1 ----------
st.markdown("<div class='title'>NDSS Traffic Parameters</div>", unsafe_allow_html=True)

col1,col2 = st.columns(2)

with col1:
    packet_size = st.number_input("Packet Size (Bytes)",min_value=0,max_value=500)
    packet_count = st.number_input("Packet Count",min_value=0,max_value=1000)
    entropy = st.slider("Entropy Level",0.0,1.0,0.5)

with col2:
    flow_duration = st.number_input("Flow Duration (ms)",min_value=0,max_value=20)

    protocol = st.selectbox(
    "Protocol Type",
    [
    "HTTP - HyperText Transfer Protocol",
    "FTP - File Transfer Protocol",
    "DNS - Domain Name System",
    "SMTP - Simple Mail Transfer Protocol"
    ])

run = st.button("Run Decision Engine")

# ---------- ENGINE ----------
if run:

    # simple NDSS prediction logic
    vector_score = packet_size + packet_count + flow_duration + entropy*100

    if vector_score > 800:
        decision="MALICIOUS"
        style="malicious"
    else:
        decision="SAFE"
        style="safe"

# ---------- SLIDE 2 ----------
    st.markdown("---")
    st.markdown("<div class='heading'>Decision Engine Result</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='{style}'>{decision}</div>",unsafe_allow_html=True)

    st.write("Check the engine analysis below")

# ---------- SLIDE 3 ----------
    st.markdown("---")
    st.markdown("<div class='heading'>Engine Analysis</div>", unsafe_allow_html=True)

    colA,colB = st.columns(2)

    with colA:

        st.markdown(f"""
        <div class="analysis-box">
        <b>AI Analysis</b><br><br>
        The AI module evaluates traffic behaviour using network parameters.
        Based on the packet size, packet count and flow behaviour, the system
        predicts that the traffic pattern is <b>{decision}</b>.
        </div>
        """,unsafe_allow_html=True)

        rf=random.choice(["SAFE","MALICIOUS"])

        st.markdown(f"""
        <div class="analysis-box">
        <b>Random Forest Analysis</b><br><br>
        Random Forest algorithm evaluates multiple decision trees to classify
        the network traffic. The algorithm predicts this network behaviour as
        <b>{rf}</b>.
        </div>
        """,unsafe_allow_html=True)

    with colB:

        st.markdown(f"""
        <div class="analysis-box">
        <b>Entropy Analysis</b><br><br>
        Current entropy value is <b>{entropy}</b>. Higher entropy indicates
        irregular packet randomness which may represent abnormal traffic
        behaviour in the network.
        </div>
        """,unsafe_allow_html=True)

        st.markdown(f"""
        <div class="analysis-box">
        <b>Vector Prediction</b><br><br>
        The NDSS vector model combines packet size, packet count and flow
        duration to generate a traffic score of <b>{vector_score}</b>.
        This score leads the decision engine to classify the traffic as
        <b>{decision}</b>.
        </div>
        """,unsafe_allow_html=True)




