# NOTE: This is a FULL replacement app.py
# Paste this entire file and deploy on Streamlit Cloud

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Agentic Command Center",
    page_icon="🧠",
    layout="wide"
)

# ================================
# GLOBAL THEME (Dark, Futuristic)
# ================================
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        background-color: #020617;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    .glass {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 16px;
    }
    .glow {
        box-shadow: 0 0 20px rgba(139,92,246,0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================================
# SESSION STATE
# ================================
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "weights" not in st.session_state:
    st.session_state.weights = {
        "impact": 1.0,
        "urgency": 1.0,
        "effort": 1.0,
        "risk": 1.0
    }

# ================================
# UTILITY FUNCTION (SAFETY AWARE)
# ================================
def calculate_utility(task):
    w = st.session_state.weights
    base = (
        (w['impact'] * task['impact'] + w['urgency'] * task['urgency']) /
        (w['effort'] * task['effort'] + w['risk'] * task['risk'])
    )
    return round(base * 5 if task['critical'] else base * 0.4, 2)

# ================================
# SIDEBAR
# ================================
with st.sidebar:
    st.markdown("<div class='glass glow'>🧠 <b>Agentic Command Center</b></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Utility-Based • Constraint-Aware • Adaptive")

    st.markdown("### ⚙ Agent Weights")
    for k in st.session_state.weights:
        st.session_state.weights[k] = st.slider(
            k.capitalize(), 0.5, 2.0, st.session_state.weights[k], 0.1
        )

# ================================
# MAIN LAYOUT
# ================================
col_left, col_right = st.columns([1.2, 2.8])

# ================================
# TASK INPUT PANEL
# ================================
with col_left:
    st.markdown("<div class='glass'>➕ <b>Add New Task</b></div>", unsafe_allow_html=True)

    name = st.text_input("Task Name")
    category = st.selectbox("Category", ["Life", "Work", "Personal"])
    critical = st.toggle("Life Critical")

    urgency = st.slider("Urgency", 1, 10, 5)
    impact = st.slider("Impact", 1, 10, 5)
    effort = st.slider("Effort", 1, 10, 5)
    risk = st.slider("Risk", 1, 10, 5)

    if st.button("➕ Add Task", use_container_width=True):
        if name:
            st.session_state.tasks.append({
                "name": name,
                "category": category,
                "critical": critical,
                "urgency": urgency,
                "impact": impact,
                "effort": effort,
                "risk": risk,
                "time": datetime.now().strftime("%H:%M:%S")
            })
            st.success("Task added")

# ================================
# DECISION ENGINE + DASHBOARD
# ================================
with col_right:
    st.markdown("<div class='glass glow'>📊 <b>Decision Dashboard</b></div>", unsafe_allow_html=True)

    if st.session_state.tasks:
        evaluated = []
        for t in st.session_state.tasks:
            t['utility'] = calculate_utility(t)
            evaluated.append(t)

        evaluated.sort(key=lambda x: x['utility'], reverse=True)
        top = evaluated[0]

        st.markdown(
            f"""
            <div class='glass glow'>
            <h2>✅ Do First: {top['name']}</h2>
            <p>Utility Score: <b>{top['utility']}</b></p>
            <p>Critical: {top['critical']} | Category: {top['category']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Utility Chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[t['name'] for t in evaluated],
            y=[t['utility'] for t in evaluated],
            marker_color="#8b5cf6"
        ))
        fig.update_layout(
            template="plotly_dark",
            height=320,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Task List
        st.markdown("### 🗂 Task List")
        for i, t in enumerate(st.session_state.tasks):
            with st.expander(f"{t['name']}  | Utility: {t['utility']}"):
                st.json(t)
                if st.button(f"❌ Delete {t['name']}", key=i):
                    st.session_state.tasks.pop(i)
                    st.experimental_rerun()

        # Learning Feedback
        st.markdown("### 🔁 Agent Learning")
        c1, c2 = st.columns(2)
        if c1.button("👍 Good Decision", use_container_width=True):
            st.session_state.weights['impact'] += 0.1
            st.session_state.weights['urgency'] += 0.1
            st.success("Agent reinforced positive factors")

        if c2.button("👎 Bad Decision", use_container_width=True):
            st.session_state.weights['effort'] += 0.1
            st.session_state.weights['risk'] += 0.1
            st.warning("Agent penalized effort & risk")

    else:
        st.info("Add tasks to activate agent")
            
