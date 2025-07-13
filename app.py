from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm

import uuid
uuuu = uuid.uuid4()

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuuu)

student_data = {
    1: {"name": "슈퍼맨", "score": {"국어": 90, "수학": 65}},
    2: {"name": "배트맨", "score": {"국어": 75, "영어": 80, "수학": 75}}
}

@app.route("/")
def index():
   return render_template("index.html", template_students = student_data)
def home():
    return render_template('layout.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'{form.username.data} 님 가입 완료!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',form=form)
@app.route("/student/<int:id>")
def student(id):
    return render_template("student.html",
                           template_name = student_data[id]["name"],
                           template_score = student_data[id]["score"])

@app.route("/index")
def hello_world():
    return f"Hello World!_index, {uuuu}"

@app.route('/user/<user_name>/<int:user_id>/<uuid:same_uuid>')
def user(user_name, user_id, same_uuid):
    if uuuu == same_uuid:
        return f'hello, {user_name}({user_id}),{uuuu}'
    else:
        return 'Access Denied: Invalid UUID.',403


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)