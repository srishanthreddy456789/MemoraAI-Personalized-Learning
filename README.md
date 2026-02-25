# MemoraAI – Personalized Learning Platform

MemoraAI is a **personalized learning system** that combines **Generative AI (GenAI)** with **Machine Learning (ML)** to help users learn, retain, and revise topics intelligently. The platform focuses on identifying what a user *forgets*, retraining models automatically using **MLOps**, and generating adaptive quizzes to improve long‑term retention.

This project was built as a **full‑stack AI system** with authentication, chat-based learning, ML-driven performance prediction, and automated training pipelines.

---
##  WorkFlow
##  Snapshot
**Frontend**
**Backendn**
## 🚀 Key Features


* 🔐 **User Authentication** – Secure user registration and login
* 💬 **GenAI Chat Interface** – Users learn topics through conversational AI
* 🧠 **Forget-Topic Detection** – ML model identifies weak or forgotten topics
* 📝 **Adaptive Quiz Generation** – Quizzes generated automatically based on learning gaps
* 🔁 **Feedback Loop** – Quiz results improve future predictions
* ⚙️ **Automated ML Training (MLOps)** – Models retrain on new learning data
* 📊 **Session Tracking** – Tracks messages, sessions, and interaction patterns

---

## 🧠 How MemoraAI Works (Workflow)

1. **User Registration & Login**

   * User creates an account and logs in

2. **Learning via Chat (GenAI)**

   * User studies topics through a conversational GenAI interface
   * Explanations adapt based on user responses

3. **Data Collection**

   * Messages
   * Sessions
   * Interaction patterns
   * Quiz responses

4. **ML Behavior Analysis**

   * ML model analyzes user learning behavior
   * Identifies weak / forgotten topics

5. **Quiz Generation**

   * GenAI generates quizzes based on forgotten concepts

6. **Performance Prediction**

   * ML predicts understanding and retention

7. **Feedback Loop**

   * Quiz results are stored
   * Models retrain automatically using MLOps pipelines

---

## 🧩 Tech Stack

### Frontend

* React
* Modern UI with chat-based interaction

### Backend

* FastAPI
* REST APIs (Swagger/OpenAPI enabled)

### AI & ML

* Generative AI for explanations and quiz generation
* Custom ML model for:

  * Forget-topic prediction
  * Performance estimation
* Automated training using MLOps pipelines

### Database

* **SQLite**

  * Stores users, sessions, messages, quizzes, and ML training data

### DevOps / MLOps

* Docker (local usage)
* DVC for data versioning
* Automated ML pipelines
* MLFlow
* CICD

---

## 📂 Project Structure

```
MemoraAI-Personalized-Learning/
│
├── api/            # API layer
├── backend/        # FastAPI backend
├── frontend/       # React frontend
├── models/         # ML models
├── pipelines/      # MLOps training pipelines
├── data/           # Training and interaction data
├── mlruns/         # ML experiment tracking
├── prompts/        # GenAI prompts
├── docker/         # Docker configuration
├── scripts/        # Utility scripts
└── config/         # Configuration files
```

---

## 🧪 API Features (Swagger)

* `/register` – User registration
* `/login` – User login
* `/chat` – Chat with GenAI
* `/quiz` – Generate quiz
* `/quiz/submit` – Submit quiz answers
* `/sessions` – List learning sessions
* `/predict` – ML performance prediction
* `/health` – Health check

---

## 🚧 Deployment Status & Limitations

### ❗ Important Note on Deployment

MemoraAI **could not be fully deployed to a free hosting platform** due to **technical and cost limitations**.

### Reasons:

* 🧠 **Heavy GenAI + ML Models**

  * Large model size
  * High memory (RAM) usage

* 💾 **Persistent Storage Requirement**

  * User chat data
  * Quiz results
  * ML training datasets

* 🗄️ **SQLite Database Limitation**

  * Requires persistent disk storage
  * Most free deployment platforms **do not allow writable persistent storage**

* 🔁 **Continuous ML Training (MLOps)**

  * Automated retraining pipelines
  * Background jobs not supported on free tiers

* 🚫 **No Free Platform Supports**:

  * Long-running ML processes
  * Persistent databases
  * Heavy AI workloads together

### Result

Due to these constraints:

* ❌ No deployment platform stores user data for free
* ❌ ML training cannot run reliably on free hosting
* ❌ SQLite data resets on redeployments

👉 Therefore, **MemoraAI is currently designed to run locally or on paid cloud infrastructure**.

---

## ▶️ Running Locally

```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

Access Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🎯 Future Improvements

* Deploy using paid cloud services (AWS / GCP / Azure)
* Replace SQLite with PostgreSQL
* Add vector database for long-term memory
* Improve quiz difficulty adaptation
* Add user analytics dashboard

---

## 👨‍💻 Author

**Srishanth Reddy**
AI / ML Engineer | Full‑Stack Developer

---

## 📜 License

This project is for **educational and research purposes**.

---

✨ *MemoraAI focuses on learning what you forget — and helping you remember it better.*


