from flask_restful import Resource, fields, marshal
from flask import make_response, jsonify, request
from models.model import Task, User
from database import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_socketio import emit
from app import socketio

task_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "completed": fields.Boolean,
}


class Todo(Resource):

    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            tasks = Task.query.filter_by(user_id=user_id).all()
            if tasks:
                return marshal(tasks, task_fields), 200
            return make_response(
                jsonify({"message": "No task left for you to complete!"}), 404
            )
        except Exception as e:
            return make_response(jsonify({"Database error occurred": str(e)}), 500)


    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            title = data.get("title", None)

            if not title:
                return make_response(jsonify({"message": "Task title is required"}), 400)

            user_id = get_jwt_identity()
            new_task = Task(title=title, user_id=user_id)
            db.session.add(new_task)
            db.session.commit()

            # Emit a SocketIO event when a task is added
            emit(
                "task_added", {"task": marshal(new_task, task_fields)}, broadcast=True, namespace="/"
            )

            return {
                "message": "Task Added Successfully!",
                "task": marshal(new_task, task_fields),
            }, 201
        except Exception as e:
            return make_response(jsonify({"Database error": str(e)}), 500)


    @jwt_required()
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            get_task = Task.query.filter_by(id=id, user_id=user_id).first()

            if get_task:
                data = request.get_json()
                task_title = data.get("title")
                completed = data.get("completed")

                if task_title is not None:
                    get_task.title = task_title
                if completed is not None:
                    get_task.completed = completed

                db.session.commit()

                # Emit a SocketIO event when a task is updated
                emit(
                    "task_updated", {"task": marshal(get_task, task_fields)}, broadcast=True, namespace="/"
                )

                return {
                    "message": "Task Updated Successfully!",
                    "task": marshal(get_task, task_fields),
                }, 200

            return make_response(jsonify({"message": "No Task Found for this user!"}), 404)
        except Exception as e:
            print(e)
            return make_response(jsonify({"error": str(e)}), 500)


    @jwt_required()
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            get_task = Task.query.filter_by(id=id, user_id=user_id).first()
            if get_task:
                db.session.delete(get_task)
                db.session.commit()

                # Emit a SocketIO event when a task is deleted
                emit("task_deleted", {"id": id}, broadcast=True, namespace="/")

                return make_response(
                    jsonify({"message": "Task Deleted Successfully!"}), 200
                )

            return make_response(jsonify({"message": "No Task Found for this user!"}), 404)
        except Exception as e:
            return make_response(jsonify({"Database error": str(e)}), 500)
