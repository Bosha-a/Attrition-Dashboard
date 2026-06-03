import pandas as pd
import plotly.express as px
import streamlit as st


def financial_page(df: pd.DataFrame):
    st.title("Financial Analysis")
    st.write("Review compensation and tenure patterns by attrition status.")

    left_col, right_col = st.columns(2)

    income_fig = px.box(
        df,
        x="Attrition",
        y="Monthly Income",
        color="Attrition",
        color_discrete_map={"Stayed": "#636EFA", "Left": "#EF553B"},
        title="Monthly Income by Attrition",
    )
    income_fig.update_layout(template="plotly_white")

    left_col.plotly_chart(income_fig, use_container_width=True)

    tenure_fig = px.histogram(
        df,
        x="Company Tenure",
        color="Attrition",
        barmode="group",
        color_discrete_map={"Stayed": "#636EFA", "Left": "#EF553B"},
        title="Company Tenure Distribution by Attrition",
    )
    tenure_fig.update_layout(template="plotly_white", xaxis_title="Company Tenure")
    
    right_col.plotly_chart(tenure_fig, use_container_width=True)