import streamlit as st
import plotly.express as px
from datetime import datetime

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Agentic Decision Command Center",
    page_icon="🧠",
    layout="wide"
)

# ==============================
# GLOBAL DARK UI (GLASS)
# ==============================
st.markdown("""
<style>
html, body, [class*="css"] {
  background-color:#020617;
  color:white;
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}
.glass {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 16px;
}
.glow { box-shadow: 0 0 20px rgba(139,92,246,0.35); }
.badge {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
}
.good { background:#10b98133; color:#10b981; }
.warn { background:#f59e0b33; color:#f59e0b; }
.danger { background:#ef444433; color:#ef4444; }
</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE (SAFE INIT)
# ==============================
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ==============================
# KEYWORD INTELLIGENCE (AUTO-INFER)
# ==============================
LIFE_WORDS = ["save", "life", "oxygen", "doctor", "hospital", "emergency", "accident"]
MEDICAL_WORDS = ["doctor", "medicine", "hospital", "treatment", "surgery"]
PLEASURE_WORDS = ["sex", "intercourse", "party", "fun", "entertainment"]
WORK_WORDS = ["deploy", "bug", "server", "client", "deadline", "meeting"]

def infer_values(task: str):
    t = task.lower()

    # defaults
    urgency, impact, effort, risk = 5, 5, 5, 5
    critical = False
    category = "Personal"

    if any(w in t for w in LIFE_WORDS):
        urgency, impact, risk = 9, 10, 9
        effort = 4
        critical = True
        category = "Life"

    if any(w in t for w in MEDICAL_WORDS):
        urgency = max(urgency, 8)
        impact = max(impact, 9)
        risk = max(risk, 8)
        effort = min(effort, 4)
        critical = True
        category = "Life"

    if any(w in t for w in WORK_WORDS):
        urgency = max(urgency, 7)
        impact = max(impact, 7)
        effort = 6
        risk = 5
        category = "Work"

    if any(w in t for w in PLEASURE_WORDS):
        urgency, impact, effort, risk = 3, 3, 2, 2
        critical = False
        category = "Personal"

    return {
        "urgency": urgency,
        "impact": impact,
        "effort": effort,
        "risk": risk,
        "critical": critical,
        "category": category
    }

# ==============================
# UTILITY FUNCTION (CONSTRAINT-AWARE)
# ==============================
def calculate_utility(v):
    base = (v["impact"] * v["urgency"]) / (v["effort"] + v["risk"])
    return round(base * 5, 2) if v["critical"] else round(base * 0.4, 2)

# ==============================
# HEADER
# ==============================
st.markdown(
    "<div class='glass glow'><h2>🧠 Agentic Decision Command Center</h2>"
    "<p>Type one task. Agent infers everything.</p></div>",
    unsafe_allow_html=True
)

st.write("")

# ==============================
# LAYOUT
# ==============================
col_in, col_out = st.columns([1.2, 2.8])

# ==============================
# INPUT (ONE TEXT ONLY)
# ==============================
with col_in:
    st.markdown(
        "<div class='glass'><b>➕ Add Task (Natural Language)</b></div>",
        unsafe_allow_html=True
    )

    task_text = st.text_area(
        "Describe the task",
        placeholder="e.g. meet with doctor to save my life",
        height=120
    )

    if st.button("Run Agent", use_container_width=True):
        if task_text.strip():
            inferred = infer_values(task_text)
            score = calculate_utility(inferred)

            st.session_state.tasks.append({
                "task": task_text,
                "inferred": inferred,
                "utility": score,
                "time": datetime.now().strftime("%H:%M:%S")
            })

            st.success("Task analyzed by agent")
        else:
            st.warning("Please type a task")

# ==============================
# DASHBOARD
# ==============================
with col_out:
    st.markdown(
        "<div class='glass glow'><b>📊 Decision Dashboard</b></div>",
        unsafe_allow_html=True
    )

    if st.session_state.tasks:
        # sort by utility
        data = sorted(
            st.session_state.tasks,
            key=lambda x: x.get("utility", 0),
            reverse=True
        )

        top = data[0]
        inferred = top.get("inferred", {})

        # SAFE BADGE
        badge = "danger" if inferred.get("critical", False) else "good"

        st.markdown(f"""
        <div class='glass glow'>
          <h3>✅ DO FIRST</h3>
          <h2>{top.get("task","")}</h2>
          <span class="badge {badge}">
            {"LIFE-CRITICAL" if inferred.get("critical", False) else "NON-CRITICAL"}
          </span>
          <p><b>Utility:</b> {top.get("utility","?")}</p>
          <p><b>Category:</b> {inferred.get("category","Unknown")}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧠 Agent Explanation")
        st.info(
            f"Urgency {inferred.get('urgency','?')} and impact {inferred.get('impact','?')} "
            f"were inferred from language. Safety constraints applied."
        )

        # CHART
        fig = px.bar(
            data,
            x=[d.get("task","") for d in data],
            y=[d.get("utility",0) for d in data],
            color=[d.get("inferred",{}).get("category","Unknown") for d in data],
            labels={"x":"Task","y":"Utility"},
            title="Utility Comparison"
        )
        fig.update_layout(template="plotly_dark", height=300)
        st.plotly_chart(fig, use_container_width=True)

        # HISTORY
        st.markdown("### 🗂 History")
        for i, d in enumerate(data):
            with st.expander(f"{i+1}. {d.get('task','')} | Utility {d.get('utility','?')}"):
                st.json(d)
                if st.button("Delete", key=f"del{i}"):
                    st.session_state.tasks.remove(d)
                    st.experimental_rerun()
    else:
        st.info("No tasks yet. Type one task and run the agent.")
        
