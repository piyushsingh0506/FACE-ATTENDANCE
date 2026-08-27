import sqlite3
import os
import pickle
from datetime import datetime, date


# ==========================================================
# DATABASE PATH
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
)

DATABASE_PATH = os.path.join(
    DATA_DIR,
    "attendance.db"
)


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # ------------------------------------------------------
    # PEOPLE TABLE
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            person_id TEXT UNIQUE NOT NULL,

            name TEXT NOT NULL,

            department TEXT,

            phone_number TEXT,

            additional_info TEXT,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ------------------------------------------------------
    # FACE EMBEDDINGS TABLE
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS face_embeddings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            person_id TEXT NOT NULL,

            embedding BLOB NOT NULL,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (person_id)
                REFERENCES people(person_id)
                ON DELETE CASCADE
        )
    """)

    # ------------------------------------------------------
    # ATTENDANCE TABLE
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            person_id TEXT NOT NULL,

            date TEXT NOT NULL,

            time TEXT NOT NULL,

            status TEXT NOT NULL,

            distance REAL,

            FOREIGN KEY (person_id)
                REFERENCES people(person_id)
                ON DELETE CASCADE
        )
    """)

    # ------------------------------------------------------
    # NOTIFICATIONS TABLE
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            person_id TEXT,

            recipient_name TEXT,

            phone_number TEXT NOT NULL,

            channel TEXT NOT NULL,

            message TEXT NOT NULL,

            status TEXT NOT NULL,

            error_message TEXT,

            sent_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (person_id)
                REFERENCES people(person_id)
                ON DELETE SET NULL
        )
    """)

    connection.commit()

    connection.close()


# ==========================================================
# ADD PERSON
# ==========================================================

def add_person(
    person_id,
    name,
    department="",
    phone_number="",
    additional_info=""
):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO people
            (
                person_id,
                name,
                department,
                phone_number,
                additional_info
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            person_id,
            name,
            department,
            phone_number,
            additional_info
        ))

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()


# ==========================================================
# GET ONE PERSON
# ==========================================================

def get_person(person_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM people
        WHERE person_id = ?
    """, (
        person_id,
    ))

    person = cursor.fetchone()

    connection.close()

    return person


# ==========================================================
# GET ALL PEOPLE
# ==========================================================

def get_people(active_only=False):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM people
        ORDER BY created_at DESC
    """)

    people = cursor.fetchall()

    connection.close()

    return people


# ==========================================================
# ALIAS FOR COMPATIBILITY
# ==========================================================

def get_all_people():

    return get_people()


# ==========================================================
# UPDATE PERSON
# ==========================================================

def update_person(
    person_id,
    name,
    department="",
    phone_number="",
    additional_info=""
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE people

        SET
            name = ?,
            department = ?,
            phone_number = ?,
            additional_info = ?

        WHERE person_id = ?
    """, (
        name,
        department,
        phone_number,
        additional_info,
        person_id
    ))

    connection.commit()

    success = cursor.rowcount > 0

    connection.close()

    return success


# ==========================================================
# DELETE PERSON
# ==========================================================

def delete_person(person_id):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        # Delete embeddings
        cursor.execute("""
            DELETE FROM face_embeddings
            WHERE person_id = ?
        """, (
            person_id,
        ))

        # Delete attendance
        cursor.execute("""
            DELETE FROM attendance
            WHERE person_id = ?
        """, (
            person_id,
        ))

        # Delete person
        cursor.execute("""
            DELETE FROM people
            WHERE person_id = ?
        """, (
            person_id,
        ))

        deleted = cursor.rowcount > 0

        connection.commit()

        return deleted

    except Exception:

        connection.rollback()

        return False

    finally:

        connection.close()


# ==========================================================
# ADD FACE EMBEDDING
# ==========================================================

def add_embedding(
    person_id,
    embedding
):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        embedding_blob = pickle.dumps(
            np_to_list(embedding)
        )

        cursor.execute("""
            INSERT INTO face_embeddings
            (
                person_id,
                embedding
            )
            VALUES (?, ?)
        """, (
            person_id,
            embedding_blob
        ))

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        return False

    finally:

        connection.close()


# ==========================================================
# GET EMBEDDINGS FOR ONE PERSON
# ==========================================================

def get_embeddings(person_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT embedding
        FROM face_embeddings
        WHERE person_id = ?
    """, (
        person_id,
    ))

    rows = cursor.fetchall()

    connection.close()

    embeddings = []

    for row in rows:

        embedding = pickle.loads(
            row["embedding"]
        )

        embeddings.append(
            embedding
        )

    return embeddings


# ==========================================================
# GET ALL EMBEDDINGS
# ==========================================================

def get_all_embeddings():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            f.person_id,
            f.embedding,
            p.name,
            p.phone_number,
            p.department
        FROM face_embeddings f
        LEFT JOIN people p
        ON f.person_id = p.person_id
    """)

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:

        embedding = pickle.loads(
            row["embedding"]
        )

        results.append({
            "person_id": row["person_id"],
            "name": row["name"] or row["person_id"],
            "phone_number": row["phone_number"],
            "department": row["department"],
            "embedding": embedding
        })

    return results


# ==========================================================
# DELETE PERSON EMBEDDINGS
# ==========================================================

