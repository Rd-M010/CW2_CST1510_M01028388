import streamlit as st
import pandas as pd
import plotly.express as px

from models.security_incident import SecurityIncident


# We first check if the user is logged in
# If not, we block access to this page
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in.")
    st.stop()


st.title("🛡️ Cyber Security Dashboard")


# We load all data directly from the CSV file
df = pd.read_csv("DATA/cyber_incidents_1000.csv")


# We convert each row into a SecurityIncident object
incidents = []

for index, row in df.iterrows():
    incident = SecurityIncident(
        incident_id=index,
        incident_type=row["incident_type"],
        severity=row["severity"],
        status=row["status"],
        description=row["description"],
    )
    incidents.append(incident)


# We rebuild a clean DataFrame from our objects
data = []

for incident in incidents:
    data.append({
        "id": incident.get_id(),
        "incident_type": incident.get_incident_type(),
        "severity": incident.get_severity(),
        "status": incident.get_status(),
        "description": incident.get_description(),
    })

df_view = pd.DataFrame(data)


# We display all incidents
st.subheader("All Cyber Incidents")
st.success("All incidents loaded successfully.")
st.dataframe(df_view, use_container_width=True)


# We show the total number of incidents
st.subheader("Total Incidents")
st.metric("Total", len(df_view))


# -------------------
# ANALYTICS SECTION
# -------------------

st.subheader("Analytics")

tab1, tab2, tab3 = st.tabs([
    "Incident Types",
    "Severity",
    "Status"
])

with tab1:
    type_counts = df_view["incident_type"].value_counts().reset_index()
    type_counts.columns = ["incident_type", "count"]

    fig_type = px.bar(
        type_counts,
        x="incident_type",
        y="count",
        text="count"
    )
    st.plotly_chart(fig_type, use_container_width=True)

with tab2:
    fig_sev = px.pie(
        df_view,
        names="severity",
        hole=0.4
    )
    st.plotly_chart(fig_sev, use_container_width=True)

with tab3:
    status_counts = df_view["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]

    fig_status = px.bar(
        status_counts,
        x="count",
        y="status",
        orientation="h",
        text="count"
    )
    st.plotly_chart(fig_status, use_container_width=True)


# -------------------
# CRUD SECTION
# -------------------

st.subheader("Manage Cyber Incidents")


# CREATE
with st.expander("➕ Add New Incident"):
    with st.form("add_incident_form"):
        incident_type = st.text_input("Incident Type")
        severity = st.selectbox("Severity", df_view["severity"].unique())
        status = st.selectbox("Status", df_view["status"].unique())
        description = st.text_area("Description")

        create_btn = st.form_submit_button("Create Incident")

    if create_btn:
        new_incident = SecurityIncident(
            incident_id=len(df),
            incident_type=incident_type,
            severity=severity,
            status=status,
            description=description,
        )

        new_row = {
            "incident_type": new_incident.get_incident_type(),
            "severity": new_incident.get_severity(),
            "status": new_incident.get_status(),
            "description": new_incident.get_description(),
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("DATA/cyber_incidents_1000.csv", index=False)

        st.success("Incident created successfully.")
        st.experimental_rerun()


# UPDATE
with st.expander("✏️ Update Incident"):
    update_id = st.selectbox("Select incident ID to update", df_view["id"].tolist())

    incident_to_update = next(
        inc for inc in incidents if inc.get_id() == update_id
    )

    with st.form("update_incident_form"):
        upd_type = st.text_input("Incident Type", incident_to_update.get_incident_type())
        upd_sev = st.selectbox(
            "Severity",
            df_view["severity"].unique(),
            index=list(df_view["severity"].unique()).index(incident_to_update.get_severity())
        )
        upd_status = st.selectbox(
            "Status",
            df_view["status"].unique(),
            index=list(df_view["status"].unique()).index(incident_to_update.get_status())
        )
        upd_desc = st.text_area("Description", incident_to_update.get_description())

        update_btn = st.form_submit_button("Update Incident")

    if update_btn:
        df.loc[update_id, "incident_type"] = upd_type
        df.loc[update_id, "severity"] = upd_sev
        df.loc[update_id, "status"] = upd_status
        df.loc[update_id, "description"] = upd_desc

        df.to_csv("DATA/cyber_incidents_1000.csv", index=False)

        st.success("Incident updated successfully.")
        st.experimental_rerun()


# DELETE
with st.expander("🗑️ Delete Incident"):
    delete_id = st.selectbox("Select incident ID to delete", df_view["id"].tolist())

    if st.button("Delete Incident"):
        df = df.drop(index=delete_id).reset_index(drop=True)
        df.to_csv("DATA/cyber_incidents_1000.csv", index=False)

        st.success("Incident deleted successfully.")
        st.experimental_rerun()


# -------------------
# AI INTEGRATION
# -------------------

st.subheader("Incident → AI Analysis")

selected_id = st.selectbox(
    "Select incident ID for AI analysis",
    df_view["id"].tolist()
)

selected_incident = next(
    inc for inc in incidents if inc.get_id() == selected_id
)

st.session_state["ai_domain"] = "Cyber Security"
st.session_state["ai_context_title"] = f"Cyber Incident ID {selected_id}"
st.session_state["ai_context_description"] = selected_incident.get_description()

st.info(
    "This incident is now available in the AI Assistant page for analysis."
)
