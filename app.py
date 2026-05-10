from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# Konfigurasi database dari environment variable
database_url = os.environ.get("DATABASE_URL")

# Jika tidak ada DATABASE_URL, gunakan SQLite lokal
if not database_url:
    database_url = "sqlite:///todo.db"

# Fix khusus Heroku PostgreSQL
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Model Todo
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tugas = db.Column(db.String(200), nullable=False)

# Membuat tabel otomatis
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

# Health check
@app.route('/health')
def cek_kesehatan():
    return jsonify({
        'status': 'sehat'
    })

# Ambil semua todo
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()

    hasil = []

    for todo in todos:
        hasil.append({
            'id': todo.id,
            'tugas': todo.tugas
        })

    return jsonify(hasil)

# Tambah todo
@app.route('/todos', methods=['POST'])
def tambah_todo():
    data = request.get_json()

    todo_baru = Todo(
        tugas=data['tugas']
    )

    db.session.add(todo_baru)
    db.session.commit()

    return jsonify({
        'pesan': 'Todo berhasil ditambahkan'
    })

# Hapus todo
@app.route('/todos/<int:id>', methods=['DELETE'])
def hapus_todo(id):
    todo = Todo.query.get(id)

    if not todo:
        return jsonify({
            'error': 'Todo tidak ditemukan'
        }), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({
        'pesan': 'Todo berhasil dihapus'
    })

# Menjalankan aplikasi
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)