def delete_embeddings(person_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM face_embeddings
        WHERE person_id = ?
    """, (
        person_id,
    ))

    connection.commit()

    connection.close()


# ==========================================================
# ADD ATTENDANCE
# ==========================================================

def add_attendance(
    person_id,
    attendance_date=None,
    attendance_time=None,
    status="Present",
    distance=None
):

    if attendance_date is None:
        attendance_date = date.today().isoformat()

    if attendance_time is None:
        attendance_time = datetime.now().strftime("%H:%M:%S")

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO attendance
        (
            person_id,
            date,
            time,
            status,
            distance
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        person_id,
        attendance_date,
        attendance_time,
        status,
        distance
    ))

    connection.commit()

    attendance_id = cursor.lastrowid

    connection.close()

    return attendance_id


# ==========================================================
# GET ATTENDANCE
# ==========================================================

def get_attendance():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT

            a.id,

            a.person_id,

            p.name,

            p.department,

            p.phone_number,

            a.date,

            a.time,

            a.status,

            a.distance

        FROM attendance a

        LEFT JOIN people p
        ON a.person_id = p.person_id

        ORDER BY
            a.date DESC,
            a.time DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records


# ==========================================================
# GET ATTENDANCE BY DATE
# ==========================================================

def get_attendance_by_date(
    attendance_date
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT

            a.id,

            a.person_id,

            p.name,

            p.department,

            p.phone_number,

            a.date,

            a.time,

            a.status,

            a.distance

        FROM attendance a

        LEFT JOIN people p
        ON a.person_id = p.person_id

        WHERE a.date = ?

        ORDER BY a.time DESC
    """, (
        attendance_date,
    ))

    records = cursor.fetchall()

    connection.close()

    return records


# ==========================================================
# GET ATTENDANCE BY PERSON
# ==========================================================

def get_attendance_by_person(
    person_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT

            a.id,

            a.person_id,

            p.name,

            p.department,

            p.phone_number,

            a.date,

            a.time,

            a.status,

            a.distance

        FROM attendance a

        LEFT JOIN people p
        ON a.person_id = p.person_id

        WHERE a.person_id = ?

        ORDER BY
            a.date DESC,
            a.time DESC
    """, (
        person_id,
    ))

    records = cursor.fetchall()

    connection.close()

    return records


# ==========================================================
# CHECK IF ALREADY MARKED TODAY
# ==========================================================

def already_marked_today(
    person_id,
    attendance_date=None
):

    if attendance_date is None:

        attendance_date = date.today().isoformat()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id

        FROM attendance

        WHERE person_id = ?

        AND date = ?

        AND status = 'Present'

        LIMIT 1
    """, (
        person_id,
        attendance_date
    ))

    result = cursor.fetchone()

    connection.close()

    return result is not None


# ==========================================================
# GET TODAY'S ATTENDANCE COUNT
# ==========================================================

def get_today_attendance_count():

    today = date.today().isoformat()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total

        FROM attendance

        WHERE date = ?

        AND status = 'Present'
    """, (
        today,
    ))

    result = cursor.fetchone()

    connection.close()

    return result["total"]


# ==========================================================
# GET TOTAL REGISTERED PEOPLE
# ==========================================================

def get_total_people():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM people
    """)

    result = cursor.fetchone()

    connection.close()

    return result["total"]


# ==========================================================
# GET TODAY'S RECOGNIZED PEOPLE
# ==========================================================

def get_today_recognized_people():

    today = date.today().isoformat()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT person_id) AS total

        FROM attendance

        WHERE date = ?

        AND status = 'Present'
    """, (
        today,
    ))

    result = cursor.fetchone()

    connection.close()

    return result["total"]


# ==========================================================
# GET RECENT ATTENDANCE
# ==========================================================

def get_recent_attendance(
    limit=10
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT

            a.id,

            a.person_id,

            p.name,

            p.department,

            p.phone_number,

            a.date,

            a.time,

            a.status,

            a.distance

        FROM attendance a

        LEFT JOIN people p
        ON a.person_id = p.person_id

        ORDER BY
            a.id DESC

        LIMIT ?
    """, (
        limit,
    ))

    records = cursor.fetchall()

    connection.close()

    return records


# ==========================================================
# GET PHONE NUMBER
# ==========================================================

def get_phone_number(
    person_id
):

    person = get_person(
        person_id
    )

    if person is None:

        return None

    return person["phone_number"]


# ==========================================================
# HELPER FOR EMBEDDINGS
# ==========================================================

def np_to_list(
    embedding
):

    try:

        return embedding.tolist()

    except AttributeError:

        return embedding


# ==========================================================
# NOTIFICATIONS DATABASE METHODS
# ==========================================================

def add_notification(
    person_id,
    recipient_name,
    phone_number,
    channel,
    message,
    status,
    error_message=None
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO notifications
        (
            person_id,
            recipient_name,
            phone_number,
            channel,
            message,
            status,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        person_id,
        recipient_name,
        phone_number,
        channel,
        message,
        status,
        error_message
    ))

    connection.commit()

    notif_id = cursor.lastrowid

    connection.close()

    return notif_id


def get_notifications(
    limit=100
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            person_id,
            recipient_name,
            phone_number,
            channel,
            message,
            status,
            error_message,
            sent_at
        FROM notifications
        ORDER BY sent_at DESC, id DESC
        LIMIT ?
    """, (
        limit,
    ))

    records = cursor.fetchall()

    connection.close()

    return records