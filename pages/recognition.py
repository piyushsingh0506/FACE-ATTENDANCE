import streamlit as st
import numpy as np

from PIL import Image

from face_recognition import (
    recognize_face
)

from attendance import (
    mark_attendance
)

from utils.face_detector import (
    get_detector
)


# ==========================================================
# RECOGNITION PAGE
# ==========================================================

def show_recognition():

    st.header("📷 Mark Attendance")

    st.write(
        "Capture a face image to recognize "
        "the registered person."
    )

    # ------------------------------------------------------
    # CAMERA
    # ------------------------------------------------------

    image = st.camera_input(
        "Take a photo"
    )

    if image is None:

        st.info(
            "📷 Use the camera above to capture a face."
        )

        return

    # ------------------------------------------------------
    # LOAD IMAGE
    # ------------------------------------------------------

    pil_image = Image.open(
        image
    ).convert("RGB")

    # ------------------------------------------------------
    # DETECT
    # ------------------------------------------------------

    detector = get_detector()

    boxes, probabilities = detector.detect(
        pil_image
    )

    if boxes is None:

        st.error(
            "❌ No face detected."
        )

        return

    if len(boxes) > 1:

        st.warning(
            "⚠️ Multiple faces detected. "
            "Please capture one person at a time."
        )

        return

    # ------------------------------------------------------
    # EXTRACT FACE
    # ------------------------------------------------------

    face = detector(
        pil_image
    )

    if face is None:

        st.error(
            "Unable to extract face."
        )

        return

    # ------------------------------------------------------
    # RECOGNIZE
    # ------------------------------------------------------

    result = recognize_face(
        face
    )

    # ------------------------------------------------------
    # RESULT
    # ------------------------------------------------------

    if result["recognized"]:

        st.success(
            "✅ Recognized"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Name",
                result["name"]
            )

        with col2:

            st.metric(
                "Person ID",
                result["person_id"]
            )

        with col3:

            st.metric(
                "Distance",
                f"{result['distance']:.4f}"
            )

        # --------------------------------------------------
        # ATTENDANCE
        # --------------------------------------------------

        marked, message, person, notif_status = mark_attendance(
            result["person_id"],
            result["distance"]
        )

        if marked:

            st.success(
                "🎉 Attendance marked successfully!"
            )

            # Notification Feedback
            if person and person["phone_number"]:
                st.info(
                    f"📱 **Notification Dispatched:** "
                    f"Alert sent to `{person['phone_number']}` "
                    f"({notif_status or 'Sent'})"
                )
            else:
                st.warning(
                    "⚠️ No phone number registered for this person. "
                    "Update phone number in '👥 Manage People' to receive SMS/WhatsApp alerts."
                )

        else:

            st.info(
                f"ℹ️ {message}"
            )

    else:

        st.error(
            "❌ Unknown Person"
        )

        if result["distance"] is not None:

            st.write(
                f"Best distance: "
                f"`{result['distance']:.4f}`"
            )