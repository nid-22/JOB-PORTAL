
from flask import *
import pymysql




app = Flask(__name__, template_folder='template')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')




@app.route("/signup", methods=['POST'])
def signup():

    username = request.form['username']
    email = request.form['email']
    dob = request.form['dob']
    location = request.form['location']
    gender = request.form['gender']
    password = request.form['password']
    msg=''
    try:
        myconn = pymysql.connect(host='localhost', user = 'root', password = '', database='flask_app')
        cursor = myconn.cursor()
        sql="insert into profiles_app(username,email,dob,location,gender,password) values('{}','{}','{}','{}','{}','{}')".format(username,email,dob,location,gender,password)
        cursor.execute(sql)
        if cursor.rowcount > 0:
            myconn.commit()
            msg = "registration done"
        else:
            myconn.rollback()
            msg = "try again"
    except Exception as e:
        msg = '{}, try again'.format(e)
        myconn.rollback()
    finally:
        myconn.close()
        return render_template("home.html", msg=msg)

@app.route("/signup/emp", methods=['POST'])
def emp():

    company_name = request.form['company_name']
    email = request.form['email']
    location = request.form['location']
    password = request.form['password']

    msg=''
    try:
        myconn = pymysql.connect(host='localhost', user = 'root', password = '', database='flask_app')
        cursor = myconn.cursor()
        sql="insert into profiles_app(email,location,password,company_name) values('{}','{}','{}','{}')".format(email,location,password,company_name)
        cursor.execute(sql)
        if cursor.rowcount > 0:
            myconn.commit()
            msg = "registration done"
        else:
            myconn.rollback()
            msg = "try again"
    except Exception as e:
        msg = '{}, try again'.format(e)
        myconn.rollback()
    finally:
        myconn.close()
        return render_template("home.html", msg=msg)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/emp')
def regisemp():
    return render_template('registeremp.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/logininfo', methods=['POST'])
def logininfo():
    email = request.form['email']
    password = request.form['password']
    error = None
    try:
        myconn = pymysql.connect(host='localhost', user='root', password='', database='flask_app')
        cursor = myconn.cursor()
        sql = "select * from profiles_app where email='{}' and password='{}'".format(email, password)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) > 0:
            if data[0][6] == None:
                resp = make_response(render_template('dashboard.html'))
                resp.set_cookie('email', email)
            else:
                resp = make_response(render_template('dashboardemp.html'))
                resp.set_cookie('email', email)
            return resp
        else:
            return "invalid id and password"
    except Exception as e:
        msg = '{}, try again '.format(e)

    finally:
        myconn.close()
        #return render_template('error.html',msg=msg)


@app.route('/viewprofile')
def profile():
    email = request.cookies.get('email')
    myconn = pymysql.connect(host='localhost', user='root', password='', database='flask_app')
    cursor = myconn.cursor()

    sql = "select * from applications where posted_by='{}'".format(email)
    cursor.execute(sql)
    data = cursor.fetchall()

    if email:
        resp = make_response(render_template('profile.html', name=email,data=data))
    else:
        resp = make_response(render_template('dashboard.html'))
    return resp



@app.route('/logout')
def logout():
    email = request.cookies.get('email')
    if email:
        resp = make_response(render_template('home.html', name=email))
        resp.set_cookie('email','',expires=0)
        resp.delete_cookie('email')
        return resp
    else:
        resp = make_response(render_template('home.html', name=email))
        return resp

@app.route('/postjob', methods=['GET','POST'])
def postjob():
    email = request.cookies.get('email')
    if email:
        resp = make_response(render_template('postjob.html', name=email))
    else:
        resp = make_response(render_template('dashboard.html'))
    return resp


@app.route("/posted", methods=['POST'])
def posted():

    title = request.form['title']
    company_name = request.form['company_name']
    location = request.form['location']
    description = request.form['description']
    contact = request.form['contact']
    date_posted = request.form['date_posted']
    posted_by = request.form['posted_by']
    msg=''
    try:
        myconn = pymysql.connect(host='localhost', user = 'root', password = '', database='flask_app')
        cursor = myconn.cursor()
        sql="insert into dashboard_jobs(title,company_name,location,description,contact,date_posted,posted_by) values('{}','{}','{}','{}','{}','{}','{}')".format(title,company_name,location,description,contact,date_posted,posted_by )
        cursor.execute(sql)
        if cursor.rowcount > 0:
            myconn.commit()
            msg = "job posted"
        else:
            myconn.rollback()
            msg = "try again"
    except Exception as e:
        msg = '{}, try again'.format(e)
        myconn.rollback()
    finally:
        myconn.close()
        return render_template("dashboard.html")

@app.route('/dashboard')
def dashboard():


    myconn = pymysql.connect(host='localhost', user='root', password='', database='flask_app')
    cursor = myconn.cursor()
    sql = "select * from dashboard_jobs"
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('dashboard.html', data=data)

@app.route('/dashboardemp')
def dashboardemp():


    myconn = pymysql.connect(host='localhost', user='root', password='', database='flask_app')
    cursor = myconn.cursor()
    sql = "select * from dashboard_jobs"
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('dashboardemp.html', data=data)


@app.route('/apply/<int:job_id>', methods=['POST','GET'])
def apply(job_id):
    email = request.cookies.get('email')
    try:
        myconn = pymysql.connect(host='localhost', user='root', password='', database='flask_app')
        cursor = myconn.cursor()
        cursor.execute("SELECT * FROM dashboard_jobs WHERE id={}".format(job_id))
        row = cursor.fetchone()
        if row:
            msg='successfull'
            if email:
                resp = make_response(render_template('apply.html', name=email, row=row))
            else:
                resp = make_response(render_template('dashboard.html'))
            return resp

    except Exception as e:
        msg = '{}, try again'.format(e)
        return render_template("error.html", msg=msg)
    finally:

        myconn.close()






@app.route('/application', methods=['POST','GET'])
def application():
    email = request.form['email']
    dob = request.form['dob']
    location = request.form['location']
    resume = request.form['resume']
    job_id = request.form['id']
    posted_by = request.form['posted_by']

    try:
        myconn = pymysql.connect(host='localhost', user='root', password='', database='flask_app')
        cursor = myconn.cursor()
        sql = "insert into applications(email,dob,location,resume,job_id,posted_by) values('{}','{}','{}','{}',{},'{}')".format(email, dob, location,resume,job_id,posted_by)
        cursor.execute(sql)
        if cursor.rowcount > 0:
            myconn.commit()
            msg = "job applied"
        else:
            myconn.rollback()
            msg = "try again"
    except Exception as e:
        msg = '{}, try again'.format(e)
        myconn.rollback()
    finally:
        myconn.close()
        return render_template("dashboard.html")


if __name__ == '__main__':
    app.run(debug=True)