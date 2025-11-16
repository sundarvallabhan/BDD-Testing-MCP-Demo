"""
Franklin Templeton BDD Testing - Fully Integrated with MCP
Uses real MCP server for all operations
"""

import streamlit as st
import json
from datetime import datetime
import time
from mcp_client import MCPClient

st.set_page_config(
    page_title="Franklin Templeton - MCP Integrated",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .status-success {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .status-error {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .status-running {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Initialize MCP Client
@st.cache_resource
def get_mcp_client():
    return MCPClient()

mcp_client = get_mcp_client()

# Initialize session state
if 'workflow_state' not in st.session_state:
    st.session_state.workflow_state = {
        'user_story': '',
        'refined_story': None,
        'gherkin_scenarios': None,
        'generated_code': None,
        'execution_results': None
    }

# Header
st.markdown('<div class="main-header">🤖 Franklin Templeton BDD Testing</div>', unsafe_allow_html=True)
st.markdown("**Powered by MCP Server - Real AI-Driven Test Generation**")

# Connection status
with st.sidebar:
    st.header("🔌 MCP Connection Status")
    try:
        import requests
        response = requests.get("http://localhost:8080/", timeout=2)
        if response.status_code == 200:
            st.success("✅ MCP Server Connected")
        else:
            st.error("❌ MCP Server Error")
    except:
        st.error("❌ MCP Server Not Running")
        st.warning("Start server:\n```bash\ncd bdd-testing-mcp\npython3 src/bdd_mcp/server.py\n```")

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 User Story Input",
    "✨ Refined Story",
    "🥒 Gherkin Scenarios",
    "💻 Generated Code",
    "▶️ Execution Results"
])

with tab1:
    st.header("Enter Your Franklin Templeton User Story")
    
    st.info("🌐 **REAL MCP SERVER INTEGRATION** - All processing happens through your MCP server!")
    
    user_story = st.text_area(
        "User Story",
        height=250,
        value="""As an individual investor, I want to navigate the Franklin Templeton Website to explore mutual fund options, so that I can make informed decisions about where to invest my money.

Acceptance Criteria:
1) The user lands on the Franklin Templeton homepage and sees a clear navigation menu
2) The user clicks on "Investment Options" and selects "Mutual Funds"
3) The user can filter funds by category (e.g., equity, fixed income) and view detailed fund information
4) Fund pages display performance data, fees and risk level
5) The user can download a fund fact sheet or prospectus

Definition of Done:
1) All acceptance criteria are met
2) Functional and Regression Test cases are executed with Pass Status"""
    )
    
    website_url = st.text_input("Website URL", value="https://www.franklintempleton.com")
    
    col1, col2 = st.columns(2)
    with col1:
        priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=0)
    with col2:
        code_language = st.selectbox("Code Language", ["Python (Playwright)", "Python (Selenium)", "Java (Selenium)"])
    
    execute_tests_option = st.checkbox("Execute tests in real browser", value=True)
    headless_option = st.checkbox("Run browser in headless mode", value=False, help="Uncheck to see browser window")
    
    if st.button("🚀 Run Full Workflow with MCP Server", type="primary", use_container_width=True):
        progress_bar = st.progress(0)
        status = st.empty()
        
        try:
            status.markdown('<div class="status-box status-running">🤖 Connecting to MCP Server...</div>', unsafe_allow_html=True)
            time.sleep(0.5)
            
            # Call MCP Full Workflow
            status.markdown('<div class="status-box status-running">🚀 Running complete BDD workflow through MCP...</div>', unsafe_allow_html=True)
            progress_bar.progress(10)
            
            workflow_start = time.time()
            
            result = mcp_client.full_workflow(
                user_story=user_story,
                website_url=website_url,
                priority=priority,
                language=code_language,
                execute_tests=execute_tests_option,
                headless=headless_option
            )
            
            workflow_duration = time.time() - workflow_start
            
            if result:
                progress_bar.progress(100)
                
                # Store results
                st.session_state.workflow_state['refined_story'] = result['refined_story']
                st.session_state.workflow_state['gherkin_scenarios'] = result['gherkin_scenarios']
                st.session_state.workflow_state['generated_code'] = result['generated_code']
                st.session_state.workflow_state['execution_results'] = result.get('execution_results')
                
                status.markdown(f'<div class="status-box status-success">✅ Workflow completed in {workflow_duration:.2f}s via MCP Server!</div>', unsafe_allow_html=True)
                st.balloons()
                
                # Show summary
                st.success("🎉 **MCP Workflow Complete!**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Story Points", result['refined_story']['story_points'])
                with col2:
                    st.metric("Scenarios", len(result['gherkin_scenarios']['scenarios']))
                with col3:
                    if result.get('execution_results'):
                        st.metric("Tests Passed", f"{result['execution_results']['summary']['passed']}/{result['execution_results']['summary']['total']}")
                
            else:
                status.markdown('<div class="status-box status-error">❌ MCP Server returned no results. Check server logs.</div>', unsafe_allow_html=True)
        
        except Exception as e:
            status.markdown(f'<div class="status-box status-error">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
            st.error(f"Full error: {str(e)}")

with tab2:
    st.header("✨ Refined Story (from MCP)")
    
    if st.session_state.workflow_state['refined_story']:
        refined = st.session_state.workflow_state['refined_story']
        
        st.markdown(f"### 📋 {refined['title']}")
        st.write(refined['description'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Story Points", refined['story_points'])
        with col2:
            st.metric("Priority", refined['priority'])
        with col3:
            st.metric("Category", refined['category'])
        
        st.markdown("### ✅ Acceptance Criteria")
        for idx, criterion in enumerate(refined['acceptance_criteria'], 1):
            st.markdown(f"{idx}. {criterion}")
        
        st.markdown("### 🎯 Test Scenarios")
        for scenario in refined['test_scenarios']:
            with st.expander(f"📌 {scenario['name']} ({scenario['type']})"):
                st.write(f"**Description:** {scenario['description']}")
                st.write(f"**Priority:** {scenario['priority']}")
        
        st.info("✨ **Generated by MCP Server**")
    else:
        st.info("👈 Run the workflow first in the 'User Story Input' tab")

with tab3:
    st.header("🥒 Gherkin Scenarios (from MCP)")
    
    if st.session_state.workflow_state['gherkin_scenarios']:
        gherkin = st.session_state.workflow_state['gherkin_scenarios']
        
        st.markdown("### 📄 Complete Feature File")
        st.code(gherkin['feature_file'], language='gherkin')
        
        st.download_button(
            label="💾 Download Feature File",
            data=gherkin['feature_file'],
            file_name="franklin_templeton.feature",
            mime="text/plain"
        )
        
        st.markdown("### 🎬 Individual Scenarios")
        for idx, scenario in enumerate(gherkin['scenarios'], 1):
            tags_str = " ".join(scenario['tags'])
            with st.expander(f"Scenario {idx}: {scenario['name']} {tags_str}"):
                st.code(scenario['gherkin'], language='gherkin')
        
        st.info("🥒 **Generated by MCP Server**")
    else:
        st.info("👈 Run the workflow first")

with tab4:
    st.header("💻 Generated Test Code (from MCP)")
    
    if st.session_state.workflow_state['generated_code']:
        code = st.session_state.workflow_state['generated_code']
        
        st.markdown(f"### {code['language']} - {code['framework']}")
        
        st.markdown("**Main Test File:**")
        st.code(code['main_file'], language=code['syntax'])
        
        st.download_button(
            label="💾 Download Test Code",
            data=code['main_file'],
            file_name=code['main_file_name'],
            mime="text/plain"
        )
        
        if code.get('supporting_files'):
            st.markdown("### 📁 Supporting Files")
            for filename, content in code['supporting_files'].items():
                with st.expander(f"📄 {filename}"):
                    st.code(content, language='python')
        
        st.markdown("### 📋 Setup Instructions")
        st.code(code['setup_instructions'], language='bash')
        
        st.info("💻 **Generated by MCP Server**")
    else:
        st.info("👈 Run the workflow first")

with tab5:
    st.header("▶️ Test Execution Results (from MCP)")
    
    if st.session_state.workflow_state['execution_results']:
        results = st.session_state.workflow_state['execution_results']
        
        st.success("🌐 **Tests Executed by MCP Server in Real Browser!**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", results['summary']['total'])
        with col2:
            st.metric("Passed ✅", results['summary']['passed'])
        with col3:
            st.metric("Failed ❌", results['summary']['failed'])
        with col4:
            st.metric("Pass Rate", f"{results['summary']['pass_rate']:.0f}%")
        
        st.markdown("---")
        st.markdown("### 📊 Detailed Results")
        
        for idx, scenario in enumerate(results['scenario_results'], 1):
            emoji = "✅" if scenario['status'] == "passed" else "❌"
            tags = " ".join(scenario.get('tags', []))
            
            with st.expander(f"{emoji} Scenario {idx}: {scenario['name']} - {scenario['status'].upper()} ({scenario['duration']:.1f}s)"):
                st.write(f"**Tags:** {tags}")
                st.write(f"**Duration:** {scenario['duration']:.2f}s")
                
                st.markdown("**Steps:**")
                for step in scenario['steps']:
                    step_emoji = "✅" if step['status'] == "passed" else "❌"
                    st.write(f"{step_emoji} {step['step']} ({step['duration']:.2f}s)")
                
                if scenario.get('error'):
                    st.error(f"Error: {scenario['error']}")
        
        if results.get('execution_log'):
            with st.expander("📋 View Execution Log"):
                st.code(results['execution_log'], language='text')
        
        st.info("▶️ **Executed by MCP Server**")
    else:
        st.info("👈 Run the workflow with 'Execute tests' enabled")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.header("ℹ️ About This Integration")
st.sidebar.info("""
**MCP Integration Active!**

This app connects to your BDD Testing MCP Server and uses it for:

✅ Story refinement
✅ Gherkin generation  
✅ Code generation
✅ Real browser execution

**All processing happens through your MCP server!**

This demonstrates the power of Model Context Protocol for reusable AI capabilities.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**MCP Server Location:**")
st.sidebar.code("http://localhost:8080")
