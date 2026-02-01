import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------
# Page config
# --------------------
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------
# Global styles
# --------------------
st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}

    .metric-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.25rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.03);
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------
# Title
# --------------------
st.title("Personal Finance Dashboard")
st.caption("A simple, clear overview of your monthly finances.")

# --------------------
# Session State Init
# --------------------
if "expenses" not in st.session_state:
    st.session_state.expenses = {
        "Rent": 15000.0,
        "Food": 8000.0,
        "Utilities": 3000.0,
        "Transport": 4000.0,
        "Entertainment": 2000.0,
        "Other": 1000.0,
    }

# --------------------
# Sidebar Inputs
# --------------------
st.sidebar.header("Monthly Setup")

income = st.sidebar.number_input(
    "Income",
    min_value=0.0,
    value=50000.0
)

savings_goal = st.sidebar.number_input(
    "Savings Goal",
    min_value=0.0,
    value=10000.0
)

st.sidebar.divider()
st.sidebar.subheader("Expenses")

for category in st.session_state.expenses:
    st.session_state.expenses[category] = st.sidebar.number_input(
        category,
        min_value=0.0,
        value=st.session_state.expenses[category],
        key=category
    )

# --------------------
# Calculations
# --------------------
expense_df = pd.DataFrame(
    st.session_state.expenses.items(),
    columns=["Category", "Amount"]
)

total_expenses = expense_df["Amount"].sum()
remaining = income - total_expenses
savings_rate = (remaining / income * 100) if income > 0 else 0

# --------------------
# Metrics (clean & modern)
# --------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Expenses", f"{total_expenses:,.2f}")

with col2:
    st.metric("Remaining Balance", f"{remaining:,.2f}")

with col3:
    st.metric("Savings Rate", f"{savings_rate:.1f}%")

st.divider()

# --------------------
# Charts
# --------------------
left, right = st.columns(2)

# ---- Donut Pie Chart
with left:
    st.markdown('<div class="section-title">Expense Breakdown</div>', unsafe_allow_html=True)

    filtered_df = expense_df[expense_df["Amount"] > 0]

    if filtered_df.empty:
        st.info("No expenses to display.")
    else:
        fig1, ax1 = plt.subplots(figsize=(5, 5))
        wedges, texts, autotexts = ax1.pie(
            filtered_df["Amount"],
            labels=filtered_df["Category"],
            autopct=lambda p: f"{p:.1f}%" if p >= 4 else "",
            startangle=90,
            wedgeprops=dict(width=0.4)
        )
        ax1.axis("equal")
        st.pyplot(fig1)

# ---- Income vs Expenses Bar
with right:
    st.markdown('<div class="section-title">Income vs Expenses</div>', unsafe_allow_html=True)

    fig2, ax2 = plt.subplots(figsize=(5, 5))
    ax2.bar(
        ["Income", "Expenses"],
        [income, total_expenses]
    )
    ax2.set_ylabel("Amount")
    st.pyplot(fig2)

# --------------------
# Savings Goal Status
# --------------------
st.divider()
st.markdown('<div class="section-title">Savings Goal Status</div>', unsafe_allow_html=True)

if remaining >= savings_goal:
    st.success("🎉 You’re on track to meet your savings goal this month.")
else:
    shortfall = savings_goal - remaining
    st.warning(
        f"⚠️ You need an additional {shortfall:,.2f} to reach your savings goal."
    )
