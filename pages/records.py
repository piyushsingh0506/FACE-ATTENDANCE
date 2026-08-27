import streamlit as st
import pandas as pd

from database import (
    get_attendance,
    get_notifications
)


# ==========================================================
# ATTENDANCE & NOTIFICATIONS RECORDS
# ==========================================================

def show_records():

    st.header(
        "📋 Records & Activity"
    )

    tab1, tab2 = st.tabs(["📋 Attendance Records", "📱 Notification History"])

    # ------------------------------------------------------
    # TAB 1: ATTENDANCE RECORDS
    # ------------------------------------------------------

    with tab1:

        rows = get_attendance()

        if not rows:

            st.info(
                "No attendance records found."
            )

        else:

            data = []

            for row in rows:

                data.append({
                    "ID": row["id"],
                    "Person ID": row["person_id"],
                    "Name": row["name"],
                    "Phone": row["phone_number"] or "N/A",
                    "Department": row["department"],
                    "Date": row["date"],
                    "Time": row["time"],
                    "Status": row["status"],
                    "Distance": f"{row['distance']:.4f}" if row['distance'] is not None else "N/A"
                })

            df = pd.DataFrame(data)

            # FILTERS
            col1, col2 = st.columns(2)

            with col1:

                search = st.text_input(
                    "🔍 Search by Name or ID",
                    key="search_att"
                )

            with col2:

                dates = sorted(
                    df["Date"].unique(),
                    reverse=True
                )

                selected_date = st.selectbox(
                    "📅 Filter by date",
                    ["All"] + list(dates),
                    key="date_att"
                )

            # SEARCH FILTER
            if search:

                search_lower = search.lower()

                df = df[
                    df["Name"]
                    .fillna("")
                    .str.lower()
                    .str.contains(search_lower)
                    |
                    df["Person ID"]
                    .fillna("")
                    .str.lower()
                    .str.contains(search_lower)
                ]

            # DATE FILTER
            if selected_date != "All":

                df = df[
                    df["Date"] == selected_date
                ]

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # CSV EXPORT
            csv = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇️ Export Attendance CSV",
                data=csv,
                file_name="attendance_records.csv",
                mime="text/csv",
                use_container_width=True
            )

    # ------------------------------------------------------
    # TAB 2: NOTIFICATIONS HISTORY
    # ------------------------------------------------------

    with tab2:

        notif_rows = get_notifications(limit=200)

        if not notif_rows:

            st.info(
                "No notifications sent yet. When people are recognized, SMS/WhatsApp alert logs will appear here."
            )

        else:

            notif_data = []

            for nrow in notif_rows:

                notif_data.append({
                    "ID": nrow["id"],
                    "Person ID": nrow["person_id"] or "N/A",
                    "Recipient": nrow["recipient_name"] or "Unknown",
                    "Phone Number": nrow["phone_number"],
                    "Channel": (nrow["channel"] or "sms").upper(),
                    "Status": nrow["status"],
                    "Message": nrow["message"],
                    "Details / Error": nrow["error_message"] or "Success",
                    "Sent At": nrow["sent_at"]
                })

            df_notif = pd.DataFrame(notif_data)

            st.dataframe(
                df_notif,
                use_container_width=True,
                hide_index=True
            )

            csv_notif = df_notif.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇️ Export Notification Logs CSV",
                data=csv_notif,
                file_name="notification_logs.csv",
                mime="text/csv",
                use_container_width=True
            )