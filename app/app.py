from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# "Base de datos" en memoria
tasks = [
    {"id": 1, "title": "Aprender Jenkins", "done": False},
    {"id": 2, "title": "Configurar pipeline CI/CD", "done": False},
    {"id": 3, "title": "Desplegar en producción", "done": False},
]
next_id = 4


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "app": "DevOps Demo App",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(task), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "El campo 'title' es requerido"}), 400
    new_task = {"id": next_id, "title": data["title"], "done": False}
    tasks.append(new_task)
    next_id += 1
    return jsonify(new_task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    data = request.get_json()
    if "title" in data:
        task["title"] = data["title"]
    if "done" in data:
        task["done"] = bool(data["done"])
    return jsonify(task), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Tarea eliminada"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
