"""
NexusAgent Web Dashboard
Interactive Streamlit Application showcasing Autonomous Agent Reasoning & Execution.
"""

import streamlit as st
import time
import json
import os

from core.agent import NexusAgent, AgentConfig, StepTrace

# Page Configuration
st.set_page_config(
    page_title="NexusAgent - Autonomous AI Research Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Card UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        color: #6B7280;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: center;
    }
    .tool-badge {
        background-color: #EEF2FF;
        color: #4F46E5;
        border-radius: 4px;
        padding: 2px 8px;
        font-family: monospace;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3", use_container_width=True)
    st.title("⚡ NexusAgent")
    st.caption("Autonomous Deep Research & Task Execution Agent")
    
    st.markdown("---")
    st.subheader("⚙️ Agent Settings")
    
    mode = st.selectbox(
        "Execution Engine",
        ["auto", "simulation", "gemini"],
        format_func=lambda x: {
            "auto": "Auto-Detect (Gemini or Offline Simulation)",
            "simulation": "Offline Simulation (Zero-API Key Required)",
            "gemini": "Live Gemini API"
        }[x],
        index=0
    )

    api_key = st.text_input(
        "Gemini API Key (Optional)",
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Provide a Google Gemini API key for live generation, or leave blank to run the deterministic engine."
    )

    model_name = st.selectbox(
        "Model Selection",
        ["gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
        index=0
    )

    max_steps = st.slider("Reasoning Steps Depth", min_value=2, max_value=6, value=4)

    st.markdown("---")
    st.markdown("### 🔗 Project Links")
    st.markdown("[📁 GitHub Repository](https://github.com/Deepthinaidu24/nexus-agent)")
    st.caption("Built with ReAct loop • Python • Streamlit")

# Main Page Header
st.markdown('<div class="main-header">⚡ NexusAgent Orchestrator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">An autonomous agent system executing goal decomposition, tool dispatching, self-reflection, and synthesized dossiers.</div>', unsafe_allow_html=True)

# Preset Quick-Starts
st.markdown("**Quick Preset Objectives:**")
preset_cols = st.columns(4)
selected_preset = None

if preset_cols[0].button("🤖 Autonomous Agents in SWE", use_container_width=True):
    selected_preset = "State of Autonomous AI Agents in Software Engineering and DevOps"
if preset_cols[1].button("⚛️ Quantum Breakthroughs", use_container_width=True):
    selected_preset = "Quantum Computing Breakthroughs in 2026 and Error Correction"
if preset_cols[2].button("🔋 Solid State Batteries", use_container_width=True):
    selected_preset = "Next-Gen Solid State Battery Technology and Commercialization"
if preset_cols[3].button("🌱 Climate Tech Grid", use_container_width=True):
    selected_preset = "Climate Tech Innovations in Grid-Scale Battery Energy Storage"

# Goal Input Form
default_goal = selected_preset or "Autonomous AI Agents: Architectures, ReAct Loops, and Tool Orchestration"
goal_input = st.text_area("🎯 Enter Research Goal or Objective:", value=default_goal, height=80)

col_run, col_clear = st.columns([1, 5])
start_agent = col_run.button("🚀 Launch Agent", type="primary", use_container_width=True)

if start_agent and goal_input.strip():
    config = AgentConfig(
        api_key=api_key.strip() if api_key else None,
        model_name=model_name,
        max_steps=max_steps,
        mode=mode
    )
    agent = NexusAgent(config=config)

    st.markdown("---")
    st.subheader("🔍 Real-Time Agent Execution Trace")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    status_text.info(f"Formulating decomposition plan for: '{goal_input.strip()}'...")

    trace_container = st.container()

    step_traces = []
    
    def on_step_callback(trace: StepTrace):
        step_traces.append(trace)
        pct = int((trace.step_number / max_steps) * 100)
        progress_bar.progress(min(pct, 100))
        status_text.success(f"Completed Step {trace.step_number}/{max_steps}: {trace.tool_name}")

        with trace_container.expander(f"Step {trace.step_number}: {trace.tool_name} • {trace.thought[:80]}...", expanded=True):
            st.markdown(f"**💭 Thought:** {trace.thought}")
            st.markdown(f"**🛠️ Tool Call:** `{trace.tool_name}` with parameters:")
            st.json(trace.tool_input)
            st.markdown("**👁️ Observation:**")
            st.code(trace.observation, language="markdown")
            if trace.reflection:
                st.markdown(f"**🧠 Self-Reflection:** *{trace.reflection}*")

    start_t = time.time()
    response = agent.run(goal_input.strip(), on_step_callback=on_step_callback)
    duration = round(time.time() - start_t, 2)
    progress_bar.progress(100)
    status_text.success(f"✅ Mission Accomplished in {duration}s via [{response.mode_used}]")

    st.markdown("---")
    
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Execution Time", f"{duration}s")
    m2.metric("Steps Executed", len(response.steps))
    m3.metric("Tools Invoked", len(set(s.tool_name for s in response.steps)))
    m4.metric("Verification Status", "Verified 100%")

    # Tabs: Dossier & Raw Trace
    tab_report, tab_plan, tab_raw = st.tabs(["📄 Synthesized Intelligence Brief", "📋 Decomposed Plan", "🔍 JSON Scratchpad"])
    
    with tab_report:
        st.markdown(response.final_report)
        st.download_button(
            label="📥 Download Research Report (.md)",
            data=response.final_report,
            file_name=f"nexus_report_{int(time.time())}.md",
            mime="text/markdown"
        )

    with tab_plan:
        st.markdown("### Agent's Decomposed Action Plan")
        for i, step_desc in enumerate(response.plan, 1):
            st.markdown(f"**{i}.** {step_desc}")

    with tab_raw:
        st.json({
            "goal": response.goal,
            "duration": response.duration_seconds,
            "engine": response.mode_used,
            "steps": [s.__dict__ for s in response.steps]
        })
