from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from types import SimpleNamespace
import certifi
import os

# Load env vars
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")
app.config["TESTING"] = os.getenv("TESTING", "").lower() in ("1", "true", "yes")
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")


def normalize_id(value):
    if isinstance(value, ObjectId):
        return value
    if isinstance(value, str):
        try:
            return ObjectId(value)
        except Exception:
            return value
    return value


class InMemoryCollection:
    def __init__(self):
        self._documents = []

    def find(self):
        return list(self._documents)

    def find_one(self, query):
        for document in self._documents:
            if self._matches(document, query):
                return dict(document)
        return None

    def insert_one(self, document):
        new_document = dict(document)
        if "_id" not in new_document:
            new_document["_id"] = str(len(self._documents) + 1)
        self._documents.append(new_document)
        return SimpleNamespace(inserted_id=new_document["_id"])

    def update_one(self, query, update):
        for index, document in enumerate(self._documents):
            if self._matches(document, query):
                updated_document = dict(document)
                for key, value in update.get("$set", {}).items():
                    updated_document[key] = value
                self._documents[index] = updated_document
                return SimpleNamespace(modified_count=1)
        return SimpleNamespace(modified_count=0)

    def delete_one(self, query):
        for index, document in enumerate(self._documents):
            if self._matches(document, query):
                del self._documents[index]
                return SimpleNamespace(deleted_count=1)
        return SimpleNamespace(deleted_count=0)

    def delete_many(self, query):
        remaining_documents = []
        deleted_count = 0
        for document in self._documents:
            if self._matches(document, query):
                deleted_count += 1
            else:
                remaining_documents.append(document)
        self._documents = remaining_documents
        return SimpleNamespace(deleted_count=deleted_count)

    @staticmethod
    def _matches(document, query):
        return all(document.get(key) == normalize_id(value) for key, value in query.items())


class InMemoryDatabase:
    def __init__(self):
        self.students = InMemoryCollection()


class InMemoryMongo:
    def __init__(self, database_name="student_db"):
        self.cx = self
        self.db = InMemoryDatabase()
        self.database_name = database_name

    def drop_database(self, database_name):
        self.db = InMemoryDatabase()
        self.database_name = database_name


# Use certifi CA bundle explicitly for cross-platform TLS reliability
# (notably fixes common macOS certificate verification failures).
if app.config.get("TESTING") or not app.config.get("MONGO_URI"):
    mongo = InMemoryMongo()
else:
    mongo = PyMongo(app, tlsCAFile=certifi.where())

# Home page -> list students
@app.route('/')
def index():
    students = mongo.db.students.find()
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        mongo.db.students.insert_one({
            "name": name,
            "email": email,
            "course": course
        })
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Update student
@app.route('/update/<student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = mongo.db.students.find_one({"_id": normalize_id(student_id)})
    if request.method == 'POST':
        new_name = request.form['name']
        new_email = request.form['email']
        new_course = request.form['course']
        mongo.db.students.update_one(
            {"_id": normalize_id(student_id)},
            {"$set": {"name": new_name, "email": new_email, "course": new_course}}
        )
        return redirect(url_for('index'))
    return render_template('update_student.html', student=student)


# Delete student
@app.route('/delete/<student_id>')
def delete_student(student_id):
    mongo.db.students.delete_one({"_id": normalize_id(student_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)


