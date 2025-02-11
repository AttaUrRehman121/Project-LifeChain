# LifeChain: Empowering Organ Donation with Machine Learning & Blockchain

## 📌 Project Overview
LifeChain is an innovative system that enhances **organ donation and transplantation** by integrating **Machine Learning (ML) and Blockchain** technologies. The goal is to create a **secure, transparent, and efficient** platform for matching donors and recipients, reducing mismatches, delays, and fraudulent activities.

## 🚀 Key Features
- **AI-Powered Donor-Recipient Matching:** Uses **ML algorithms** (Random Forest, Decision Tree, KNN) to find the most compatible matches.
- **Blockchain Smart Contracts:** Ensures **security, transparency, and immutability** of agreements.
- **User Roles:** Supports **donors, recipients, and admins** with separate dashboards.
- **Automated Compatibility Tests:** Provides instant predictions for organ compatibility.
- **Data Privacy & Security:** Blockchain-backed storage ensures **tamper-proof** records.
- **Interactive Reports & Analytics:** Displays insights on donor-recipient trends.

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, JavaScript (Bootstrap)
- **Backend:** Python (Django)
- **Machine Learning:** Scikit-Learn (Random Forest, Decision Tree, KNN)
- **Blockchain:** Smart Contracts for organ allocation
- **Database:** MySQL

## 📥 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/lifechain.git
cd lifechain
```
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the Application
```bash
python manage.py runserver  # Django
```
### 4️⃣ Access the Web App
Open your browser and go to:
```
http://127.0.0.1:8000  # Django
```

## 📊 Machine Learning Model Workflow
1. **Data Preprocessing:** Handles missing values, encodes categorical data.
2. **Model Training:** Trains ML models on donor-recipient datasets.
3. **Prediction & Evaluation:** Uses `accuracy_score`, `f1_score`, `confusion_matrix`.
4. **Blockchain Integration:** Stores verified matches on a secure ledger.

## 🔬 Evaluation Metrics
- **Accuracy Score**: Measures prediction correctness.
- **Confusion Matrix**: Analyzes classification errors.
- **F1 Score**: Ensures balanced precision and recall.

## 📜 API Endpoints (Example)
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/register` | User registration |
| `POST` | `/login` | User authentication |
| `GET` | `/donors` | Retrieve donor list |
| `GET` | `/recipients` | Retrieve recipient list |
| `POST` | `/match` | Run ML model to find matches |

## 🤝 Contributors
- **[Your Name]** – Machine Learning & Backend
- **[Teammate 1]** – Frontend & UI/UX
- **[Teammate 2]** – Blockchain & Security

## 📌 Future Enhancements
- **Real-time Donor-Recipient Tracking** using IoT.
- **Deep Learning-based Compatibility Predictions**.
- **Mobile App for Better Accessibility**.

## 📜 License
This project is licensed under the **MIT License**.

---

**🔗 Stay Connected:** [LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)

