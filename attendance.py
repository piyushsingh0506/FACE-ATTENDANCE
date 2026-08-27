import time
from datetime import datetime, date

from database import (
    add_attendance,
    already_marked_today,
    get_person
)

from config import (
    ATTENDANCE_COOLDOWN,
    ENABLE_NOTIFICATIONS
)

from utils.notifier import (
    send_attendance_notification
)


# ==========================================================
# SESSION MEMORY
# ==========================================================

_last_attendance = {}


# ==========================================================
# MARK ATTENDANCE
# ==========================================================

def mark_attendance(
    person_id,
    distance
):

    current_time = time.time()
    person = get_person(person_id)

    # ------------------------------------------------------
    # CHECK COOLDOWN
    # ------------------------------------------------------

    if person_id in _last_attendance:

        elapsed = (
            current_time
            - _last_attendance[person_id]
        )

        if elapsed < ATTENDANCE_COOLDOWN:

            return False, "Cooldown active", person, None

    # ------------------------------------------------------
    # CHECK TODAY
    # ------------------------------------------------------

    if already_marked_today(
        person_id
    ):

        _last_attendance[
            person_id
        ] = current_time

        return False, "Already marked today", person, None

    # ------------------------------------------------------
    # DATABASE
    # ------------------------------------------------------

    today_date = date.today().isoformat()
    now_time = datetime.now().strftime("%H:%M:%S")

    add_attendance(
        person_id=person_id,
        attendance_date=today_date,
        attendance_time=now_time,
        status="Present",
        distance=distance
    )

    _last_attendance[
        person_id
    ] = current_time

    # ------------------------------------------------------
    # SEND NOTIFICATION
    # ------------------------------------------------------

    notif_status = None

    if ENABLE_NOTIFICATIONS and person:

        name = person["name"]
        phone_number = person["phone_number"]

        if phone_number:

            success, notif_status = send_attendance_notification(
                person_id=person_id,
                name=name,
                phone_number=phone_number,
                time_str=datetime.now().strftime("%I:%M:%S %p"),
                date_str=today_date,
                async_send=True
            )

        else:

            notif_status = "No phone number registered"

    return True, "Attendance marked successfully", person, notif_status