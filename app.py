import streamlit as st

# Page configuration
st.set_page_config(
    page_title="NDSS - Network Decision Support System",
    layout="wide"
)

# Sidebar
st.sidebar.title("NDSS Dashboard")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "System Overview", "Network Analysis"]
)

# HOME PAGE (Slide 1)
if page == "Home":
    st.title("Network Decision Support System")
    st.subheader("AI Based Network Monitoring Platform")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Project Description")
        st.info(
            """
            The **Network Decision Support System (NDSS)** helps administrators
            monitor network traffic and make intelligent decisions
            based on data analysis.
            """
        )

    with col2:
        st.markdown("### Technologies Used")
        st.success(
            """
            • Python  
            • Machine Learning  
            • Network Traffic Analysis  
            • Streamlit Web Interface
            """
        )

# SYSTEM OVERVIEW (Slide 2)
elif page == "System Overview":

    st.title("System Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.warning(
            """
            ### Data Collection
            Collects network traffic data from users and devices.
            """
        )

    with col2:
        st.warning(
            """
            ### Data Processing
            Analyzes network packets and behavior patterns.
            """
        )

    with col3:
        st.warning(
            """
            ### Decision Support
            Provides suggestions for network administrators.
            """
        )

# ANALYSIS PAGE
elif page == "Network Analysis":

    st.title("Network Traffic Analysis")

    traffic = st.selectbox(
        "Select Network Traffic Type",
        [
            "Normal Traffic",
            "Suspicious Traffic",
            "High Network Load"
        ]
    )

    if st.button("Analyze Network"):

        if traffic == "Normal Traffic":
            st.success("Network is operating normally.")

        elif traffic == "Suspicious Traffic":
            st.error("Suspicious activity detected. Check network security.")

        elif traffic == "High Network Load":
            st.warning("Network traffic is high. Consider bandwidth optimization.")
    






