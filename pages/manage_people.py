import streamlit as st

from database import (
    get_people,
    get_person,
    update_person,
    delete_person
)


# ==========================================================
# MANAGE PEOPLE
# ==========================================================

def show_manage_people():

    st.header(
        "👥 Manage People"
    )

    people = get_people()

    if not people:

        st.info(
            "No registered people."
        )

        return

    # ------------------------------------------------------
    # PEOPLE TABLE
    # ------------------------------------------------------

    st.subheader(
        f"Registered People ({len(people)})"
    )

    for person in people:

        with st.expander(
            f"👤 {person['name']} "
            f"({person['person_id']}) - 📱 {person['phone_number'] or 'No Phone'}"
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Person ID:** "
                    f"`{person['person_id']}`"
                )

                st.write(
                    f"**Name:** "
                    f"{person['name']}"
                )

                st.write(
                    f"**Phone Number:** "
                    f"`{person['phone_number'] or 'N/A'}`"
                )

            with col2:

                st.write(
                    f"**Department:** "
                    f"{person['department'] or 'N/A'}"
                )

                st.write(
                    f"**Created At:** "
                    f"{person['created_at']}"
                )

                st.write(
                    f"**Additional Info:** "
                    f"{person['additional_info'] or 'None'}"
                )

            st.markdown("---")

            # ------------------------------------------------
            # UPDATE
            # ------------------------------------------------

            st.subheader(
                "✏️ Update Information"
            )

            u_col1, u_col2 = st.columns(2)

            with u_col1:
                new_name = st.text_input(
                    "Full Name",
                    value=person["name"],
                    key=f"name_{person['person_id']}"
                )

                new_phone = st.text_input(
                    "📱 Phone Number (For Notifications)",
                    value=person["phone_number"] or "",
                    key=f"phone_{person['person_id']}",
                    placeholder="+91XXXXXXXXXX"
                )

            with u_col2:
                new_department = st.text_input(
                    "Department",
                    value=person["department"] or "",
                    key=f"dept_{person['person_id']}"
                )

                new_info = st.text_area(
                    "Additional Information",
                    value=person["additional_info"] or "",
                    key=f"info_{person['person_id']}"
                )

            b_col1, b_col2 = st.columns(2)

            with b_col1:

                if st.button(
                    "💾 Update Person",
                    key=f"update_{person['person_id']}",
                    type="primary",
                    use_container_width=True
                ):

                    update_person(
                        person_id=person["person_id"],
                        name=new_name.strip(),
                        department=new_department.strip(),
                        phone_number=new_phone.strip(),
                        additional_info=new_info.strip()
                    )

                    st.success(
                        "✅ Person details updated successfully."
                    )

                    st.rerun()

            with b_col2:

                if st.button(
                    "🗑️ Delete Person",
                    key=f"delete_{person['person_id']}",
                    use_container_width=True
                ):

                    delete_person(
                        person["person_id"]
                    )

                    st.success(
                        "🗑️ Person and embeddings removed."
                    )

                    st.rerun()