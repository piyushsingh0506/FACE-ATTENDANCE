import sys
import streamlit as st

# Auto-start with Streamlit if executed directly via standard python
if __name__ == "__main__":
    try:
        from streamlit.runtime import exists as _runtime_exists
        _in_runtime = _runtime_exists()
    except Exception:
        _in_runtime = hasattr(st, "_is_running_with_streamlit") and st._is_running_with_streamlit

    if not _in_runtime:
        try:
            from streamlit.web import cli as stcli
        except ImportError:
            from streamlit import cli as stcli
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())

from config import (
    APP_TITLE,
    APP_ICON,
    RECOGNITION_THRESHOLD,
    ATTENDANCE_COOLDOWN,
    ENABLE_NOTIFICATIONS,
    NOTIFICATION_CHANNEL
)

from database import (
    initialize_database
)

from pages.dashboard import (
    show_dashboard
)

from pages.register import (
    show_register
)

from pages.recognition import (
    show_recognition
)

from pages.records import (
    show_records
)

from pages.manage_people import (
    show_manage_people
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# DATABASE
# ==========================================================

initialize_database()


# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.main-title {
    font-size: 32px;
    font-weight: 700;
}

.subtitle {
    color: #777;
    font-size: 16px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("👁️ Face Attendance")

    st.markdown("---")

    selected_page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👤 Register Person",
            "📷 Mark Attendance",
            "📋 Attendance Records",
            "👥 Manage People"
        ]
    )

    st.markdown("---")

    st.subheader("⚙️ Settings")

    st.write(
        f"Recognition threshold: "
        f"`{RECOGNITION_THRESHOLD}`"
    )

    st.write(
        f"Attendance cooldown: "
        f"`{ATTENDANCE_COOLDOWN}s`"
    )

    st.write(
        f"📱 SMS Alerts: "
        f"`{'🟢 Enabled' if ENABLE_NOTIFICATIONS else '🔴 Disabled'}`"
    )

    if ENABLE_NOTIFICATIONS:
        st.caption(f"Channel: `{NOTIFICATION_CHANNEL.upper()}`")

    st.markdown("---")

    st.caption(
        "FaceNet Attendance System"
    )


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">'
    '👁️ Face Recognition Attendance System'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Automatic attendance using FaceNet'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# ROUTING
# ==========================================================

if selected_page == "🏠 Dashboard":

    show_dashboard()


elif selected_page == "👤 Register Person":

    show_register()


elif selected_page == "📷 Mark Attendance":

    show_recognition()


elif selected_page == "📋 Attendance Records":

    show_records()


elif selected_page == "👥 Manage People":

    show_manage_people()