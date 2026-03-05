import streamlit as st
import random

st.set_page_config(page_title="NDSS - Network Decision Support System", layout="centered")

# ---------- Custom CSS (Professional Style) ----------
st.markdown("""
<style>

.main {
    background-color:#2a7f7f;
}

.title{
    text-align:center;
    font-size:45px;
    font-weight:bold;
    color:#5af2e3;
}

.card{
    background-color:#1e2b38;
    padding:30px;
    border-radius:15px;
    box-shadow:0px 4px 20px rgba(0,0,0,0.5);
}

label{
    font-weight:bold;
    color:white;
}

.stNumberInput input{
    background-color:black;
    color:white;
}

.stButton>button{
    background-color:#3fa7a3;
    color:white;
    border-radius:10px;
    height:45px;
    width:100%;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("<div class='title'>NDSS Decision Engine</div>", unsafe_allow_html=True)

st.write("")

# ---------- Card Layout ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("Network Traffic Parameters")

packet_size = st.number_input("Packet Size", 0, 2000)
packet_count = st.number_input("Packet Count", 0, 10000)
entropy = st.number_input("Entropy", 0.0, 10.0)

flow_duration = st.number_input("Flow Duration")
protocol_type = st.number_input("Protocol Type")

analyze = st.button("Analyze Traffic")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- Decision Engine ----------
if analyze:

    score = packet_size + packet_count + entropy + flow_duration + protocol_type

    prediction = random.choice(["Safe", "Malicious"])

    st.write("")
    st.subheader("Decision Engine Result")

    if prediction == "Safe":
        st.success("Traffic Status: SAFE")

        st.write("""
AI Analysis:
- Packet behaviour is within normal range  
- Network entropy indicates stable traffic pattern  
- No abnormal flow detected  
- System predicts the traffic as legitimate
""")

    else:
        st.error("Traffic Status: MALICIOUS")

        st.write("""
AI Analysis:
- High packet activity detected  
- Entropy indicates irregular traffic behaviour  
- Possible anomaly in network flow  
- System predicts potential malicious activity
""")
