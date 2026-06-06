# Nova-Class 🎓

An AI-powered smart attendance platform. Teachers log in with a username & password, students authenticate via **face recognition**. Teacher creates subjects, shares a class code — and when it's time for attendance, just upload a class photo. The system detects faces, matches them against enrolled students, and marks attendance automatically.

🌐 **Live Demo:** [novaclass-main.streamlit.app](https://novaclass-main.streamlit.app/)

---

## ✨ Features

- 👨‍🏫 **Teacher Dashboard** — Create subjects, share class codes, manage students
- 🧑‍🎓 **Student Face Login** — Students register and authenticate using face recognition
- 📸 **One-Click Attendance** — Upload a class photo → AI marks attendance automatically
- 📊 **Attendance History** — Students can view their own attendance per subject

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Frontend/UI | Streamlit (multi-screen) |
| Face Detection & Embedding | dlib + face_recognition_models (128-dim descriptor) |
| Face Classification | sklearn SVC (linear kernel) |
| Database | Supabase (PostgreSQL) |
| Auth | bcrypt (teacher password hashing) |
| Caching | `@st.cache_resource` |

---

## 🧠 How the AI Pipeline Works

1. Teacher uploads a class photo
2. `dlib` detects all faces and generates **128-dimensional embeddings** for each
3. A trained **SVC classifier** predicts the identity of each detected face
4. A **Euclidean distance threshold (0.6)** acts as a confidence check — faces with distance > 0.6 are rejected
5. Matched students get their attendance logged in Supabase

---

## 📁 File Structure

| File | Role |
|---|---|
| `face_pipeline.py` | Core AI: detect → embed → classify |
| `db.py` | All Supabase CRUD operations |
| `config.py` | Supabase client setup |
| `home_screen.py` | Landing / login screen |
| `teacher_screen.py` | Teacher dashboard |
| `student_screen.py` | Student attendance history |
| `dialog_*.py` | Popups: enroll, create subject, share, results |
| `subject_card.py` | Subject card UI component |
| `base_layout.py`, `header.py`, `footer.py` | Layout components |

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/Vinayagasundaram/Nova-Class.git
cd Nova-Class

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

> ⚠️ You'll need a Supabase project set up with the required tables: `teachers`, `students`, `subjects`, `subject_students`, `attendance_logs`
