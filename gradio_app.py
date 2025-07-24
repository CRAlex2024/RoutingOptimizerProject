import gradio as gr
import pandas as pd
import joblib

# Load your trained model
model = joblib.load('notebooks/models/protocol_classifier.joblib')


def gradio_recommend(latency, jitter, packet_loss, convergence,
                     cisco_only, large_network, admin_preference):
    """Adapted recommendation function for Gradio"""
    input_data = [[latency, jitter, packet_loss, convergence]]
    predicted = model.predict(input_data)[0]

    # Constraint handling (same logic as before)
    viable = []
    for proto in ['RIP', 'OSPF', 'EIGRP']:
        if large_network and proto == 'RIP': continue
        if cisco_only and proto == 'EIGRP':
            viable.append(proto)
        elif not cisco_only:
            viable.append(proto)

    final = admin_preference if admin_preference != 'None' and admin_preference in viable else predicted
    note = "(Admin override)" if admin_preference != 'None' else ""

    return f"Recommended Protocol: {final} {note}\nViable Options: {', '.join(viable)}"


# Create Gradio interface
demo = gr.Interface(
    fn=gradio_recommend,
    inputs=[
        gr.Slider(5, 200, value=50, label="Latency (ms)"),
        gr.Slider(1, 100, value=20, label="Jitter (ms)"),
        gr.Slider(0.1, 5.0, value=0.5, label="Packet Loss (%)"),
        gr.Slider(1, 60, value=20, label="Convergence (s)"),
        gr.Checkbox(label="Cisco-only Network"),
        gr.Checkbox(label="Large Network (>15 routers)"),
        gr.Dropdown(["None", "RIP", "OSPF", "EIGRP"], label="Admin Preference")
    ],
    outputs="text",
    title="🌐 Network Protocol Advisor (Gradio)",
    description="Get optimal routing protocol recommendations based on network metrics"
)

demo.launch()  # Runs locally or generates shareable link