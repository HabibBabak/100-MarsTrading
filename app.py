from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import os

# Initilize
app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'student'
app.config['SECRET_KEY'] = os.urandom(24)

# Initilization of MySQL
mysql = MySQL(app)

# create sql connection Routes
@app.route('/', methods = ['GET'])
def index():
    cur = mysql.connection.cursor()             # create sql connection 
    cur.execute("SELECT * FROM student_info")   # sql command
    data = cur.fetchall()                       #fetch all the data 
    cur.close()                                  # close the connection

    return render_template('index.html', data = data)

# home 
@app.route('/home')
def home():
    return render_template('home.html')

# sign In route
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Create connection
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM student_info WHERE username = %s AND password = %s", (username, password))
        
        user = cur.fetchall()
        if user:
            print('value', user[0][0])
            session["user_id"] = user[0][0]             # give access to specific info to user
            return redirect(url_for("dashboard"))
        
    return render_template('sign_in.html')
#dashboard
@app.route('/dashboard', methods=["GET"])
def dashboard():
    user_id = session.get("user_id")
    #print("The user id is ", data) # it will show the user id store the user info specially id 
    
    # create connection
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM course WHERE id = %s", (user_id,))
    data = cur.fetchall()

    return render_template("dashboard.html", data = data)

# Sign out


#add a course
@app.route('/course_post', methods=["GET", "POST"])
def course_post():
    if request.method == "POST":
        course_name = request.form["course_name"]
        user_id = session.get("user_id")

    #create connection
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO course (course_name, id ) VALUES (%s,%s)', (course_name, user_id))
        cur.connection.commit()
        
        cur.close()
        return redirect(url_for("dashboard"))

    return render_template("course_post.html")

# sign up route
@app.route('/sign_up', methods=['GET', "POST"])
def sign_up():
    if request.method == 'POST':
        #name = request.form['full_name']
        username = request.form['username']
        password = request.form['password']
        
        # Send Data to database
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO student_info (username,password) VALUES (%s,%s)', (username,password))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('index'))

    return render_template('sign_up.html')

#update route 
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
        cur = mysql.connection.cursor()
        if request.method == "POST":
            name = request.form['full_name']
            username = request.form['username']
            password = request.form['password']

            cur.execute("UPDATE student_info SET name = %s, username = %s, password = %s WHERE id = %s", (name, username, password, id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for ("dashboard"))
        cur.execute("SELECT * FROM student_info WHERE id = %s", (id,))
        data = cur.fetchall()

        print(data)
        return render_template('update.html', data=data)




# Run the server
if __name__ == '__main__':
    app.run()