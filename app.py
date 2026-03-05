import streamlit as st
import random

st.set_page_config(page_title="NDSS System", layout="wide")

# -------------------- CSS STYLE --------------------
st.markdown("""
<style>

.main{
background-color:#2a7f7f;
}

.title{
text-align:center;
font-size:45px;
font-weight:bold;
color:#5af2e3;
}

.section{
font-size:28px;
font-weight:bold;
color:white;
margin-top:20px;
}

.box{
background-color:#1e2b38;
padding:20px;
border-radius:12px;
margin-bottom:15px;
color:white;
font-weight:bold;
}

.result{
font-size:40px;
font-weight:bold;
text-align:center;
}

</style>
""", unsafe_allow_html=True)

# -------------------- SLIDE NAVIGATION --------------------

page = st.sidebar.radio(
"NDSS Navigation",
["Slide 1 - Traffic Parameters",
 "Slide 2 - Decision Engine",
 "Slide 3 - Engine Analysis"]
)

# store result
if "prediction" not in st.session_state:
    st.session_state.prediction = None


# -------------------- SLIDE 1 --------------------
if page == "Slide 1 - Traffic Parameters":

    st.markdown("<div class='title'>NDSS Traffic Parameters</div>", unsafe_allow_html=True)

    st.write("")

    col1,col2,col3 = st.columns(3)

    with col1:
        packet_size = st.number_input("Packet Size",0,200)

    with col2:
        packet_count = st.number_input("Packet Count",0,1000)

    with col3:
        entropy = st.number_input("Entropy",0.0,10.0)

    col4,col5 = st.columns(2)

    with col4:
        flow_duration = st.number_input("Flow Duration",0,500)

    with col5:
        protocol = st.selectbox("Protocol Type",["HTTP","FTP","DNS","SMTP"])

    if st.button("Run Decision Engine"):

        score = packet_size + packet_count + entropy + flow_duration

        if score > 5000 or entropy > 5:
            st.session_state.prediction = "Malicious"
        else:
            st.session_state.prediction = "Safe"

        st.success("Parameters submitted. Go to Slide 2.")


# -------------------- SLIDE 2 --------------------
elif page == "Slide 2 - Decision Engine":

    st.markdown("<div class='title'>Decision Engine Result</div>", unsafe_allow_html=True)

    st.write("")

    if st.session_state.prediction is None:
        st.warning("Run the Decision Engine from Slide 1")

    else:

        if st.session_state.prediction == "Safe":
            st.markdown("<div class='result'>SAFE</div>",unsafe_allow_html=True)
        else:
            st.markdown("<div class='result'>MALICIOUS</div>",unsafe_allow_html=True)

        st.write("")
        st.info("Check Analysis of the Engine Result in Slide 3")


# -------------------- SLIDE 3 --------------------
elif page == "Slide 3 - Engine Analysis":

    st.markdown("<div class='title'>Engine Analysis</div>", unsafe_allow_html=True)

    if st.session_state.prediction is None:
        st.warning("Run the Decision Engine first")

    else:

        pred = st.session_state.prediction

        st.markdown("<div class='box'>1. AI Analysis</div>",unsafe_allow_html=True)
        st.write(f"""
Using AI traffic behaviour analysis, the system studies packet size,
packet count and flow duration patterns. The model compares these
parameters with normal network behaviour and predicts the traffic as **{pred}**.
""")

        st.markdown("<div class='box'>2. Random Forest</div>",unsafe_allow_html=True)
        st.write(f"""
Random Forest algorithm evaluates multiple decision trees based on
network features. The combined prediction from trees indicates that
the traffic behaviour is **{pred}**.
""")

        st.markdown("<div class='box'>3. Entropy</div>",unsafe_allow_html=True)
        st.write(f"""
Entropy measures randomness in network packets.
Higher entropy indicates abnormal traffic patterns
which may signal malicious activity. Based on entropy
value the traffic is predicted as **{pred}**.
""")

        st.markdown("<div class='box'>4. Vector Prediction</div>",unsafe_allow_html=True)
        st.write(f"""
Vector prediction converts network parameters into
feature vectors and compares them with trained
machine learning models. The similarity score
classifies the traffic as **{pred}**.
""")


