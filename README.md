# hotel_lister_app_django

A simple hotel listing web application built as part of the **Technometrics Junior Software Engineer Assessment**.  
The app allows users to search for hotels by city, filter by star rating or availability of features (like pool), bookmark hotels, and toggle between light and dark modes. It includes user authentication and is built with a Django backend and a React + Tailwind CSS frontend.

---

## ✨ Features

- 🔍 **Search Hotels** by location (city)
- ⭐ **Filter** by:
  - Star Rating (e.g., 3-star, 4-star, 5-star)
  - Features (e.g., Pool Available: Yes/No)
- 📋 **Display Hotel Results** with:
  - Hotel Name
  - Description
  - Star Rating
  - Indicative Price
  - "View Details" button
- 🔖 **Bookmarking Functionality**
  - Save hotels
  - View bookmarked list
- 👤 **User Authentication**
  - Register and login/logout
  - Session-based login with hashed passwords
- 🎨 **Light/Dark Mode Toggle**
  - Switch between Light and Dark appearance

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** React.js with Tailwind CSS
- **Database:** SQLite (Django ORM)
- **Static Data:** Demo data using JSON (Option A)
- **Authentication:** Django built-in auth system
- **Others:** Pillow (for image support)

---

## 🚀 How to Run the Project

### 🧱 Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/hotel_lister_app_django.git
   cd hotel_lister_app_django
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   If `requirements.txt` is not present, install manually:
   ```bash
   pip install django Pillow
   ```

4. **Run the server**
   ```bash
   python manage.py runserver
   ```

5. **Load demo hotel data**
   ```bash
   python manage.py load_hotels
   ```

---

## 🧪 Demo Data

We used **Option A** from the assessment: mock/static JSON hotel data stored within the backend.  
The data is loaded via the custom management command `load_hotels` and includes sample hotel details, prices, ratings, and features.

---

## 🎥Project Demo Video  
Check out the demo video of this project here:  
https://youtu.be/PQuqWA4OP2I


## 💡 AI Tool Usage

This project was supported using **ChatGPT (OpenAI)** to:
- Generate boilerplate code (views, models, templates)
- Debug and improve logic
- Structure the Django app efficiently
- Help write this README file

---

## 📂 Folder Structure

```
hotel_lister_app_django/
├── myenv/                      # Virtual environment
├── manage.py
├── hotel_lister_app/           # Main Django app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   ├── static/
│   └── management/             # For loading demo data
├── db.sqlite3
└── README.md
```

---

## 🧑‍💻 Author

**S.M. Abrar Mustakim Taki**  
Junior Software Engineer Candidate — Technometrics Assessment Submission

---

## 📎 License

This project is created solely for the purpose of the Technometrics assessment and is not intended for production use.
