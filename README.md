<h1 align="center">Tavyar Educational Platform</h1>
<p align="center">
  <img src="images/tavyarr.png" alt="Tavyar Logo" width="200" />
</p>

**Tavyar** is a modern educational platform designed to empower learners with high-quality, engaging courses. Built with Django, MySQL, and front-end technologies (HTML, CSS, JavaScript), Tavyar provides a seamless experience for students and instructors to connect, learn, and grow.

---

## 🚀 Features

- User registration and authentication  
- Secure SMS code verification (optional)  
- Instructor and student roles  
- Course creation and enrollment  
- Lesson and module management  
- Responsive front-end with clean, modern UI  
- Payment gateway integration (planned)  
- Robust MySQL data storage  
- Admin dashboard  
- Scalable and extensible architecture

---

## 🛠️ Tech Stack

- **Backend**: Django 5.2.3
- **Database**: MySQL 8
- **Frontend**: HTML5, CSS3, JavaScript  
- **Authentication**: Django’s built-in system (with extensibility for social login)  
- **Deployment**: Gunicorn + Nginx (recommended)  
- **Containerization**: Docker (optional)

---

## 📦 Installation

**Step 1: Clone the repository**

```bash
git clone https://github.com/yourusername/tavyar.git
cd tavyar
```

**Step 2: Set up your virtual environment**

```bash
python -m venv venv
```

**Step 3: active your virtual environment**


- ***for linux:***
```bash
source venv/bin/activate
```


- ***for windows:***
```bash
venv\Scripts\activate
```


**Step 4: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 5: Configure MySQL database**

Create the database in MySQL:

```sql
CREATE DATABASE tavyar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Update your `tavyar/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tavyar',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**Step 6: Apply migrations**

```bash
python manage.py migrate
```

**Step 7: Create superuser**

```bash
python manage.py createsuperuser
```

**Step 8: Run the development server**

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to see Tavyar running locally.

---

## 🧩 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/amazing-feature`)  
3. Commit your changes  
4. Push to your branch  
5. Open a pull request

---

## 🛡️ Security

If you discover a security vulnerability, please open an issue or contact the maintainers directly.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Authors

- **Pourya Janparvar** 
- 

---

## 🌟 Acknowledgments

- Django Community  
- MySQL Community  
- OpenAI ChatGPT for drafting inspiration  
- All developers and educators who believe in open, accessible learning







