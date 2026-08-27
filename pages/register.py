import streamlit as st
import numpy as np
from PIL import Image

from database import (
    add_person,
    add_embedding,
    get_person
)

from utils.face_detector import (
    get_detector
)

from utils.embedding import (
    generate_embedding
)

from config import (
    MIN_REGISTRATION_IMAGES,
    MAX_REGISTRATION_IMAGES
)


# ==========================================================
# REGISTER PERSON
# ==========================================================

def show_register():

    st.header("👤 Register Person")

    st.write(
        f"Capture {MIN_REGISTRATION_IMAGES}–"
        f"{MAX_REGISTRATION_IMAGES} face images."
    )

    # ------------------------------------------------------
    # PERSON INFORMATION
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        person_id = st.text_input(
            "Person ID",
            placeholder="EMP001 / STU001"
        )

        name = st.text_input(
            "Full Name"
        )

        phone_number = st.text_input(
            "📱 Phone Number",
            placeholder="+91XXXXXXXXXX"
        )

    with col2:

        department = st.text_input(
            "Department / Class / Team"
        )

        additional_info = st.text_area(
            "Additional Information"
        )

    # ------------------------------------------------------
    # CAMERA
    # ------------------------------------------------------

    st.subheader(
        "📷 Capture Face"
    )

    image = st.camera_input(
        "Take a face photograph"
    )

    # ------------------------------------------------------
    # SESSION STORAGE
    # ------------------------------------------------------

    if "registration_embeddings" not in st.session_state:

        st.session_state[
            "registration_embeddings"
        ] = []

    embeddings = st.session_state[
        "registration_embeddings"
    ]

    # ------------------------------------------------------
    # PROCESS IMAGE
    # ------------------------------------------------------

    if image is not None:

        pil_image = Image.open(
            image
        ).convert("RGB")

        detector = get_detector()

        # --------------------------------------------------
        # DETECT FACE
        # --------------------------------------------------

        boxes, probabilities = detector.detect(
            pil_image
        )

        if boxes is None:

            st.error(
                "❌ No face detected."
            )

        elif len(boxes) > 1:

            st.warning(
                "⚠️ Multiple faces detected. "
                "Please capture only one person."
            )

        else:

            face_tensor = detector(
                pil_image
            )

            if face_tensor is None:

                st.error(
                    "Unable to extract face."
                )

            else:

                embedding = generate_embedding(
                    face_tensor
                )

                embeddings.append(
                    embedding
                )

                st.session_state[
                    "registration_embeddings"
                ] = embeddings

                st.success(
                    f"Face captured successfully. "
                    f"Images: {len(embeddings)}"
                )

    # ------------------------------------------------------
    # PROGRESS
    # ------------------------------------------------------

    progress = min(
        len(embeddings)
        / MAX_REGISTRATION_IMAGES,
        1.0
    )

    st.progress(
        progress
    )

    st.write(
        f"Captured embeddings: "
        f"**{len(embeddings)} / "
        f"{MAX_REGISTRATION_IMAGES}**"
    )

    # ------------------------------------------------------
    # SAVE
    # ------------------------------------------------------

    if st.button(
        "💾 Register Person",
        type="primary",
        use_container_width=True
    ):

        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        if not person_id.strip():

            st.error(
                "Please enter Person ID."
            )

            return

        if not name.strip():

            st.error(
                "Please enter name."
            )

            return

        if not phone_number.strip():

            st.error(
                "Please enter phone number."
            )

            return

        if len(embeddings) < MIN_REGISTRATION_IMAGES:

            st.error(
                f"Please capture at least "
                f"{MIN_REGISTRATION_IMAGES} images."
            )

            return

        if get_person(
            person_id.strip()
        ):

            st.error(
                "Person ID already exists."
            )

            return

        # --------------------------------------------------
        # ADD PERSON
        # --------------------------------------------------

        success = add_person(
            person_id=person_id.strip(),
            name=name.strip(),
            department=department.strip(),
            phone_number=phone_number.strip(),
            additional_info=additional_info.strip()
        )

        if not success:

            st.error(
                "Unable to register person."
            )

            return

        # --------------------------------------------------
        # SAVE EMBEDDINGS
        # --------------------------------------------------

        for embedding in embeddings:

            add_embedding(
                person_id.strip(),
                embedding
            )

        # --------------------------------------------------
        # CLEAR SESSION
        # --------------------------------------------------

        st.session_state[
            "registration_embeddings"
        ] = []

        st.success(
            f"✅ {name} registered successfully!"
        )

        st.info(
            f"📱 Phone number {phone_number} "
            f"saved successfully."
        )

        st.balloons()