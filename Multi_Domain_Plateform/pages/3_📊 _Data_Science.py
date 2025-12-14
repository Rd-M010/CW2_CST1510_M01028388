import streamlit as st
import pandas as pd
import plotly.express as px


# We block access if the user is not logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in.")
    st.stop()


st.title("📊 Data Science Dashboard")


# We load our Data Science CSV (single source of truth)
df = pd.read_csv("DATA/datasets_metadata_1000.csv")


# We show all records
st.subheader("All Datasets")
st.success("All datasets loaded successfully.")
st.dataframe(df, use_container_width=True)

st.subheader("Total Datasets")
st.metric("Total", len(df))


# We provide quick analytics
st.subheader("Analytics")
tab1, tab2, tab3, tab4 = st.tabs(["Dataset Types", "Severity", "Status", "Reported By"])

with tab1:
    type_counts = df["dataset_type"].value_counts().reset_index()
    type_counts.columns = ["dataset_type", "count"]
    fig_type = px.bar(type_counts, x="dataset_type", y="count", text="count")
    st.plotly_chart(fig_type, use_container_width=True)

with tab2:
    fig_sev = px.pie(df, names="severity", hole=0.4)
    st.plotly_chart(fig_sev, use_container_width=True)

with tab3:
    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]
    fig_status = px.bar(status_counts, x="count", y="status", orientation="h", text="count")
    st.plotly_chart(fig_status, use_container_width=True)

with tab4:
    rep_counts = df["reported_by"].value_counts().reset_index()
    rep_counts.columns = ["reported_by", "count"]
    fig_rep = px.bar(rep_counts, x="reported_by", y="count", text="count")
    st.plotly_chart(fig_rep, use_container_width=True)


# We manage the dataset records (CRUD)
st.subheader("Manage Datasets")


with st.expander("➕ Add Dataset"):
    with st.form("add_dataset"):
        date = st.date_input("Date")
        dataset_type = st.text_input("Dataset Type")
        severity = st.selectbox("Severity", df["severity"].unique())
        status = st.selectbox("Status", df["status"].unique())
        description = st.text_area("Description")
        reported_by = st.text_input("Reported By")
        create_btn = st.form_submit_button("Create Dataset")

    if create_btn:
        new_row = {
            "date": str(date),
            "dataset_type": dataset_type,
            "severity": severity,
            "status": status,
            "description": description,
            "reported_by": reported_by,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("DATA/datasets_metadata_1000.csv", index=False)
        st.success("Dataset created successfully.")
        st.rerun()


with st.expander("✏️ Update Dataset"):
    update_index = st.selectbox("Select dataset row", df.index.tolist())
    row = df.loc[update_index]

    with st.form("update_dataset"):
        upd_date = st.date_input("Date", pd.to_datetime(row["date"]))
        upd_type = st.text_input("Dataset Type", row["dataset_type"])

        sev_list = list(df["severity"].unique())
        status_list = list(df["status"].unique())

        upd_sev = st.selectbox("Severity", sev_list, index=sev_list.index(row["severity"]))
        upd_status = st.selectbox("Status", status_list, index=status_list.index(row["status"]))

        upd_desc = st.text_area("Description", row["description"])
        upd_rep = st.text_input("Reported By", row["reported_by"])
        update_btn = st.form_submit_button("Update Dataset")

    if update_btn:
        df.loc[update_index] = [
            str(upd_date),
            upd_type,
            upd_sev,
            upd_status,
            upd_desc,
            upd_rep,
        ]
        df.to_csv("DATA/datasets_metadata_1000.csv", index=False)
        st.success("Dataset updated successfully.")
        st.rerun()


with st.expander("🗑️ Delete Dataset"):
    delete_index = st.selectbox("Select dataset row to delete", df.index.tolist())

    if st.button("Delete Dataset"):
        df = df.drop(delete_index).reset_index(drop=True)
        df.to_csv("DATA/datasets_metadata_1000.csv", index=False)
        st.success("Dataset deleted successfully.")
        st.rerun()


# We link the selected record to the AI Assistant
st.subheader("Dataset → AI Analysis")

selected_index = st.selectbox("Select dataset for AI analysis", df.index.tolist())
selected_row = df.loc[selected_index]

st.session_state["ai_domain"] = "Data Science"
st.session_state["ai_context_title"] = f"Dataset Row {selected_index}"
st.session_state["ai_context_description"] = (
    f"Date: {selected_row['date']}. "
    f"Dataset type: {selected_row['dataset_type']}. "
    f"Severity: {selected_row['severity']}. "
    f"Status: {selected_row['status']}. "
    f"Reported by: {selected_row['reported_by']}. "
    f"Description: {selected_row['description']}"
)

st.info("This dataset is now available in the AI Assistant page.")
