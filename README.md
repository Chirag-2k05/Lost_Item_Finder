# 🔍 AI Lost Item Finder

A simple and efficient web application to **store, search, and manage lost items**, built using **Streamlit** with a user authentication system.

---

## 🌐 Live Demo

[![Open App](https://img.shields.io/badge/Streamlit-Live_App-red?style=for-the-badge&logo=streamlit)](https://lostitemfinder-jwrrq3rh5j7dj8222hrfem.streamlit.app/)

## 🚀 Features

* 🔐 User Authentication (Login & Signup)
* ➕ Add Lost Items
* 🔍 Search Items Easily
* 📋 View Your Items
* 💾 Lightweight Data Storage (CSV-based)
* ☁️ Deployable on Streamlit Cloud

---

## 🛠️ Tech Stack

* **Frontend & Backend:** Python, Streamlit
* **Data Handling:** Pandas
* **Storage:** CSV (can be upgraded to MongoDB/PostgreSQL)

---

## 📁 Project Structure

```
Lost_item/
│── app.py
│── users.csv
│── data.csv
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/lost-item-finder.git
cd lost-item-finder
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Run the Application

```
streamlit run app.py
```

---

## 📌 Usage

1. Create a new account (Signup)
2. Login with your credentials
3. Add lost items with details
4. Search items using keywords
5. View your saved items

---

## ⚠️ Important Notes

* Ensure `users.csv` and `data.csv` exist with headers:

### users.csv

```
username,password
```

### data.csv

```
user,item,location,description
```

---

## 🔒 Security Note

This project uses **basic authentication (plain text passwords)**.

👉 For production:

* Use password hashing (bcrypt)
* Use a database like MongoDB or PostgreSQL
* Implement JWT authentication

---

## 🌐 Deployment

You can deploy this app easily on:

* Streamlit Cloud
* Render
* Railway

---

## 💼 Resume Description

> Developed and deployed an AI-based Lost Item Finder using Streamlit with user authentication, data storage, and search functionality.

---

## 🚀 Future Improvements

* 🔐 Secure password hashing
* ☁️ Database integration (MongoDB/PostgreSQL)
* 📸 Image upload for items
* 🤖 AI-based item matching
* 👑 Admin dashboard

---

## 👨‍💻 Author

**Chirag Verma**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
