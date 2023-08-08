from flask import Flask, render_template,redirect, url_for,request,session
import mysql.connector
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


#Homepage
@app.route("/")
def index():
    return render_template("home.html")


#Database connection
connection=mysql.connector.connect(host="localhost",port="#",user="#",passwd='#',database="quizdata")
cursor=connection.cursor()


#teacher registration
@app.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    if request.method == 'POST':
        name = request.form['user']
        address = request.form['address']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        #store data in database
        cursor.execute("INSERT INTO teachers (teachername, address, mobile,email,password) VALUES (%s, %s, %s, %s,%s)",
                    (name, address, mobile,email,password))
        connection.commit()
        cursor.close()
        return render_template('teacher_accessible.html') 
    return render_template('register_teacher.html')


#student registration
@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form['studentname']
        highestqualification = request.form['highestqualification']
        email = request.form['email']
        mobileno = request.form['mobileno']
        password = request.form['password']
        #store data in database
        cursor=connection.cursor()
        cursor.execute("INSERT INTO students (studentname, highestqualification, mobileno,email,password) VALUES (%s, %s, %s, %s,%s)",
                    (name, highestqualification, email,mobileno,password))
        connection.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register_student.html')


#Parents registration
@app.route('/register_parents', methods=['GET', 'POST'])
def register_parents():
    cursor=connection.cursor()
    cursor.execute("SELECT id, studentname FROM students")
    students = cursor.fetchall()
    print(students)
    if request.method == 'POST':
        name = request.form['parentname']
        mobileno = request.form['mobileno']
        email = request.form['email']
        address = request.form['address']
        child_name = request.form['child_name']
        password = request.form['password']
        #store data in database
        
        cursor.execute("INSERT INTO parents (parentname, mobileno, email,address,password,student_id) VALUES (%s, %s, %s, %s,%s,%s)",
                    (name, mobileno, email,address,password,child_name))
        connection.commit()
        cursor.close()
        return redirect(url_for('success'))
    return render_template('register_parent.html',students=students)




#login
@app.route('/login',methods=['GET', 'POST'])
def login():
    cursor=connection.cursor()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        #fetching student id using session
        cursor.execute("SELECT id FROM students WHERE studentname = %s AND password = %s", (username, password))
        student = cursor.fetchone()
        print(student)
        if student:
            session['student_id'] = student[0]  
            student_id = session.get('student_id')
            print(student_id)

        cursor.execute("SELECT password FROM teachers WHERE teachername = %s", (username,))
        teacher_result = cursor.fetchone()
        cursor.execute("SELECT password FROM students WHERE studentname = %s", (username,))
        student_result = cursor.fetchone()
        cursor.execute("SELECT password FROM parents WHERE parentname = %s", (username,))
        parent_result = cursor.fetchone()
        
        results=[teacher_result,student_result,parent_result]
        if teacher_result and student_result and parent_result==None:
            error="invalid username or password"
        else:
            for i in results:
                if i!=None:
                    for j in i:
                        if j==password:
                            return redirect(url_for('quiz'))
                        else:
                            error= "invalid username or password"
    cursor.close()
    return render_template('login.html',error=error,login_type='regular')




#submit quiz
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quizquestions")
    questions = cursor.fetchall()
    cursor.close()
    score = 0
    user_answers = {}
    
    for question in questions:
        user_answer = request.form.get('question' + str(question['id']))
        user_answers[question['id']] = user_answer
        user_name = session.get('username')
        student_id=session.get('student_id')
        print(user_name,student_id)
        
        # Fetch the correct option from the database
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT correct_option FROM quizquestions WHERE id = %s", (question['id'],))
        correct_option = cursor.fetchone()['correct_option']
    
        
        if user_answer == correct_option:
            score += 1

    cursor.execute("INSERT INTO quizscores (student_id, user_name, score) VALUES (%s, %s, %s)",(student_id, user_name, score))
    connection.commit()
    cursor.close()

    
    
    return render_template('quiz_result.html', score=score, user_answers=user_answers,user_name=user_name)


#accessing question from database
@app.route('/quiz', methods=['GET'])
def quiz():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quizquestions")
    questions = cursor.fetchall()
    cursor.close()
    
    return render_template('quiz.html', questions=questions)


#teacher login for accessing information
@app.route('/teacher_login',methods=['GET', 'POST'])
def teacher_login():
    
    error = None
    if request.method == 'POST':
        cursor = connection.cursor()
        username = request.form['username']
        pwd = request.form['password']
        cursor.execute("SELECT password FROM teachers WHERE teachername = %s", (username,))
        teacher_password = cursor.fetchone()
        cursor.close()
        if teacher_password is None:
            error = "Invalid username or password"
        elif teacher_password[0] == pwd:
            return render_template('teacher_accessible.html')  # Password is correct
        else:
            error = "Invalid username or password"
                
                
    return render_template('login.html',error=error,login_type='teacher')

#scores
@app.route('/show_score')
def show_score():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quizscores")
    scores = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('score_data.html', scores=scores)


#students info
@app.route('/show_students')
def show_students():
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    connection.close()
    return render_template('student_table.html', students=students)



#parents info
@app.route('/show_parents')
def show_parents():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM parents")
    parents = cursor.fetchall()
    cursor.close()
    
    return render_template('parents_table.html', parents=parents)







@app.route('/success')
def success():
    return "registered successfully!"
if __name__=='__main__':
    app.run(debug=True)