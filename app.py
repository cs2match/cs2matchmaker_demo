from flask import Flask, jsonify, request
import uuid, json
import re, os

app = Flask(__name__)

uuuu = uuid.uuid4()
app.config['SECRET_KEY'] = str(uuuu)

STUDENTS_JSON_PATH = os.path.join(os.path.dirname(__file__), "templates", "students.json")

def load_students_data():
    with open(STUDENTS_JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data

@app.route("/students", methods=["GET"])
def get_students():
    data = load_students_data()
    return jsonify(data["students"])

@app.route("/students/list", methods=["GET"])
def get_students_list():
    data = load_students_data()
    # students 배열만 반환
    return jsonify({"students": data.get("students", [])})

@app.route("/students/<int:student_id>", methods=["GET"])
def get_student_by_id(student_id):
    data = load_students_data()
    students = data.get("students", [])
    for student in students:
        if student["id"] == student_id:
            return jsonify(student)
    return jsonify({"error": "학생이 존재하지 않습니다."}), 404

def validate_registration(data):
    errors = {}
    username = data.get('username')
    if not username or not (4 <= len(username) <= 20):
        errors['username'] = "아이디는 4~20자여야 합니다."
    email = data.get('email')
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors['email'] = "올바른 이메일 형식이 아닙니다."
    password = data.get('password')
    if not password or not (4 <= len(password) <= 20):
        errors['password'] = "비밀번호는 4~20자여야 합니다."
    confirm_password = data.get('confirm_password')
    if password != confirm_password:
        errors['confirm_password'] = "비밀번호가 일치하지 않습니다."
    return errors

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    errors = validate_registration(data)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400
    return jsonify({"success": True, "message": f"{data['username']} 님 가입 완료!"})

@app.route("/home", methods=["GET"])
def home():
    return jsonify({"message": "This is the home page."})

@app.route("/index", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello World!_index", "uuid": str(uuuu)})

@app.route('/user/<user_name>/<int:user_id>/<uuid:same_uuid>', methods=["GET"])
def user(user_name, user_id, same_uuid):
    if uuuu == same_uuid:
        return jsonify({
            "message": f"hello, {user_name}({user_id})",
            "uuid": str(uuuu)
        })
    else:
        return jsonify({"error": "Access Denied: Invalid UUID."}), 403

if __name__ == "__main__":
    app.run(debug=True)
