# 🎓 AcaNexus : Studivo

> A modern student productivity platform that helps students manage academics, assignments, notes, and expenses through a unified dashboard.
> **A unified, full-stack student productivity ecosystem designed for modern academia.**

![Status](https://img.shields.io/badge/Status-Active%20Development-gold)
[![Version](https://img.shields.io/badge/Version-v1.0-blue?style=flat-square)](#)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![SQLite](https://img.shields.io/badge/SQLite-Database-green)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 📖 Overview

**AcaNexus : Studivo** is a full-stack student productivity and management platform built using Flask, SQLite, HTML, CSS, and JavaScript.

The modern student juggles multiple platforms for managing assignments, tracking deadlines, organizing study sessions, and keeping personal notes. This fragmentation creates unnecessary friction and cognitive load.

**AcaNexus : Studivo** is a centralized academic workspace built to solve this problem. Developed with Python and Flask, it brings essential student tools into a single, cohesive dashboard. Wrapped in a premium "Dark Academic" aesthetic with modern gold accents, AcaNexus is designed to be more than just a task manager—it is a comprehensive ecosystem aimed at optimizing student productivity and academic success.

Instead of relying on multiple applications, students can access everything through a single modern dashboard.

This project is being developed as both a practical productivity solution and a portfolio project showcasing full-stack development skills.

---

## ✨ Current Features

## ✨ Key Features

### 🔐 Authentication & Security

- **Secure Access:** Robust user registration, secure login, and session management.
- **Data Privacy:** Strict user-specific data isolation ensuring your academic data remains private.
- **Account Management:** Seamless password changes and secure logout functionality.

### 📊 Smart Dashboard

- **Personalized Experience:** Dynamic greetings based on time of day and user profile.
- **Academic Overview:** Quick-glance statistics cards for active assignments and tasks.
- **Widgets:** Built-in "Upcoming Deadlines" widget to keep you ahead of your schedule.
- **Responsive Layout:** A fluid, mobile-friendly design that adapts to any screen size.

### 📝 Assignment Management

- **Full Control:** Secure CRUD (Create, Read, Update, Delete) operations for all tasks.
- **Tracking:** Toggle between Pending and Completed statuses with intuitive visual indicators.
- **Filtering & Search:** Easily search through past assignments and filter by current status.
- **Deadline Management:** Date-aware tracking that automatically highlights pressing due dates.

### 📅 Calendar & Study Planner

- **Interactive Navigation:** Monthly calendar view with current-day highlighting.
- **Event Management:** Add, edit, and delete academic events or study sessions.
- **Seamless Integration:** Only pending assignments are dynamically displayed on your calendar.
- **Planner Widget:** A quick-look upcoming events widget with dynamic statistics and visual legends.

### 👤 Profile & Settings

- **Identity:** Manage your personal and academic information from a dedicated profile page.
- **Customization:** Theme settings foundation laying the groundwork for personalized aesthetics.
- **Security Hub:** Dedicated account settings and security management section.

### 📝 Notes Manager

- Create notes
- Edit notes
- Delete notes
- Search notes instantly
- Organized note cards
- Clean modern interface

### 💰 Expense Manager

- Add expenses
- Categorize spending
- Track total expenses
- Expense summaries
- Organized expense cards

### 🎨 Modern UI System

- Dark Academic × Modern Tech theme
- Gold accent design language
- Responsive layouts
- Hover animations
- Consistent design system
- Reusable components
- Premium dashboard styling

---

## 🖼️ Screenshots

### 🏠 Homepage

![Homepage](screenshots/Homepage.png)

### 📊 Dashboard

![Dashboard](screenshots/Dashboard.png)

### 📝 Notes

![Notes](screenshots/Notes.png)

### 📅 Assignments

![Assignments](screenshots/Assignments.png)

### 💰 Expenses

![Expenses](screenshots/Expenses.png)

---

## 🎯 Problem Statement

Students frequently switch between multiple applications for:

- Notes management
- Assignment tracking
- Expense management
- Productivity planning
- Academic organization

This creates unnecessary complexity and inefficiency.

**AcaNexus : Studivo** aims to solve this problem by bringing essential student tools into one integrated platform.

---

## 🚀 MVP Features

The MVP (Minimum Viable Product) includes:

- Dashboard
- Notes Manager
- Assignment Tracker
- Expense Manager

---

## 🔮 Planned Features

### 📚 Academic Hub

- Study Planner
- Exam Countdown
- Semester Tracker
- Academic Analytics
- Attendance Tracker

### 🏠 Hostel Hub

- Expense Splitter
- Roommate Expense Management
- Hostel Notice Board
- Laundry Reminders
- Mess Menu Management

### 👤 Student Profile

- Personalized Dashboard
- Activity Statistics
- Productivity Metrics
- Achievement Tracking

### 🔐 Authentication System

- User Registration
- User Login
- Password Security
- Session Management
- Profile Management

### ☁️ Future Enhancements

- PostgreSQL Migration
- Cloud Deployment
- REST API
- Mobile Responsive Improvements
- AI Study Assistant
- Smart Recommendations

---

## 🛠️ Tech Stack

| Category            | Technologies                                   |
| :------------------ | :--------------------------------------------- |
| **Frontend**        | HTML5, CSS3, JavaScript, Jinja2 Templating     |
| **Backend**         | Python 3, Flask Framework                      |
| **Database**        | SQLite (Relational Database)                   |
| **Design System**   | Custom CSS (Dark Academic × Modern Tech theme) |
| **Version Control** | Git, GitHub ,VS Code (Tools)                   |

---

## 🚀 Installation Guide

Want to run AcaNexus locally? Follow these steps to set up your development environment.

**1. Clone the repository**

```bash
git clone [https://github.com/Celestial-tech100/AcaNexus-Studivo.git](https://github.com/Celestial-tech100/AcaNexus-Studivo.git)
cd AcaNexus-Studivo

```

**2. Create a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

```

**3. Install dependencies**

```bash
pip install -r requirements.txt

```

**4. Initialize the Database and Run the Application**

```bash
python reset_db.py  # Optional: Only if you need a fresh database schema
python app.py

```

_The application will be available at `http://127.0.0.1:5000`._

---

## 📂 Project Structure

```text
AcaNexus-Studivo/
│
├── .vscode/
│   └── settings.json
├── database/
│   ├── acanexus.db
│   └── schema.sql
├── docs/
│   └── project-architecture.md
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── auth.css
│   │   ├── notes.css
│   │   ├── landing.css
│   │   ├── expenses.css
│   │   ├── attendance.css
│   │   ├── animations.css
│   │   ├── base.css
│   │   ├── components.css
│   │   ├── dashboard.css
│   │   ├── layout.css
│   │   ├── pages.css
│   │   └── style.css
│   │   ├── assignments.css
│   │   ├── settings.css
│   │
│   ├── js/
│   │   └── script.js
|       └── assignments.js
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── attendance.html
│   ├── assignments.html
│   ├── calendar.html
│   ├── notes.html
│   ├── expenses.html
│   ├── edit_note.html
│   ├── edit_event.html
│   ├── profile.html
│   └── settings.html
│
└── screenshots/
|   ├── Homepage.png
|   ├── Dashboard.png
|   ├── Notes.png
|   ├── Assignment.png
|   └── Expenses.png
├── .gitignore
├── app.py
├── LICENSE
├── README.md
├── requirements.txt
└── reset_db.py

```

## 🛡️ Security Highlights

AcaNexus is built with foundational security principles in mind:

- **Session Authentication:** Secure server-side sessions manage user states safely.
- **Data Isolation:** All database queries are strictly scoped to the logged-in user's ID, ensuring total data privacy.
- **Secure Routing:** Protected endpoints prevent unauthorized access to internal dashboards and API routes via custom decorators.
- **Password Security:** (Implementation of secure password hashing for user accounts).

---

## 🎯 Learning Objectives

This project is helping strengthen skills in:

- Full-Stack Development
- Python Programming
- Flask Framework
- Database Design
- SQL Queries
- Frontend Development
- Git & GitHub
- Software Engineering Practices
- UI/UX Design
- Cloud Computing Fundamentals

---

## 🎯 Feature Status & Roadmap

### Current Implementation Status

| Module                    | Status      |
| ------------------------- | ----------- |
| **Authentication System** | ✅ Complete |
| **Smart Dashboard**       | ✅ Complete |
| **Assignment Tracking**   | ✅ Complete |
| **Calendar & Planner**    | ✅ Complete |
| **User Profile**          | ✅ Complete |
| **Application Settings**  | ✅ Complete |
| Notes & Document Manager  | 🚧 Planned  |
| Academic Study Planner    | 🚧 Planned  |
| Digital Library           | 🚧 Planned  |

## 📈 Development Roadmap

**Phase 1: Academic Hub (Next Steps)**

- Study Sessions & Pomodoro Timer integration.
- Rich-text Notes management and Attendance Tracker.
- Semester Tracker and automated GPA Calculator.

**Phase 2: Digital Ecosystem**

- Digital Library with eBook reading capabilities.
- Subscription and Author Permission systems.
- Productivity analytics, Daily Goals, and Habit tracking.

**Phase 3: AI & Community**

- AI Study Assistant and automated Note Summaries.
- Student Groups, Discussion Forums, and Shared Notes.

**Phase 4: Technical Scaling**

- Migration to PostgreSQL and Cloud Deployment.
- Docker containerization and CI/CD pipelines.
- Building out a dedicated REST API for future mobile integration.

---

## 💡 Learning Outcomes

Developing this platform provided hands-on experience in several core software engineering disciplines:

- Architecting scalable **Full-Stack Applications** using Python and Flask.
- Designing normalized **Relational Databases** and writing efficient SQL queries.
- Implementing **State and Session Management** for secure user authentication.
- Crafting a cohesive **UI/UX Design System** using reusable components and modern CSS techniques.
- Applying robust **Software Engineering Practices** including modular code structuring and version control.

---

## 🔭 Future Vision

The ultimate goal for **AcaNexus : Studivo** is to transcend the standard "To-Do List" architecture. The vision is to build an intelligent, predictive student ecosystem. By eventually integrating AI planners and community-driven knowledge sharing, AcaNexus aims to become the definitive operating system for a student's academic life.

---

## 🤝 Support & Contributions

This project is currently being developed as a personal learning and portfolio project.

Suggestions, feedback, and ideas are always welcome.
If you find this project interesting or helpful:

- ⭐ **Star the repository** to show your support!
- 🐛 **Open an issue** if you find a bug or have a feature request.
- 📬 **Share feedback**—constructive criticism is always welcome as this portfolio project continues to grow.

---

## 👩‍💻 Developer

### Divya H Kishore

B.Tech Computer Science Engineering Student

GitHub:

https://github.com/Celestial-tech100

---

### "One dashboard. Every student need."

**AcaNexus : Studivo**
