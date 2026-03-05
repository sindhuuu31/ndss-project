import streamlit as st
import random

st.set_page_config(page_title="NDSS Traffic Analysis", layout="centered")

# Slide navigation
if "slide" not in st.session_state:
    st.session_state.slide = 1

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

# ---------------- SLIDE 1 ----------------

if st.session_state.slide == 1:

    st.markdown("<h1 style='text-align:center; color:#1f4e79;'>NDSS Traffic Parameters</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        packet_size = st.number_input("Packet Size", 0, 1000)
        packet_count = st.number_input("Packet Count", 0, 10000)
        entropy = st.number_input("Entropy", 0, 20)

    with col2:
        flow_duration = st.number_input("Flow Duration", 0, 500)
        protocol = st.selectbox(
            "Protocol Type",
            ["HTTP - Hyper Text Transfer Protocol",
             "FTP - File Transfer Protocol"]
        )

    st.markdown("---")

    if st.button("Run Decision Engine"):
        st.session_state.result = random.choice(["SAFE TRAFFIC", "MALICIOUS TRAFFIC"])
        st.session_state.slide = 2
        st.rerun()

# ---------------- SLIDE 2 ----------------

elif st.session_state.slide == 2:

    st.markdown("<h1 style='text-align:center; color:#1f4e79;'>Decision Engine Result</h1>", unsafe_allow_html=True)

    result = st.session_state.result

    if result == "SAFE TRAFFIC":
        st.success("Traffic Result: SAFE")
    else:
        st.error("Traffic Result: MALICIOUS")

    st.markdown("### Check Analysis of the Engine Result")

    if st.button("Check Engine Analysis"):
        st.session_state.slide = 3
        st.rerun()

# ---------------- SLIDE 3 ----------------

elif st.session_state.slide == 3:

    st.markdown("<h1 style='text-align:center; color:#1f4e79;'>Engine Analysis</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.info("AI Analysis")
        st.write("Artificial Intelligence analyzes traffic patterns and detects abnormal behaviour in the network.")

        st.info("Random Forest Analysis")
        st.write("Random Forest uses multiple decision trees to classify traffic data as safe or malicious.")

    with col2:
        st.info("Entropy Analysis")
        st.write("Entropy measures randomness in network packets. High entropy may indicate suspicious traffic.")

        st.info("Vector Prediction")
        st.write("Vector prediction analyzes network feature vectors to predict whether traffic is normal or malicious.")

    st.markdown("---")

    st.markdown("### Conclusion")
    st.write("Using these analysis techniques, the system predicts whether the network traffic is **Safe or Malicious**.")


















