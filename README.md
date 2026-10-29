# Face Recognition Attendance System

An AI-powered attendance management system that uses face recognition to identify registered people and record attendance automatically.

## 🚀 Live Demo

**[🔗 Open Face Recognition Attendance Application](https://piyushsingh0506-face-aatendance-main-v7kx8s.streamlit.app/)**

The application is deployed using Streamlit Community Cloud.

## 📌 Project Overview

The Face Recognition Attendance System automates the attendance process using computer vision and deep learning. Instead of manually marking attendance, the system detects a person's face, generates facial embeddings, compares them with registered users, and records attendance when a match is found.

The project is developed using Python, Streamlit, FaceNet, MTCNN, OpenCV, and SQLite.

## ✨ Features

- **Face Detection:** Detects faces from camera input.
- **Face Recognition:** Identifies registered people using facial embeddings.
- **Automatic Attendance:** Records attendance after successful recognition.
- **Person Registration:** Registers people with their details and face data.
- **Attendance Records:** Stores attendance information in a database.
- **Dashboard:** Provides an interface to access attendance features.
- **Database Management:** Uses SQLite to store records.
- **Email Notifications:** Email notifications can be integrated to inform users when attendance is marked, provided SMTP configuration and notification code are implemented.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| FaceNet | Facial feature extraction |
| MTCNN | Face detection |
| OpenCV | Image processing |
| PyTorch | Deep learning model support |
| NumPy | Numerical operations |
| SQLite | Database management |
| Git and GitHub | Version control and source code hosting |

## 📂 Project Structure

```text
Face-Recognition-Attendance-System/
│
├── models/
│   └── Face recognition model files
│
├── pages/
│   ├── dashboard.py
│   ├── register.py
│   ├── recognition.py
│   ├── records.py
│   └── manage_people.py
│
├── utils/
│   ├── face_detector.py
│   ├── embedding.py
│   └── similarity.py
│
├── .env.example
├── .gitignore
├── README.md
├── attendance.py
├── config.py
├── database.py
├── face_recognition.py
├── main.py
└── requirements.txt
```

*Note: Keep this structure aligned with the files actually present in your GitHub repository.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's HTTPS URL.

### 2. Open the project directory

```bash
cd Face-Recognition-Attendance-System
```

Use your actual cloned folder name if it differs.

### 3. Create a virtual environment

```powershell
python -m venv test
```

### 4. Activate the environment

```powershell
.\test\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python directly or use Command Prompt:

```cmd
test\Scripts\activate.bat
```

### 5. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Configure environment variables

If your project uses environment variables, copy `.env.example` to `.env` and fill in the required settings.

Never upload `.env` or real passwords, API keys, or authentication tokens to GitHub.

### 7. Run the application

Run this command from the project root:

```bash
streamlit run main.py
```

Streamlit will display a local URL in your terminal. Open that URL in your browser.

## 🧠 How It Works

1. A user registers with their details and face image.
2. The system detects the face using a face detection model.
3. FaceNet generates a numerical representation called a facial embedding.
4. The embedding is compared with stored embeddings.
5. If the similarity satisfies the configured recognition threshold, the system identifies the person.
6. Attendance is recorded in the database.
7. If email notifications are configured and implemented, the system can send an attendance confirmation.

## 🗄️ Database

SQLite is used to store application data. Depending on the implemented schema, the database may contain:

- Registered people and their details
- Facial embeddings
- Attendance dates and timestamps
- Other attendance-related records

## 📧 Email Notification Configuration

To enable email notifications, the project must include email-sending code and the required recipient email field in the database.

For Gmail SMTP, configure the credentials using environment variables such as:

```env
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
```

Use a Gmail App Password where required. Do not use or publish your normal Gmail password.

**Important:** These settings alone do not enable notifications; the registration, database, and attendance code must also implement email delivery.

## 🔒 Security

- Keep credentials and secret keys out of source control.
- Add `.env` to `.gitignore`.
- Protect personal information and attendance records.
- Use appropriate access controls before deploying for real-world use.

## 🚀 Deployment

The project is available through Streamlit Community Cloud:

**[Open Live Application](https://piyushsingh0506-face-aatendance-main-v7kx8s.streamlit.app/)**

For deployment configuration and dependency requirements, refer to the [Streamlit Community Cloud documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app).

## 🔮 Future Improvements

- Email notifications after successful attendance marking
- Attendance reports with CSV or Excel export
- Improved recognition under different lighting conditions
- Admin dashboard and user management
- Duplicate attendance prevention
- Secure authentication and role-based access
- Attendance analytics and visual reports

## 👨‍💻 Author

**Piyush Singh**

- GitHub: [piyushsingh0506](https://github.com/piyushsingh0506)
- LinkedIn: [Piyush Singh](https://linkedin.com/in/piyush-singh-4b5816328)

## 📄 License

This project is intended for educational and learning purposes. Add a LICENSE file if you want to publish it under a specific open-source license.
