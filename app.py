import pandas as pd
import plotly.express as px
import streamlit as st

from demographic import demographic_page
from diagnostic import diagnostic_page
from financial import financial_page

st.set_page_config(
    page_title="Employee Attrition Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data():
    return pd.read_csv("Attrition.csv")


df = load_data()


st.sidebar.title("Dashboard Menu")
page = st.sidebar.radio(
    "Navigate to",
    ["Overview", "Demographic", "Diagnostic", "Financial"],
)
st.sidebar.caption("Use the menu to explore each dashboard.")


def overview_page(dataframe: pd.DataFrame):
    st.title("Employee Attrition Dashboard")
    st.write("Overview of attrition across the workforce.")

    total_employees = len(dataframe)
    stayed_count = dataframe["Attrition"].value_counts().get("Stayed", 0)
    left_count = dataframe["Attrition"].value_counts().get("Left", 0)

    stayed_percentage = (stayed_count / total_employees) * 100 if total_employees else 0
    left_percentage = (left_count / total_employees) * 100 if total_employees else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Employees", total_employees)
    col2.metric("Stayed %", f"{stayed_percentage:.2f}%")
    col3.metric("Left %", f"{left_percentage:.2f}%")

    if "Monthly Income" in dataframe.columns:
        avg_income = dataframe["Monthly Income"].mean()
        col4.metric("Avg Monthly Income", f"${avg_income:,.2f}")
    else:
        col4.metric("Avg Monthly Income", "N/A")

    # job role chart
    job_role_fig = px.histogram(df, x="Job Role", color="Attrition", barmode="group", text_auto=".1f", color_discrete_map={"Stayed": "#636EFA", "Left": "#EF553B"}, title="Attrition by Job Role (%)")

    st.plotly_chart(job_role_fig, use_container_width=True)


    temp = df.groupby(["Performance Rating", "Attrition"]).size().reset_index(name="Count")
    temp["percent"] = temp.groupby("Performance Rating")["Count"].transform(
        lambda x: x / x.sum() * 100
    )

    Performance_fig = px.bar(
    temp,
    x="Performance Rating",
    y="percent",
    color="Attrition",
    barmode="group",
    text_auto=".1f",
    color_discrete_map={"Stayed": "#636EFA", "Left": "#EF553B"},
    title="Attrition Rate by Performance Rating (%)"
    )

    Performance_fig.update_layout(
        xaxis_title="Performance Rating",
        yaxis_title="Percentage (%)",
        template="plotly_white"
    )

    st.plotly_chart(Performance_fig, use_container_width=True)



if page == "Overview":
    overview_page(df)
elif page == "Demographic":
    demographic_page(df)
elif page == "Diagnostic":
    diagnostic_page(df)
else:
    financial_page(df)