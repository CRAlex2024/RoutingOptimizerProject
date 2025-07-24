import streamlit as st
import joblib

# Load model
model = joblib.load('notebooks/models/protocol_classifier.joblib')

st.title("🌐 Network Protocol Advisor")
st.markdown("""
Get data-driven routing protocol recommendations  
*Based on your trained machine learning model*
""")

# Metrics input
latency = st.slider("Latency (ms)", 5, 200, 50)
jitter = st.slider("Jitter (ms)", 1, 100, 20)
packet_loss = st.slider("Packet Loss (%)", 0.1, 5.0, 0.5)
convergence = st.slider("Convergence Time (s)", 1, 60, 20)

# Constraints
with st.expander("⚙️ Advanced Settings"):
    cisco_only = st.checkbox("Cisco-only Network")
    large_network = st.checkbox("Large Network (>15 routers)")
    admin_pref = st.selectbox("Admin Preference", ["None", "RIP", "OSPF", "EIGRP"])

# Recommendation logic
if st.button("Get Recommendation"):
    input_data = [[latency, jitter, packet_loss, convergence]]
    predicted = model.predict(input_data)[0]

    viable = []
    for proto in ['RIP', 'OSPF', 'EIGRP']:
        if large_network and proto == 'RIP': continue
        if cisco_only and proto == 'EIGRP':
            viable.append(proto)
        elif not cisco_only:
            viable.append(proto)

    final = admin_pref if admin_pref != "None" and admin_pref in viable else predicted

    # Enhanced output
    st.success(f"Recommended Protocol: **{final}**")
    with st.expander("📊 Decision Details"):
        st.write(f"- ML Model Prediction: {predicted}")
        st.write(f"- Viable Options: {', '.join(viable)}")
        st.write(
            f"- Active Constraints: {'Cisco-only ' if cisco_only else ''}{'Large-network ' if large_network else ''}")