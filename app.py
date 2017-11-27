from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import sqlite3
import os
from sqlite3 import Error

 
app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect('/dashboard')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


@app.route('/student/add', methods=['GET', 'POST'])
def page_AddStudent():
    error = None
    if request.method == "POST":
        try:
            sqlite_file = 'hw13.db'
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute('insert into tbl_students (first_name, last_name) values (?,?)', (request.form['first_name'], request.form['last_name']))
            conn.commit()
            msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("result.html",msg = msg)
            con.close()           
    return render_template("page_add_student.html", error=error) 


@app.route('/dashboard', methods=['GET'])
def dshboard():
    try:
        sqlite_file = 'hw13.db'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute('SELECT * FROM tbl_students')
        students_all_rows = c.fetchall()
        conn.close
    except Error as e:
        print(e)
    return render_template("dashboard.html", students_all_rows=students_all_rows)


@app.route('/quizzes', methods=['GET'])
def quizzes():
    try:
        sqlite_file = 'hw13.db'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute('SELECT * FROM tbl_quizzes')
        quizzes_all_rows = c.fetchall()
        conn.close
    except Error as e:
        print(e)
    return render_template("quizzes.html", quizzes_all_rows=quizzes_all_rows)



@app.route('/quizzes/add', methods=['GET', 'POST'])
def page_AddQuizzes():
    error = None
    if request.method == "POST":
        try:
            sqlite_file = 'hw13.db'
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute('insert into tbl_quizzes (subject, question_count, quiz_date) values (?,?,?)', (request.form['subject'], request.form['question_count'], request.form['quiz_date']))
            conn.commit()
            msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("result.html",msg = msg)
            con.close()           
    return render_template("page_add_quizzes.html", error=error)


@app.route('/student/<studentid>', methods=['GET', 'POST'])
def page_quizResults(studentid):
    quiz_results = ""    
    sqlite_file = 'hw13.db'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT tbl_students.first_name, tbl_students.last_name, tbl_quizzes.subject, tbl_student_quiz_results.score,'+
        ' tbl_quizzes.quiz_date FROM tbl_student_quiz_results JOIN tbl_students ON'+
        ' tbl_student_quiz_results.student_id = students_id JOIN tbl_quizzes ON tbl_student_quiz_results.quiz_id = quizzes_id Where students_id =' + str(studentid))
    quiz_results = c.fetchall()
    return render_template("view_result.html", quiz_results = quiz_results)
            

@app.route("/results/add", methods = ["POST", "GET"])
def addresult():
    error = None
    sqlite_file = 'hw13.db'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT * FROM tbl_students')
    student = c.fetchall()
    c.execute('SELECT * FROM tbl_quizzes')
    quiz = c.fetchall()
    if request.method == 'POST':
        if request.form['student'] == '' or request.form['quiz'] == ''\
                or request.form['score'] == '':
            error = 'Please Enter Valid Input (Fields can not be blank)'
        else:
            student = request.form['student']
            quiz = request.form['quiz']
            score = request.form['score']
            c.execute(
                'INSERT into tbl_student_quiz_results(student_id, quiz_id, score) VALUES (?,?,?)',
                (student, quiz, score))
            conn.commit()
            return redirect('/dashboard')
    return render_template('add_quiz_results.html', error=error, student=student, quiz=quiz)
    

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()    
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
