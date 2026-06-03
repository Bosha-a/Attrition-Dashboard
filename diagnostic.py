import pandas as pd
import plotly.express as px
import streamlit as st


def diagnostic_page(df: pd.DataFrame):
    st.title("Diagnostic Analysis")
    st.write("Inspect operational signals that may be linked to attrition.")

    left_col, right_col = st.columns(2)

    temp = df.groupby(["Overtime", "Attrition"]).size().reset_index(name="Count")

    temp["percent"] = temp.groupby("Overtime")["Count"].transform(
        lambda x: x / x.sum() * 100
    )

    overtime_fig = px.bar(
        temp,
        x="Overtime",
        y="percent",
        color="Attrition",
        barmode="group",
        text_auto=".1f",
        color_discrete_map={"Stayed": "#636EFA", "Left": "#EF553B"},
        title="Attrition Rate by Overtime (%)"
    )

    overtime_fig.update_layout(
        xaxis_title="Overtime",
        yaxis_title="Percentage (%)",
        legend_title="Attrition Status",
        template="plotly_white"
    )

    # Work-Life Balance vs Attrition
    temp = df.groupby(["Work-Life Balance", "Attrition"]).size().reset_index(name="Count")
    temp["percent"] = temp.groupby("Work-Life Balance")["Count"].transform(
        lambda x: x / x.sum() * 100
    )

    work_life_fig = px.bar(
        temp,
        x="Work-Life Balance",
        y="percent",
        color="Attrition",
        barmode="group",
        text_auto=".1f",
        color_discrete_map={"Stayed": "#636EFA", "Left": "#EF553B"},
        title="Attrition Rate by Work-Life Balance",
    )
    work_life_fig.update_layout(
        xaxis_title="Work-Life Balance",
        yaxis_title="Percentage (%)",
        legend_title="Attrition Status",
        template="plotly_white",
    )

    years_fig = px.box(
        df,
        x="Attrition",
        y="Years at Company",
        color="Attrition",
        color_discrete_map={"Stayed": "#636EFA", "Left": "#EF553B"},
        title="Years at Company vs Attrition",
    )
    years_fig.update_layout(template="plotly_white")

    left_col.plotly_chart(overtime_fig, use_container_width=True)
    right_col.plotly_chart(work_life_fig, use_container_width=True)

    st.plotly_chart(years_fig, use_container_width=True)