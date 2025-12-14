import streamlit as st
import pandas as pd
import plotly.express as px

# We make sure the user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.error("You must be logged in.")
    st.stop()

st.title("💻 IT Tickets Dashboard")

# We load the data once and keep it in memory
if "df_it" not in st.session_state:
    st.session_state.df_it = pd.read_csv("DATA(csv)/it_tickets_1000.csv")

df = st.session_state.df_it

st.success("IT tickets loaded successfully!")
st.dataframe(df, use_container_width=True)

# Quick overview
st.subheader("Total Tickets")
st.metric("Total", df.shape[0])

st.subheader("Analytics")

tab1, tab2, tab3, tab4 = st.tabs([
    "Ticket Types",
    "Severity",
    "Status",
    "Reported By"
])

with tab1:
    type_counts = df["ticket_type"].value_counts().reset_index()
    type_counts.columns = ["ticket_type", "count"]

    fig_type = px.bar(
        type_counts,
        x="ticket_type",
        y="count",
        text="count",
        color="ticket_type"
    )
    st.plotly_chart(fig_type, use_container_width=True)

with tab2:
    fig_sev = px.pie(
        df,
        names="severity",
        hole=0.5
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
    fig_rep = px.treemap(
        df,
        path=["reported_by"]
    )
    st.plotly_chart(fig_rep, use_container_width=True)

st.subheader("Manage IT Tickets")

# Here we add a new ticket
with st.expander("➕ Add New Ticket"):
    with st.form("add_it"):
        date = st.date_input("Date")
        ticket_type = st.text_input("Ticket Type")
        severity = st.selectbox("Severity", sorted(df["severity"].unique()))
        status = st.selectbox("Status", sorted(df["status"].unique()))
        description = st.text_area("Description")
        reported_by = st.text_input("Reported By")

        add_btn = st.form_submit_button("Add Ticket")

    if add_btn:
        new_row = {
            "date": str(date),
            "ticket_type": ticket_type,
            "severity": severity,
            "status": status,
            "description": description,
            "reported_by": reported_by
        }
        st.session_state.df_it = pd.concat(
            [st.session_state.df_it, pd.DataFrame([new_row])],
            ignore_index=True
        )
        st.success("Ticket added successfully!")
        st.experimental_rerun()

# Here we update an existing ticket
with st.expander("✏️ Update Ticket"):
    index = st.number_input(
        "Row index to update",
        min_value=0,
        max_value=len(df) - 1,
        step=1
    )

    row = df.loc[index]

    severity_options = sorted(df["severity"].unique())
    status_options = sorted(df["status"].unique())

    with st.form("update_it"):
        upd_date = st.date_input("Date", pd.to_datetime(row["date"]))
        upd_type = st.text_input("Ticket Type", row["ticket_type"])
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

        upd_btn = st.form_submit_button("Update Ticket")

    if upd_btn:
        st.session_state.df_it.loc[index] = [
            str(upd_date),
            upd_type,
            upd_sev,
            upd_status,
            upd_desc,
            upd_report
        ]
        st.success("Ticket updated successfully!")
        st.experimental_rerun()

# Here we delete a ticket
with st.expander("🗑️ Delete Ticket"):
    del_index = st.number_input(
        "Row index to delete",
        min_value=0,
        max_value=len(df) - 1,
        step=1
    )

    if st.button("Delete Ticket"):
        st.session_state.df_it = (
            st.session_state.df_it
            .drop(del_index)
            .reset_index(drop=True)
        )
        st.success("Ticket deleted successfully!")
        st.experimental_rerun()

         #AI Assistant                                       
from services.ai_widget import ai_assistant_box

st.divider()
ai_assistant_box()

