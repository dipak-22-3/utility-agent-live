import streamlit as st
import json
import plotly.express as px

st.set_page_config(page_title="Agentic Decision AI", layout="wide")

# ---------- Memory ----------
if "weights" not in st.session_state:
    st.session_state.weights = {
        "impact": 1.0,
        "urgency": 1.0,
        "effort": 1.0,
        "risk": 1.0
    }

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Utility ----------
def utility(task):
    w = st.session_state.weights
    return (w["impact"] * task["impact"] + w["urgency"] * task["urgency"]) / (
        w["effort"] * task["effort"] + w["risk"] * task["risk"]
    )

# ---------- UI ----------
st.title("🧠 Agentic Decision Intelligence System")
st.caption("Utility-based, Goal-driven, Adaptive AI Agent")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Task name")
    urgency = st.slider("Urgency", 1, 10, 5)
    impact = st.slider("Impact", 1, 10, 5)

with col2:
    effort = st.slider("Effort", 1, 10, 5)
    risk = st.slider("Risk", 1, 10, 5)

if st.button("➕ Add Task"):
    st.session_state.history.append({
        "name": name,
        "urgency": urgency,
        "impact": impact,
        "effort": effort,
        "risk": risk
    })

# ---------- Decision ----------
if st.session_state.history:
    tasks = []
    for t in st.session_state.history:
        score = round(utility(t), 2)
        t["utility"] = score
        tasks.append(t)

    tasks = sorted(tasks, key=lambda x: x["utility"], reverse=True)

    st.subheader("✅ Agent Decision")
    st.success(f"DO FIRST: **{tasks[0]['name']}** (Utility: {tasks[0]['utility']})")

    st.markdown("### Explanation")
    st.info(
        f"High impact ({tasks[0]['impact']}) and urgency ({tasks[0]['urgency']}) "
        f"outweigh effort ({tasks[0]['effort']}) and risk ({tasks[0]['risk']})."
    )

    # ---------- Chart ----------
    fig = px.bar(
        tasks,
        x="name",
        y="utility",
        title="Utility Score Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---------- Learning ----------
    st.markdown("### Feedback")
    col_good, col_bad = st.columns(2)

    if col_good.button("👍 Good Decision"):
        st.session_state.weights["impact"] += 0.1
        st.session_state.weights["urgency"] += 0.1
        st.success("Agent learned: prioritizing impact & urgency")

    if col_bad.button("👎 Bad Decision"):
        st.session_state.weights["effort"] += 0.1
        st.session_state.weights["risk"] += 0.1
        st.warning("Agent learned: penalizing effort & risk")

    # ---------- Weights ----------
    st.markdown("### Agent Weights (Learning State)")
    st.json(st.session_state.weights)

else:
    st.info("Add tasks to activate agent.")
