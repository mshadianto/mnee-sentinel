"""
MNEE Sentinel: AI-Powered Treasury Guardian (Enhanced)
Streamlit Dashboard with Advanced Visualizations
"""
import streamlit as st
from decimal import Decimal
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config.settings import TREASURY_ADDRESS, MNEE_CONTRACT_ADDRESS
from utils.crypto_utils import MNEETokenManager
from utils.db_utils import GovernanceDB
from agents.auditor_agent import AuditorAgent

# ===================================
# Page Configuration
# ===================================

st.set_page_config(
    page_title="MNEE Sentinel - Treasury Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (Enhanced)
st.markdown("""
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    /* Audit results */
    .audit-approved {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 6px solid #28a745;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        box-shadow: 0 2px 8px rgba(40,167,69,0.1);
    }
    
    .audit-rejected {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 6px solid #dc3545;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        box-shadow: 0 2px 8px rgba(220,53,69,0.1);
    }
    
    /* ENHANCED: Big RED alert for rejections */
    .rejection-alert {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 20px rgba(220,53,69,0.4);
        border: 3px solid #bd2130;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* ENHANCED: Big GREEN success for approvals */
    .approval-alert {
        background: linear-gradient(135deg, #28a745 0%, #218838 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 20px rgba(40,167,69,0.4);
        border: 3px solid #1e7e34;
    }
    
    /* Risk Level Badges */
    .risk-high {
        background-color: #dc3545;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .risk-medium {
        background-color: #ffc107;
        color: #212529;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    
    .risk-low {
        background-color: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 700;
    }
    
    /* Code blocks */
    code {
        background-color: #f4f4f4;
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# ===================================
# Initialize Components
# ===================================

@st.cache_resource
def init_components(provider="groq"):
    """Initialize blockchain, database, and AI agent"""
    try:
        token_manager = MNEETokenManager()
        db = GovernanceDB()
        agent = AuditorAgent(db, provider=provider)
        return token_manager, db, agent
    except Exception as e:
        st.error(f"❌ Initialization Error: {e}")
        st.stop()

# ===================================
# Sidebar - Configuration & Status
# ===================================

st.sidebar.title("🛡️ MNEE Sentinel")
st.sidebar.markdown("*AI-Powered Treasury Guardian*")
st.sidebar.markdown("---")

# AI Provider Selection
st.sidebar.markdown("### 🤖 AI Configuration")
ai_provider = st.sidebar.selectbox(
    "Select AI Provider",
    options=["groq", "openai", "anthropic"],
    format_func=lambda x: {
        "groq": "⚡ Groq (Llama 3.1) - Fastest",
        "openai": "🎯 OpenAI (GPT-4) - Accurate",
        "anthropic": "🧠 Claude (Sonnet 4) - Best"
    }[x],
    index=0
)

# Initialize with selected provider
token_manager, db, agent = init_components(provider=ai_provider)

# Update agent if provider changed
if agent.provider != ai_provider:
    try:
        agent.switch_provider(ai_provider)
        st.sidebar.success(f"✅ Switched to {ai_provider.upper()}")
    except Exception as e:
        st.sidebar.error(f"❌ Provider switch failed: {e}")

st.sidebar.markdown("---")

# Treasury Balance
st.sidebar.markdown("### 💰 Treasury Status")
if TREASURY_ADDRESS:
    balance, balance_str = token_manager.get_balance(TREASURY_ADDRESS)
    st.sidebar.metric("Balance", balance_str, delta=None)
    st.sidebar.caption(f"Address: `{TREASURY_ADDRESS[:8]}...{TREASURY_ADDRESS[-6:]}`")
else:
    st.sidebar.warning("⚠️ Treasury address not configured")

st.sidebar.markdown("---")

# Network Info
st.sidebar.markdown("### 🌐 Network Info")
st.sidebar.info(f"""
**Token:** MNEE  
**Network:** Ethereum Mainnet  
**Contract:** `{MNEE_CONTRACT_ADDRESS[:8]}...{MNEE_CONTRACT_ADDRESS[-6:]}`
""")

# Quick Stats
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
try:
    total_audits = len(db.get_recent_audits(limit=1000))
    recent_audits = db.get_recent_audits(limit=10)
    approved_count = sum(1 for a in recent_audits if a['decision'] == 'APPROVED')
    
    col1, col2 = st.sidebar.columns(2)
    col1.metric("Total Audits", total_audits)
    col2.metric("Recent Approvals", f"{approved_count}/10")
except:
    pass

# ===================================
# Main Dashboard Header
# ===================================

st.title("🛡️ MNEE Sentinel Dashboard")
st.markdown("### AI-Powered Treasury Management with Full Compliance & Audit Trail")
st.markdown("---")

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

try:
    # Fetch budget totals
    budgets_data = db.client.table("budgets").select("*").execute()
    total_budget = sum(Decimal(str(b['monthly_limit_mnee'])) for b in budgets_data.data)
    total_spent = sum(Decimal(str(b['current_spent'])) for b in budgets_data.data)
    total_remaining = total_budget - total_spent
    
    with col1:
        st.metric("📊 Total Budget", f"{total_budget:,.0f} MNEE")
    with col2:
        st.metric("💸 Total Spent", f"{total_spent:,.0f} MNEE", 
                 delta=f"-{(total_spent/total_budget*100):.1f}%" if total_budget > 0 else None)
    with col3:
        st.metric("💰 Remaining", f"{total_remaining:,.0f} MNEE",
                 delta=f"+{(total_remaining/total_budget*100):.1f}%" if total_budget > 0 else None)
    with col4:
        vendors_count = db.client.table("whitelisted_vendors").select("id", count="exact").execute()
        st.metric("✅ Whitelisted Vendors", vendors_count.count if vendors_count.count else 0)
except Exception as e:
    st.error(f"Error loading metrics: {e}")

st.markdown("---")

# ===================================
# Tabs
# ===================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Submit Proposal",
    "📊 Budget Analytics", 
    "📋 Audit History",
    "👥 Vendor Management"
])

# ===================================
# TAB 1: Submit Proposal
# ===================================

with tab1:
    st.markdown("## 📝 Submit Payment Proposal")
    st.markdown("Describe your payment request in natural language **OR** upload a PDF invoice.")
    
    # PDF Upload Feature (NEW!)
    st.markdown("### 📄 Option 1: Upload Invoice/Contract PDF")
    
    uploaded_file = st.file_uploader(
        "Upload PDF document (invoice, contract, etc.)",
        type=['pdf'],
        help="Upload a PDF invoice and we'll auto-extract payment details"
    )
    
    parsed_data = None
    auto_proposal = ""
    
    if uploaded_file is not None:
        try:
            # Import document parser
            from utils.document_parser import InvoiceParser, PYMUPDF_AVAILABLE
            
            if not PYMUPDF_AVAILABLE:
                st.warning("⚠️ PyMuPDF not installed. Please run: `pip install pymupdf`")
            else:
                with st.spinner("⚡ Parsing PDF document (fast mode)..."):
                    parser = InvoiceParser()
                    
                    # Parse PDF
                    document_dict = parser.parse_uploaded_file(uploaded_file)
                    
                    # Extract invoice data
                    parsed_data = parser.extract_invoice_data(document_dict)
                    
                    st.success("✅ PDF parsed successfully!")
                    
                    # Show extracted data
                    with st.expander("📋 Extracted Data from PDF"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Vendor", parsed_data.get('vendor_name') or "Not found")
                        with col2:
                            st.metric("Amount", f"{parsed_data.get('amount') or 0:,.2f}")
                        with col3:
                            st.metric("Invoice #", parsed_data.get('invoice_number') or "N/A")
                        
                        st.caption(f"**Description:** {parsed_data.get('description', 'N/A')[:200] if parsed_data.get('description') else 'N/A'}")
                    
                    # Generate auto-proposal
                    auto_proposal = parser.generate_proposal_from_invoice(document_dict)
                    st.info(f"💡 **Auto-generated proposal:** {auto_proposal}")
                
        except ImportError:
            st.warning("⚠️ PDF parser not available. Please run: `pip install pymupdf`")
        except Exception as e:
            st.error(f"❌ Error parsing PDF: {e}")
    
    st.markdown("---")
    st.markdown("### ✍️ Option 2: Write Proposal Manually")
    
    # Example proposals
    with st.expander("💡 See Example Proposals (Indonesian Vendors)"):
        st.code("""
✅ GOOD EXAMPLES:

"Transfer 50 MNEE to PT Nusantara FX Services (0xA1b2C3D4e5F60718293aBcD4E5F60718293aBcD4) for FX hedging"

"Pay PT Global Money Transfer 40 MNEE at address 0xB2c3D4E5F60718293aBcD4E5F60718293aBcD4E5 for remittance services"

"Send 25 MNEE to PT Office Supplies Jakarta (0x0718293aBcD4E5F60718293aBcD4E5F60718293a) for stationery"

❌ BAD EXAMPLES:

"Send money to Bob" ← Missing: amount, address, category
"Transfer 200 MNEE to Random Company" ← Not whitelisted
"Pay AWS $1000" ← Wrong currency (use MNEE)
        """)
    
    # Input form (pre-fill if PDF was parsed)
    proposal_text = st.text_area(
        "💬 Proposal Description",
        value=auto_proposal if auto_proposal else "",
        placeholder="Example: Transfer 30 MNEE to PT Cybersecurity Services (0x293aBcD4E5F60718293aBcD4E5F60718293aBcD4E) for monthly security audit",
        height=120,
        help="Use natural language. Include vendor name, wallet address, amount in MNEE, and purpose."
    )
    
    col1, col2, col3 = st.columns([2, 2, 3])
    with col1:
        submit_button = st.button("🔍 Submit for AI Audit", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.rerun()
    
    if submit_button and proposal_text:
        with st.spinner(f"🤖 {ai_provider.upper()} analyzing proposal..."):
            # Run AI audit
            audit_result = agent.audit_proposal(proposal_text)
            
            # Display result
            st.markdown("---")
            st.markdown("## 🔍 Audit Result")
            
            if audit_result['decision'] == "APPROVED":
                # BIG GREEN SUCCESS ALERT
                st.markdown(f"""
                <div class="approval-alert">
                    <h2 style="margin: 0; text-align: center;">✅ APPROVED</h2>
                    <p style="text-align: center; font-size: 1.2rem; margin: 1rem 0;">
                        AI Confidence: {audit_result['confidence']:.0%} | Provider: {(audit_result.get('provider') or 'UNKNOWN').upper()}
                    </p>
                    <p style="text-align: center;">
                        <span class="risk-low">RISK LEVEL: LOW</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📋 Analysis")
                st.success(audit_result['reasoning'])
                
                # Show parsed details in columns
                if audit_result['parsed_data']:
                    parsed = audit_result['parsed_data']
                    st.markdown("### 📊 Parsed Information")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Vendor", parsed.vendor_name)
                    with col2:
                        st.metric("Amount", f"{parsed.amount} MNEE")
                    with col3:
                        st.metric("Category", parsed.category)
                    with col4:
                        st.metric("Confidence", f"{parsed.confidence:.0%}")
                    
                    st.caption(f"**Wallet:** `{parsed.vendor_address}`")
                
                # Execute transaction option
                st.markdown("---")
                st.markdown("### 💸 Execute Transaction")
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    execute_tx = st.button("💰 Execute Payment", type="primary", use_container_width=True)
                with col2:
                    st.info("⚠️ In demo mode, transactions are simulated. Set TREASURY_PRIVATE_KEY for live execution.")
                
                if execute_tx:
                    with st.spinner("⛓️ Executing blockchain transaction..."):
                        parsed = audit_result['parsed_data']
                        success, tx_hash = token_manager.execute_transfer(
                            parsed.vendor_address,
                            Decimal(str(parsed.amount)),
                            simulate_only=True  # Change to False for mainnet
                        )
                        
                        if success:
                            st.success(f"✅ **Transaction Successful!**\n\nTransaction Hash: `{tx_hash}`")
                            
                            # Log to audit trail
                            db.log_audit_decision(
                                proposal_text=proposal_text,
                                vendor_name=parsed.vendor_name,
                                vendor_address=parsed.vendor_address,
                                amount=Decimal(str(parsed.amount)),
                                category=parsed.category,
                                decision="APPROVED",
                                reasoning=audit_result['reasoning'],
                                ai_confidence=audit_result['confidence'],
                                transaction_hash=tx_hash
                            )
                            
                            # Update budget
                            db.update_budget_spent(parsed.category, Decimal(str(parsed.amount)))
                            
                            # Update velocity tracker
                            db.update_velocity_tracker(parsed.vendor_address, Decimal(str(parsed.amount)))
                            
                            st.balloons()
                            st.info("✅ Audit log created, budget updated, velocity tracker updated")
                        else:
                            st.error(f"❌ **Transaction Failed**\n\nError: {tx_hash}")
            
            else:  # REJECTED
                # Determine risk level based on rejection reason
                reasoning_lower = audit_result['reasoning'].lower()
                if 'budget' in reasoning_lower or 'limit' in reasoning_lower:
                    risk_level = "HIGH"
                    risk_class = "risk-high"
                elif 'whitelist' in reasoning_lower or 'not found' in reasoning_lower:
                    risk_level = "CRITICAL"
                    risk_class = "risk-high"
                elif 'velocity' in reasoning_lower:
                    risk_level = "HIGH"
                    risk_class = "risk-high"
                else:
                    risk_level = "MEDIUM"
                    risk_class = "risk-medium"
                
                # BIG RED REJECTION ALERT
                st.markdown(f"""
                <div class="rejection-alert">
                    <h2 style="margin: 0; text-align: center;">🚫 TRANSACTION BLOCKED</h2>
                    <p style="text-align: center; font-size: 1.2rem; margin: 1rem 0;">
                        AI Confidence: {audit_result['confidence']:.0%} | Provider: {(audit_result.get('provider') or 'UNKNOWN').upper()}
                    </p>
                    <p style="text-align: center;">
                        <span class="{risk_class}">RISK LEVEL: {risk_level}</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 🔍 Detailed Rejection Analysis")
                
                # Show detailed reasoning with breakdown
                st.error("**Primary Reason:**")
                st.markdown(f"```\n{audit_result['reasoning']}\n```")
                
                # Log rejection
                if audit_result['parsed_data']:
                    parsed = audit_result['parsed_data']
                    db.log_audit_decision(
                        proposal_text=proposal_text,
                        vendor_name=parsed.vendor_name,
                        vendor_address=parsed.vendor_address,
                        amount=Decimal(str(parsed.amount)),
                        category=parsed.category,
                        decision="REJECTED",
                        reasoning=audit_result['reasoning'],
                        ai_confidence=audit_result['confidence']
                    )
                    st.info("📝 Rejection logged to audit trail")
            
            # Show detailed compliance checks
            with st.expander("🔬 View Detailed Compliance Checks"):
                st.json(audit_result['details'])

# ===================================
# TAB 2: Budget Analytics
# ===================================

with tab2:
    st.markdown("## 📊 Budget Analytics & Visualization")
    
    try:
        budgets_data = db.client.table("budgets").select("*").execute()
        
        if budgets_data.data:
            # Prepare data
            budget_rows = []
            for budget in budgets_data.data:
                limit = Decimal(str(budget['monthly_limit_mnee']))
                spent = Decimal(str(budget['current_spent']))
                remaining = limit - spent
                pct_used = float(spent / limit * 100) if limit > 0 else 0
                
                budget_rows.append({
                    "Category": budget['category'],
                    "Limit": float(limit),
                    "Spent": float(spent),
                    "Remaining": float(remaining),
                    "% Used": pct_used
                })
            
            df_budgets = pd.DataFrame(budget_rows)
            
            # Visualization 1: Budget Overview Table
            st.markdown("### 📋 Budget Overview")
            
            # Format dataframe for display
            df_display = df_budgets.copy()
            df_display['Limit'] = df_display['Limit'].apply(lambda x: f"{x:,.2f} MNEE")
            df_display['Spent'] = df_display['Spent'].apply(lambda x: f"{x:,.2f} MNEE")
            df_display['Remaining'] = df_display['Remaining'].apply(lambda x: f"{x:,.2f} MNEE")
            df_display['% Used'] = df_display['% Used'].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
            
            # Visualization 2: Pie Chart - Budget Distribution
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🥧 Budget Distribution by Category")
                fig_pie = px.pie(
                    df_budgets,
                    values='Limit',
                    names='Category',
                    title='Total Budget Allocation',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 Spending Status")
                fig_donut = px.pie(
                    df_budgets,
                    values='Spent',
                    names='Category',
                    title='Current Spending by Category',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_donut.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_donut, use_container_width=True)
            
            # Visualization 3: Bar Chart - Budget Utilization
            st.markdown("### 📈 Budget Utilization Comparison")
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                name='Spent',
                x=df_budgets['Category'],
                y=df_budgets['Spent'],
                marker_color='#dc3545'
            ))
            fig_bar.add_trace(go.Bar(
                name='Remaining',
                x=df_budgets['Category'],
                y=df_budgets['Remaining'],
                marker_color='#28a745'
            ))
            
            fig_bar.update_layout(
                barmode='stack',
                title='Budget: Spent vs Remaining (MNEE)',
                xaxis_title='Category',
                yaxis_title='Amount (MNEE)',
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Visualization 4: Progress Bars
            st.markdown("### 🎯 Category Utilization Progress")
            
            for _, row in df_budgets.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{row['Category']}**")
                    progress_val = row['% Used'] / 100
                    st.progress(progress_val)
                
                with col2:
                    color = "🟢" if row['% Used'] < 60 else "🟡" if row['% Used'] < 80 else "🔴"
                    st.metric("Usage", f"{row['% Used']:.1f}% {color}")
                
                with col3:
                    st.metric("Remaining", f"{row['Remaining']:.0f}")
            
            # Visualization 5: Heatmap of Risk Levels
            st.markdown("### 🌡️ Budget Risk Heatmap")
            
            df_budgets['Risk'] = df_budgets['% Used'].apply(
                lambda x: 'Low' if x < 60 else 'Medium' if x < 80 else 'High'
            )
            
            risk_colors = {'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'}
            
            fig_scatter = px.scatter(
                df_budgets,
                x='Category',
                y='% Used',
                size='Spent',
                color='Risk',
                color_discrete_map=risk_colors,
                title='Budget Risk Assessment',
                labels={'% Used': 'Utilization %'},
                height=400
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        else:
            st.info("📭 No budget data available")
    
    except Exception as e:
        st.error(f"❌ Error loading budget analytics: {e}")

# ===================================
# TAB 3: Audit History
# ===================================

with tab3:
    st.markdown("## 📋 Audit History & Compliance Trail")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_decision = st.selectbox(
            "Filter by Decision",
            ["All", "APPROVED", "REJECTED"]
        )
    with col2:
        limit = st.slider("Number of records", 5, 50, 20)
    
    # Fetch audits
    audits = db.get_recent_audits(limit=limit)
    
    if audits:
        # Filter
        if filter_decision != "All":
            audits = [a for a in audits if a['decision'] == filter_decision]
        
        # Statistics
        st.markdown("### 📊 Audit Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(audits)
        approved = sum(1 for a in audits if a['decision'] == 'APPROVED')
        rejected = total - approved
        avg_confidence = sum(float(a['ai_confidence']) for a in audits if a['ai_confidence']) / total if total > 0 else 0
        
        col1.metric("Total Audits", total)
        col2.metric("✅ Approved", approved, delta=f"{approved/total*100:.0f}%" if total > 0 else "0%")
        col3.metric("❌ Rejected", rejected, delta=f"-{rejected/total*100:.0f}%" if total > 0 else "0%")
        col4.metric("Avg Confidence", f"{avg_confidence:.0%}")
        
        # Visualization: Approval Rate Over Time
        st.markdown("### 📈 Approval Trends")
        df_audits = pd.DataFrame(audits)
        df_audits['created_at'] = pd.to_datetime(df_audits['created_at'])
        df_audits['date'] = df_audits['created_at'].dt.date
        
        daily_stats = df_audits.groupby(['date', 'decision']).size().unstack(fill_value=0)
        
        fig_trend = go.Figure()
        if 'APPROVED' in daily_stats.columns:
            fig_trend.add_trace(go.Scatter(
                x=daily_stats.index,
                y=daily_stats['APPROVED'],
                mode='lines+markers',
                name='Approved',
                line=dict(color='#28a745', width=3),
                fill='tozeroy'
            ))
        if 'REJECTED' in daily_stats.columns:
            fig_trend.add_trace(go.Scatter(
                x=daily_stats.index,
                y=daily_stats['REJECTED'],
                mode='lines+markers',
                name='Rejected',
                line=dict(color='#dc3545', width=3),
                fill='tozeroy'
            ))
        
        fig_trend.update_layout(
            title='Approval vs Rejection Trend',
            xaxis_title='Date',
            yaxis_title='Number of Audits',
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Audit Log Display
        st.markdown("### 📜 Recent Audit Logs")
        
        for i, audit in enumerate(audits, 1):
            decision_class = "audit-approved" if audit['decision'] == "APPROVED" else "audit-rejected"
            icon = "✅" if audit['decision'] == "APPROVED" else "🚫"
            
            # Determine risk level
            if audit['decision'] == "REJECTED":
                reasoning_lower = audit['reasoning'].lower()
                if 'budget' in reasoning_lower or 'limit' in reasoning_lower:
                    risk_badge = "🔴 HIGH RISK"
                elif 'whitelist' in reasoning_lower:
                    risk_badge = "🔴 CRITICAL"
                elif 'velocity' in reasoning_lower:
                    risk_badge = "🟡 MEDIUM RISK"
                else:
                    risk_badge = "🟡 MEDIUM RISK"
            else:
                risk_badge = "🟢 LOW RISK"
            
            with st.expander(
                f"{icon} {audit['vendor_name']} - {audit['amount']} MNEE - {audit['created_at'][:10]} | {risk_badge}", 
                expanded=(i == 1)
            ):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **Decision:** {audit['decision']}  
                    **Vendor:** {audit['vendor_name']}  
                    **Address:** `{audit['vendor_address']}`  
                    **Amount:** {audit['amount']} MNEE  
                    **Category:** {audit['category']}  
                    **AI Confidence:** {audit['ai_confidence']:.0%} ({(audit.get('ai_provider') or 'unknown').upper()})  
                    **Timestamp:** {audit['created_at']}
                    """)
                    
                    if audit.get('transaction_hash'):
                        st.markdown(f"**Tx Hash:** `{audit['transaction_hash']}`")
                
                with col2:
                    # Show decision badge
                    if audit['decision'] == "APPROVED":
                        st.success("✅ APPROVED")
                    else:
                        st.error("🚫 BLOCKED")
                
                # DETAILED REASONING (Expandable)
                st.markdown("---")
                st.markdown("### 📋 Detailed Reasoning & Audit Trail")
                
                # Show full reasoning
                st.info(audit['reasoning'])
                
                # Show original proposal (using checkbox - expanders can't be nested)
                if st.checkbox(f"📄 Show Original Proposal", key=f"proposal_{audit['id']}"):
                    st.code(audit.get('proposal_text', 'N/A'), language=None)
        
        # Export functionality
        st.markdown("---")
        st.markdown("### 💾 Export Data")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            df_export = pd.DataFrame(audits)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"mnee_audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("📭 No audit history yet. Submit a proposal to create the first entry!")

# ===================================
# TAB 4: Vendor Management
# ===================================

with tab4:
    st.markdown("## 👥 Vendor Management")
    
    try:
        vendors_data = db.client.table("whitelisted_vendors").select("*").execute()
        
        if vendors_data.data:
            st.markdown("### 📋 Whitelisted Vendors")
            
            # Convert to dataframe
            df_vendors = pd.DataFrame(vendors_data.data)
            
            # Display table
            df_display = df_vendors[['vendor_name', 'wallet_address', 'category', 'max_transaction_limit', 'is_active']].copy()
            df_display.columns = ['Vendor Name', 'Wallet Address', 'Category', 'Max Limit (MNEE)', 'Active']
            df_display['Max Limit (MNEE)'] = df_display['Max Limit (MNEE)'].apply(lambda x: f"{float(x):,.2f}")
            df_display['Active'] = df_display['Active'].apply(lambda x: "✅" if x else "❌")
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Vendor stats visualization
            st.markdown("### 📊 Vendor Distribution by Category")
            
            vendor_category_count = df_vendors['category'].value_counts()
            
            fig_vendor_dist = px.bar(
                x=vendor_category_count.index,
                y=vendor_category_count.values,
                labels={'x': 'Category', 'y': 'Number of Vendors'},
                title='Vendors per Category',
                color=vendor_category_count.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_vendor_dist, use_container_width=True)
            
            # Transaction limits analysis
            st.markdown("### 💰 Vendor Transaction Limits")
            
            fig_limits = px.bar(
                df_vendors.sort_values('max_transaction_limit', ascending=False),
                x='vendor_name',
                y='max_transaction_limit',
                color='category',
                title='Maximum Transaction Limits by Vendor',
                labels={'max_transaction_limit': 'Max Limit (MNEE)', 'vendor_name': 'Vendor'}
            )
            fig_limits.update_xaxes(tickangle=-45)
            st.plotly_chart(fig_limits, use_container_width=True)
            
        else:
            st.info("📭 No vendors in whitelist")
    
    except Exception as e:
        st.error(f"❌ Error loading vendor data: {e}")

# ===================================
# Footer
# ===================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p style='font-size: 1.2rem; font-weight: bold;'>🛡️ MNEE Sentinel - AI-Powered Treasury Guardian</p>
    <p>Built for MNEE Hackathon 2025 | Track: Programmable Finance & Automation</p>
    <p style='font-size: 0.9rem; margin-top: 1rem;'>
        Solving Real Coordination Problems Through AI-Driven Treasury Management
    </p>
    <p style='font-size: 0.8rem; color: #999; margin-top: 0.5rem;'>
        AI Provider: <strong>{}</strong> | Database: Supabase | Blockchain: Ethereum
    </p>
</div>
""".format((ai_provider or 'groq').upper()), unsafe_allow_html=True)
