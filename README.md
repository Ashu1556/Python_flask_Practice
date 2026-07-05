# Student Registration System

A simple **Flask** web application to manage student records with **MongoDB** as the backend database. Users can **add, view, update, and delete** student details.

---

## CI/CD Status

This repository now includes both a Jenkins pipeline and a GitHub Actions workflow so the application can be tested automatically on every push and deployed from the staging or production branches/tags.

---

## Features

* List all students on the home page
* Add a new student
* Update existing student details
* Delete a student with confirmation
* Simple and responsive UI using Bootstrap

---

## Tech Stack

* **Backend:** Python, Flask
* **Database:** MongoDB (via Flask-PyMongo)
* **Frontend:** HTML, Jinja2 templates, Bootstrap 5
* **Environment Variables:** Managed via `.env` file

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Activate venv
# Windows:
venv\Scripts\activate
# Linux / Mac:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` example:**

```
Flask
Flask-PyMongo
python-dotenv
bson
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
MONGO_URI=<your-mongodb-connection-string>
SECRET_KEY=<your-secret-key>
```

### 5. Run the application

```bash
python app.py
```

Open your browser at: [http://localhost:8000](http://localhost:8000)

---

## Project Structure

```
project/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_student.html
│   ├── update_student.html
│
├── app.py
├── requirements.txt
└── .env
```

---

## Screenshots

**Home Page**
Lists all students with Edit/Delete buttons.
- <img width="1902" height="607" alt="image" src="https://github.com/user-attachments/assets/a58a6a6d-4978-4769-8074-232e4d31e69d" />


**Add Student**
Form to add a new student.
- <img width="1897" height="801" alt="image" src="https://github.com/user-attachments/assets/d65d25c3-ebb5-410a-adb1-e130ad7c5878" />


**Update Student**
Form pre-filled with student details.
- <img width="1905" height="897" alt="image" src="https://github.com/user-attachments/assets/04febf01-879f-431f-ab07-abcfb993acf1" />



---

## Jenkins Pipeline

1. Install Jenkins on a VM or use a cloud-hosted Jenkins instance.
2. Configure Jenkins with Python 3 and install the required packages from `requirements.txt`.
3. Create a pipeline job pointing to this repository and use the included `Jenkinsfile`.
4. Configure email notifications in Jenkins under the `post` section by replacing `your-email@example.com` with a valid address.
5. The pipeline runs three stages:
   - Build: install dependencies
   - Test: run the pytest suite
   - Deploy: print the deployment step for the main or staging branch

## GitHub Actions Workflow

1. Push changes to the `main` or `staging` branches to trigger the workflow.
2. Create a tag starting with `v` to trigger the production deployment job.
3. Add any deployment secrets in GitHub repository settings, for example:
   - `STAGING_DEPLOY_TOKEN`
   - `PRODUCTION_DEPLOY_TOKEN`
4. The workflow performs:
   - Install dependencies
   - Run tests
   - Deploy to staging for the `staging` branch
   - Deploy to production for version tags

## Notes

* Make sure MongoDB is running and accessible via the URI in `.env` when you use the live database path.
* The test suite is configured to run in a CI-safe in-memory mode when `TESTING=true` or when no MongoDB URI is provided.
* Delete action includes a confirmation page to prevent accidental deletion.
* Uses `ObjectId` from `bson` to work with MongoDB document IDs.
* If you use MongoDB Atlas on macOS, install dependencies again (`pip install -r requirements.txt`). This project now uses `certifi` CA bundle explicitly to avoid common TLS certificate verification failures with `pymongo`.

---

## License

MIT License

---



