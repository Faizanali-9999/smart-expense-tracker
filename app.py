import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import date

from database import (
    add_expense,
    delete_expense,
    get_expenses,
    get_monthly_total,
    init_db,
    update_expense,
)

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide",
)

init_db()

CATEGORIES = [
    "Food", "Travel", "Shopping", "Education",
    "Bills", "Health", "Entertainment", "Other"
]

st.title("💰 Smart Expense Tracker")
st.caption("Track spending, understand your habits, and stay within your budget.")

with st.sidebar:
    st.header("⚙️ Settings")
    monthly_budget = st.number_input(
        "Monthly budget (₹)",
        min_value=0.0,
        value=10000.0,
        step=500.0,
        help="This budget is used for the current month's summary.",
    )
    st.divider()
    st.write("**About this app**")
    st.write("A beginner-friendly Python project using Streamlit and SQLite.")

today = date.today()
all_expenses = get_expenses()
df = pd.DataFrame(all_expenses)

if not df.empty:
    df["date"] = pd.to_datetime(df["date"]).dt.date
    current_month_df = df[
        (pd.to_datetime(df["date"]).dt.year == today.year)
        & (pd.to_datetime(df["date"]).dt.month == today.month)
    ].copy()
else:
    current_month_df = pd.DataFrame(columns=["id", "date", "category", "description", "amount"])

month_total = float(current_month_df["amount"].sum()) if not current_month_df.empty else 0.0
remaining = monthly_budget - month_total
transaction_count = len(current_month_df)

c1, c2, c3 = st.columns(3)
c1.metric("Spent this month", f"₹{month_total:,.2f}")
c2.metric("Monthly budget remaining", f"₹{remaining:,.2f}", delta=f"{remaining:,.2f}")
c3.metric("Transactions this month", transaction_count)

if monthly_budget > 0:
    progress = min(month_total / monthly_budget, 1.0)
    st.progress(progress, text=f"Budget used: {month_total / monthly_budget:.1%}")
if remaining < 0:
    st.error(f"You are ₹{abs(remaining):,.2f} over your monthly budget.")
elif monthly_budget > 0 and remaining < monthly_budget * 0.2:
    st.warning("Your remaining budget is getting low.")
else:
    st.success("You're within your monthly budget.")

st.divider()
left, right = st.columns([1, 1])

with left:
    st.subheader("➕ Add an expense")
    with st.form("add_expense_form", clear_on_submit=True):
        expense_date = st.date_input("Date", value=today)
        category = st.selectbox("Category", CATEGORIES)
        description = st.text_input("Description", placeholder="e.g. Lunch at college")
        amount = st.number_input("Amount (₹)", min_value=0.01, value=100.0, step=10.0)
        submitted = st.form_submit_button("Add expense", use_container_width=True)

        if submitted:
            add_expense(expense_date.isoformat(), category, description.strip(), amount)
            st.success("Expense added.")
            st.rerun()

with right:
    st.subheader("📊 Spending by category")
    if not current_month_df.empty:
        category_totals = (
            current_month_df.groupby("category", as_index=False)["amount"]
            .sum()
            .sort_values("amount", ascending=False)
        )
        fig = px.pie(
            category_totals,
            names="category",
            values="amount",
            hole=0.55,
            title="Current month",
        )
        fig.update_layout(margin=dict(t=45, b=10, l=10, r=10), legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add an expense to see your category breakdown.")

st.divider()
st.subheader("📈 Recent spending")
if not current_month_df.empty:
    daily = current_month_df.groupby("date", as_index=False)["amount"].sum()
    fig = px.bar(daily, x="date", y="amount", labels={"date": "Date", "amount": "Amount (₹)"})
    fig.update_layout(margin=dict(t=20, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No expenses recorded for this month yet.")

st.divider()
st.subheader("🧾 Expense history")
if df.empty:
    st.info("No expenses yet. Add your first expense above.")
else:
    display_df = df.sort_values(["date", "id"], ascending=[False, False]).copy()
    display_df["date"] = pd.to_datetime(display_df["date"]).dt.date
    st.dataframe(
        display_df[["id", "date", "category", "description", "amount"]].rename(
            columns={
                "id": "ID",
                "date": "Date",
                "category": "Category",
                "description": "Description",
                "amount": "Amount (₹)",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    csv = display_df.drop(columns=["id"]).to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download expenses as CSV",
        data=csv,
        file_name="my_expenses.csv",
        mime="text/csv",
    )

    with st.expander("Edit or delete an expense"):
        expense_ids = display_df["id"].astype(int).tolist()
        selected_id = st.selectbox("Choose expense ID", expense_ids)
        selected = display_df[display_df["id"] == selected_id].iloc[0]

        with st.form("edit_expense_form"):
            edit_date = st.date_input("Edit date", value=selected["date"])
            edit_category = st.selectbox(
                "Edit category",
                CATEGORIES,
                index=CATEGORIES.index(selected["category"]) if selected["category"] in CATEGORIES else 0,
            )
            edit_description = st.text_input("Edit description", value=str(selected["description"]))
            edit_amount = st.number_input(
                "Edit amount (₹)",
                min_value=0.01,
                value=float(selected["amount"]),
                step=10.0,
            )
            save = st.form_submit_button("Save changes")
            if save:
                update_expense(
                    int(selected_id),
                    edit_date.isoformat(),
                    edit_category,
                    edit_description.strip(),
                    edit_amount,
                )
                st.success("Expense updated.")
                st.rerun()

        if st.button("🗑️ Delete selected expense", type="secondary"):
            delete_expense(int(selected_id))
            st.success("Expense deleted.")
            st.rerun()

st.caption("Your expense records are stored locally in an SQLite database file named expenses.db.")
