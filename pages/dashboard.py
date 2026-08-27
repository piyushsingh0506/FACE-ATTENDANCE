import streamlit as st
import pandas as pd

from database import (
    get_total_people,
    get_today_attendance_count,
    get_attendance
)


def show_dashboard():

    st.header("🏠 Dashboard")

    st.write(
        "Face Recognition Attendance Overview"
    )

    total_people = get_total_people()

    today_count = get_today_attendance_count()

    attendance = get_attendance()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "👥 Registered People",
            total_people
        )

    with col2:

        st.metric(
            "📅 Today's Attendance",
            today_count
        )

    with col3:

        st.metric(
            "📋 Total Records",
            len(attendance)
        )

    st.markdown("---")

    st.subheader(
        "🕐 Recent Attendance"
    )

    if attendance:

        data = []

        for row in attendance[:10]:

            data.append({
                "Person ID": row["person_id"],
                "Name": row["name"],
                "Department": row["department"],
                "Date": row["date"],
                "Time": row["time"],
                "Status": row["status"],
                "Distance": row["distance"]
            })

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No attendance records yet."
        )

    st.markdown("---")

    # ------------------------------------------------------
    # TEST NOTIFICATION WIDGET
    # ------------------------------------------------------

    with st.expander("📲 Test Phone Notification (Send SMS / WhatsApp Alert)"):
        st.write("Test sending real or simulated attendance alerts to any mobile number:")

        from utils.notifier import send_direct_test_alert

        tcol1, tcol2 = st.columns(2)
        with tcol1:
            test_phone = st.text_input(
                "Phone Number",
                placeholder="+91XXXXXXXXXX or 10-digit number",
                key="test_phone_input"
            )
            test_name = st.text_input(
                "Recipient Name",
                value="Test User",
                key="test_name_input"
            )

        with tcol2:
            test_channel = st.selectbox(
                "Notification Channel",
                ["sms", "fast2sms", "whatsapp", "simulation"],
                index=0,
                key="test_channel_select",
                help="SMS uses Twilio or Fast2SMS. WhatsApp uses Twilio or CallMeBot. Simulation logs without external API."
            )

        if st.button("🚀 Send Test Notification Now", type="primary", use_container_width=True):
            if not test_phone.strip():
                st.error("Please enter a phone number to test.")
            else:
                with st.spinner("Sending notification..."):
                    success, detail, preview_msg = send_direct_test_alert(
                        phone_number=test_phone.strip(),
                        name=test_name.strip(),
                        channel=test_channel
                    )

                if success:
                    st.success(f"✅ Notification Processed! Status: **{detail}**")
                    st.text_area("Message Preview Sent:", value=preview_msg, height=120, disabled=True)
                else:
                    st.error(f"❌ Failed to send: {detail}")