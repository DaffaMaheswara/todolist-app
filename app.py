from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Environment variable
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Database config
DATABASE_URL = os.environ.get('DATABASE_URL')


if not DATABASE_URL:
    DATABASE_URL = 'sqlite:///todo.db'


if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Model Todo
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tugas = db.Column(db.String(200), nullable=False)

# tabel 
with app.app_context():
    db.create_all()

# Endpoint utama
@app.route('/')
def beranda():
    return jsonify({
        'pesan': 'API To-Do List',
        'status': 'aktif',
        'versi': '1.0.0'
    })

# Endpoint dashboard
@app.route('/dashboard')
def dashboard():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

# Endpoint tambah todo
@app.route('/tambah', methods=['POST'])
def tambah_todo():
    tugas = request.form.get('tugas')

    if tugas:
        todo_baru = Todo(tugas=tugas)
        db.session.add(todo_baru)
        db.session.commit()

    return redirect('/dashboard')


# Endpoint hapus todo
@app.route('/hapus/<int:id>', methods=['POST'])
def hapus_todo(id):
    todo = Todo.query.get(id)

    if todo:
        db.session.delete(todo)
        db.session.commit()

    return redirect('/dashboard')

# Health check
@app.route('/health')
def cek_kesehatan():
    return jsonify({
        'status': 'sehat'
    })

#  API endpoint
@app.route('/api/todos')
def api_todos():
    todos = Todo.query.all()

    hasil = []

    for todo in todos:
        hasil.append({
            'id': todo.id,
            'tugas': todo.tugas
        })

    return jsonify(hasil)


# Run App
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)