import streamlit as st
import pandas as pd
import plotly.express as px

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.error("You must be logged in.")
    st.stop()

st.title("📚 Data Science Dashboard")

if "df_ds" not in st.session_state:
    st.session_state.df_ds = pd.read_csv("DATA(csv)/datasets_metadata_1000.csv")

df = st.session_state.df_ds

st.success("Dataset metadata loaded successfully!")
st.dataframe(df, use_container_width=True)

st.subheader("Total Datasets")
st.metric("Total", df.shape[0])

st.subheader("Analytics")

tab1, tab2, tab3, tab4 = st.tabs([
    "Dataset Types",
    "Severity",
    "Status",
    "Reported By"
])

with tab1:
    type_counts = df["dataset_type"].value_counts().reset_index()
    type_counts.columns = ["dataset_type", "count"]

    fig_type = px.bar(
        type_counts,
        x="dataset_type",
        y="count",
        text="count",
        color="dataset_type"
    )
    st.plotly_chart(fig_type, use_container_width=True)

with tab2:
    fig_sev = px.treemap(
        df,
        path=["severity"]
    )
    st.plotly_chart(fig_sev, use_container_width=True)

with tab3:
    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]

    fig_status = px.bar(
        status_counts,
        x="count",
        y="status",
        orientation="h",
        text="count",
        color="status"
    )
    st.plotly_chart(fig_status, use_container_width=True)

with tab4:
    fig_rep = px.pie(
        df,
        names="reported_by",
        hole=0.5
    )
    st.plotly_chart(fig_rep, use_container_width=True)

st.subheader("Manage Datasets")

with st.expander("➕ Add New Dataset"):
    with st.form("add_dataset"):
        date = st.date_input("Date")
        dataset_type = st.text_input("Dataset Type")
        severity = st.selectbox("Severity", sorted(df["severity"].unique()))
        status = st.selectbox("Status", sorted(df["status"].unique()))
        description = st.text_area("Description")
        reported_by = st.text_input("Reported By")

        add_btn = st.form_submit_button("Add Dataset")

    if add_btn:
        new_row = {
            "date": str(date),
            "dataset_type": dataset_type,
            "severity": severity,
            "status": status,
            "description": description,
            "reported_by": reported_by
        }
        st.session_state.df_ds = pd.concat(
            [st.session_state.df_ds, pd.DataFrame([new_row])],
            ignore_index=True
        )
        st.success("Dataset added successfully!")
        st.experimental_rerun()

with st.expander("✏️ Update Dataset"):
    index = st.number_input(
        "Row index to update",
        min_value=0,
        max_value=len(df) - 1,
        step=1
    )

    row = df.loc[index]

    severity_options = sorted(df["severity"].unique())
    status_options = sorted(df["status"].unique())

    with st.form("update_dataset"):
        upd_date = st.date_input("Date", pd.to_datetime(row["date"]))
        upd_type = st.text_input("Dataset Type", row["dataset_type"])
        upd_sev = st.selectbox(
            "Severity",
            severity_options,
            index=severity_options.index(row["severity"])
        )
        upd_status = st.selectbox(
            "Status",
            status_options,
            index=status_options.index(row["status"])
        )
        upd_desc = st.text_area("Description", row["description"])
        upd_report = st.text_input("Reported By", row["reported_by"])

        upd_btn = st.form_submit_button("Update Dataset")

    if upd_btn:
        st.session_state.df_ds.loc[index] = [
            str(upd_date),
            upd_type,
            upd_sev,
            upd_status,
            upd_desc,
            upd_report
        ]
        st.success("Dataset updated successfully!")
        st.experimental_rerun()

with st.expander("🗑️ Delete Dataset"):
    del_index = st.number_input(
        "Row index to delete",
        min_value=0,
        max_value=len(df) - 1,
        step=1
    )

    if st.button("Delete Dataset"):
        st.session_state.df_ds = (
            st.session_state.df_ds
            .drop(del_index)
            .reset_index(drop=True)
        )
        st.success("Dataset deleted successfully!")
        st.experimental_rerun()

         #AI Assistant                                       
from services.ai_widget import ai_assistant_box

st.divider()
ai_assistant_box()
