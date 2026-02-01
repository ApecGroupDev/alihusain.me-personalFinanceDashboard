import streamlit as st
import pandas as pd
import altair as alt

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide"
)

# -----------------------
# APP HEADER
# -----------------------
st.markdown(
    """
    <style>
    .big-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="big-title">💰 Personal Finance Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Track your monthly income, expenses, and savings at a glance</div>', unsafe_allow_html=True)

# -----------------------
# SIDEBAR — INPUTS
# -----------------------
st.sidebar.header("🧾 Monthly Inputs")

income = st.sidebar.number_input(
    "Monthly Income",
    min_value=0.0,
    value=50000.0,
    step=1000.0
)

st.sidebar.subheader("Expenses")

rent = st.sidebar.number_input("Rent", min_value=0.0, value=15000.0, step=500.0)
food = st.sidebar.number_input("Food", min_value=0.0, value=8000.0, step=500.0)
transport = st.sidebar.number_input("Transport", min_value=0.0, value=4000.0, step=500.0)
utilities = st.sidebar.number_input("Utilities", min_value=0.0, value=3000.0, step=500.0)
entertainment = st.sidebar.number_input("Entertainment", min_value=0.0, value=2000.0, step=500.0)

# -----------------------
# DATA PREP
# -----------------------
data = {
    "Category": ["Rent", "Food", "Transport", "Utilities", "Entertainment"],
    "Amount": [rent, food, transport, utilities, entertainment],
}

df = pd.DataFrame(data)

# Remove zero-value categories (important!)
df = df[df["Amount"] > 0]

total_expenses = df["Amount"].sum()
savings = income - total_expenses

# -----------------------
# KPI METRICS
# -----------------------
st.markdown("### 📊 Monthly Summary")

m1, m2, m3 = st.columns(3)

m1.metric("Income", f"₱{income:,.0f}")
m2.metric("Expenses", f"₱{total_expenses:,.0f}")
m3.metric(
    "Savings",
    f"₱{savings:,.0f}",
    delta=f"{(savings / income * 100):.1f}%" if income > 0 else None
)

st.divider()

# -----------------------
# CHARTS
# -----------------------
left, right = st.columns([1, 1.2])

# ---- LEFT: DONUT PIE ----
with left:
    st.subheader("🧁 Expense Breakdown")

    if df.empty:
        st.info("No expenses to display.")
    else:
        df["Percent"] = (df["Amount"] / df["Amount"].sum() * 100).round(1)

        pie = (
            alt.Chart(df)
            .mark_arc(innerRadius=65, cornerRadius=6)
            .encode(
                theta=alt.Theta(field="Amount", type="quantitative"),
                color=alt.Color(
                    field="Category",
                    type="nominal",
                    legend=alt.Legend(title="Category", orient="bottom")
                ),
                tooltip=[
                    alt.Tooltip("Category:N"),
                    alt.Tooltip("Amount:Q", format=",.0f"),
                    alt.Tooltip("Percent:Q", format=".1f")
                ],
            )
            .properties(height=320)
        )

        st.altair_chart(pie, use_container_width=True)

# ---- RIGHT: BAR CHART ----
with right:
    st.subheader("📉 Expense Comparison")

    if df.empty:
        st.info("No data to show.")
    else:
        bar = (
            alt.Chart(df)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
            .encode(
                x=alt.X("Category:N", sort="-y", title=None),
                y=alt.Y("Amount:Q", title="Amount"),
                color=alt.Color(
                    "Category:N",
                    legend=None
                ),
                tooltip=[
                    alt.Tooltip("Category:N"),
                    alt.Tooltip("Amount:Q", format=",.0f")
                ],
            )
            .properties(height=320)
        )

        st.altair_chart(bar, use_container_width=True)

# -----------------------
# PERSONAL TOUCH ✨
# -----------------------
st.divider()

if savings < 0:
    st.error("⚠️ You're spending more than you earn. Time to rebalance.")
elif savings < income * 0.2:
    st.warning("🟡 You're saving a bit — try pushing toward 20% if possible.")
else:
    st.success("🟢 Great job! Your savings rate is healthy.")

st.caption("Built with ❤️ using Streamlit & Altair")
