from flask_restful import Resource, fields, marshal
from flask import make_response, jsonify, request
from models.model import Task
from database import db


task_fields={
  "id": fields.Integer,
  "title": fields.String,
  "completed" : fields.Boolean
}


class Todo(Resource):
    
    def get(self):
        try:
            tasks = Task.query.all()
            return marshal(tasks, task_fields), 200
        except Exception as e:
            return jsonify({"Database error occured": str(e)}), 500

    

    def post(self):
        
        try:
            data = request.get_json()
            title = data.get("title", None)

            new_task = Task(title=title)
            db.session.add(new_task)
            db.session.commit()
            return {"Task Added Successfully!": marshal(new_task, task_fields)}, 201
        except Exception as e:
            return jsonify({"Database error": str(e)}), 500
    


    def put(self, id):

        try:
            get_task = Task.query.filter_by(id=id).first()

            if get_task:
                data = request.get_json()
                task_title = data.get("title")  
                completed = data.get("completed")

                if task_title is not None:
                    get_task.title = task_title
                if completed is not None:
                    get_task.completed = completed

                db.session.commit()
                return {"Task Updated Successfully!": marshal(get_task, task_fields)}, 200
            
            return jsonify("No Task Found!"), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    

    
    def delete(self, id):

        try:
            get_task = Task.query.filter_by(id=id).first()
            if get_task:
                db.session.delete(get_task)
                db.session.commit()
                return make_response(jsonify("Task Deleted Successfully!"), 200)
            
            return jsonify("No Task Found!"), 404
        except Exception as e:
            return jsonify({"Database err": str(e)}), 500

