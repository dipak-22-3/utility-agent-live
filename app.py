import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Agentic Decision Intelligence",
    layout="wide"
)

# ===============================
# MEMORY (Session State)
# ===============================
if "weights" not in st.session_state:
    st.session_state.weights = {
        "impact": 1.0,
        "urgency": 1.0,
        "effort": 1.0,
        "risk": 1.0
    }

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ===============================
# UTILITY FUNCTION (CONSTRAINT-AWARE)
# ===============================
def utility(task):
    w = st.session_state.weights

    base_score = (
        (w["impact"] * task["impact"] + w["urgency"] * task["urgency"]) /
        (w["effort"] * task["effort"] + w["risk"] * task["risk"])
    )

    # HARD SAFETY CONSTRAINT
    if task["critical"] == "Yes":
        return round(base_score * 5, 2)     # force priority
    else:
        return round(base_score * 0.5, 2)   # penalize non-critical

# ===============================
# UI HEADER
# ===============================
st.title("🧠 Agentic Decision Intelligence System")
st.caption("Utility-Based • Goal-Driven • Constraint-Aware • Adaptive")

st.divider()

# ===============================
# INPUT SECTION
# ===============================
st.subheader("➕ Add Task")

col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("Task Name")

with col2:
    category = st.selectbox(
        "Task Category",
        ["Life", "Work", "Personal"]
    )

with col3:
    critical = st.selectbox(
        "Life-Critical?",
        ["No", "Yes"]
    )

col4, col5, col6, col7 = st.columns(4)

with col4:
    urgency = st.slider("Urgency", 1, 10, 5)

with col5:
    impact = st.slider("Impact", 1, 10, 5)

with col6:
    effort = st.slider("Effort", 1, 10, 5)

with col7:
    risk = st.slider("Risk", 1, 10, 5)

if st.button("➕ Add Task", use_container_width=True):
    if name.strip() == "":
        st.warning("Task name required")
    else:
        st.session_state.tasks.append({
            "name": name,
            "category": category,
            "critical": critical,
            "urgency": urgency,
            "impact": impact,
            "effort": effort,
            "risk": risk
        })
        st.success("Task added")

st.divider()

# ===============================
# DECISION ENGINE
# ===============================
if st.session_state.tasks:

    evaluated = []
    for t in st.session_state.tasks:
        score = utility(t)
        t["utility"] = score
        evaluated.append(t)

    evaluated = sorted(
        evaluated,
        key=lambda x: x["utility"],
        reverse=True
    )

    # ===============================
    # DECISION OUTPUT
    # ===============================
    st.subheader("✅ Agent Decision")

    top = evaluated[0]

    st.success(
        f"DO FIRST: **{top['name']}**  \n"
        f"Utility Score: **{top['utility']}**"
    )

    st.markdown("### 🧠 Explanation")
    st.info(
        f"""
**Critical:** {top['critical']}  
**Category:** {top['category']}  

High **impact ({top['impact']})** and **urgency ({top['urgency']})**
outweighed **effort ({top['effort']})** and **risk ({top['risk']})**.

Hard safety constraints were applied.
"""
    )

    # ===============================
    # VISUALIZATION
    # ===============================
    st.subheader("📊 Utility Comparison")

    fig = px.bar(
        evaluated,
        x="name",
        y="utility",
        color="critical",
        title="Utility Score by Task"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # FEEDBACK LEARNING
    # ===============================
    st.subheader("🔁 Agent Learning")

    col_good, col_bad = st.columns(2)

    if col_good.button("👍 Good Decision", use_container_width=True):
        st.session_state.weights["impact"] += 0.1
        st.session_state.weights["urgency"] += 0.1
        st.success("Agent learned: prioritizing impact & urgency")

    if col_bad.button("👎 Bad Decision", use_container_width=True):
        st.session_state.weights["effort"] += 0.1
        st.session_state.weights["risk"] += 0.1
        st.warning("Agent learned: penalizing effort & risk")

    # ===============================
    # WEIGHT VISIBILITY
    # ===============================
    st.subheader("⚙️ Agent Weights")
    st.json(st.session_state.weights)

    # ===============================
    # TASK MANAGEMENT
    # ===============================
    st.subheader("🗂 Task List")

    for i, t in enumerate(st.session_state.tasks):
        with st.expander(f"{i+1}. {t['name']}"):
            st.write(t)
            if st.button(f"❌ Delete '{t['name']}'", key=i):
                st.session_state.tasks.pop(i)
                st.experimental_rerun()

else:
    st.info("Add tasks to activate the agent.")
    
