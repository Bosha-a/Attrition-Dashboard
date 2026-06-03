import pandas as pd
import plotly.express as px
import streamlit as st


def demographic_page(df: pd.DataFrame):
    st.title("Demographic Analysis")
    st.write("Explore how attrition varies across employee demographics.")

    col1, col2 = st.columns(2)

    # First chart: Attrition by Gender
    gender_fig = px.histogram(
        df,
        x="Gender",
        color="Attrition",
        barmode="group",
        text_auto=".1f",
        color_discrete_map={"Stayed": "#636EFA", "Left": "#EF553B"},
        title="Attrition by Gender (%)",
    )
    gender_fig.update_layout(template="plotly_white")

    col1.plotly_chart(gender_fig, use_container_width=True)


    # Second chart: Attrition by Job Level
    temp = df.groupby(["Job Level", "Attrition"]).size().reset_index(name="Count")
    temp["percent"] = temp.groupby("Job Level")["Count"].transform(
        lambda x: x / x.sum() * 100
    )

    job_level_fig = px.bar(
        temp,
        x="Job Level",
        y="percent",
        color="Attrition",
        barmode="group",
        text_auto=".1f",
        color_discrete_map={"Stayed": "#636EFA", "Left": "#EF553B"},
        title="Attrition Rate by Job Level (%)",
    )

    job_level_fig.update_layout(
        xaxis_title="Job Level",
        yaxis_title="Percentage (%)",
        legend_title="Attrition Status",
        template="plotly_white",
    )

    col2.plotly_chart(job_level_fig, use_container_width=True)
