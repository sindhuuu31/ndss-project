import streamlit as st

# Page settings
st.set_page_config(page_title="NDSS Project", layout="wide")

# Title
st.title("Network Decision Support System (NDSS)")
st.markdown("### AI Based Network Monitoring & Decision Support")

# ---- SLIDE 1 ----
st.header("Overview")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **Project Name**
    
    Network Decision Support System
    
    **Purpose**
    
    Helps administrators analyze network traffic and take better decisions.
    """)

with col2:
    st.success("""
    **Technology Used**
    
    - Python
    - Machine Learning
    - Network Analysis
    - Streamlit Deployment
    """)

# ---- SLIDE 2 ----
st.header("Project Modules")

col3, col4, col5 = st.columns(3)

with col3:
    st.warning("""
    **Data Collection**
    
    Collects network traffic data from users.
    """)

with col4:
    st.warning("""
    **Analysis Engine**
    
    Uses algorithms to analyze patterns and risks.
    """)

with col5:
    st.warning("""
    **Decision Support**
    
    Suggests actions for administrators.
    """)

# ---- INPUT SECTION ----
st.header("Network Decision Input")

traffic = st.selectbox(
    "Select Network Traffic Type",
    ["Normal Traffic", "Suspicious Traffic", "High Load Traffic"]
)

if st.button("Analyze Network"):
    if traffic == "Normal Traffic":
        st.success("Network is stable. No action required.")
    elif traffic == "Suspicious Traffic":
        st.error("Possible security risk detected!")
    else:
        st.warning("High network load. Optimize bandwidth.")
    





