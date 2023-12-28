from flask import Flask,render_template,request,redirect,url_for,flash
import mysql.connector

#establishing Mysql connection
connection = mysql.connector.connect(host='Bindukala.mysql.pythonanywhere-services.com',user='Bindukala',password='binduhari@19815god',database='Bindukala$project')
mycursor = connection.cursor()


#name and id details added for login
user_dict={'bindu':'101','hari':'102','kala':'103','indu':'104','sruthy':'108'}

#defining home

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('task_index.html')

#defining login
@app.route('/login')
def login():
    return render_template('login.html')


#checking login details
@app.route('/emp_home', methods=['POST'])
def emp_home():
    name=request.form['name']
    staff_id=request.form['staff_id']
    if name not in user_dict:
        return render_template('login.html', msg='Invalid Username')
    elif user_dict[name]!=staff_id:
        return render_template('login.html', msg='Invalid Id')
    else:
         return projects()
    

#Displaying Staff list
@app.route('/staff')
def staff():
    query = "SELECT * FROM staff"
    mycursor.execute(query)
    data = mycursor.fetchall()
    return render_template('staff.html',sqldata=data)



#Displaying project list
@app.route('/projects')
def projects():
    query = "SELECT * FROM projects"
    mycursor.execute(query)
    data = mycursor.fetchall()
    return render_template('projects.html',sqldata=data)


#New User Registration
@app.route('/register')
def register():
    return render_template('register.html')


#Adding new task/project
@app.route('/add_projects')
def add_projects():
    return render_template('update.html')



#New registration aaded in to staff list table
@app.route('/register',methods=['GET','POST'])
def read():
    if request.method=='POST':
        name=request.form.get('name')
        staff_id=request.form.get('staff_id')
        dept=request.form.get('dept')
        mail_id=request.form.get('mail_id')
     

        query="INSERT INTO staff VALUES (%s,%s,%s,%s)"
        data=(name,staff_id,dept,mail_id)

        
        mycursor.execute(query,data)
        connection.commit()
        return staff()
    

#Adding new projects into project list
@app.route('/addProject',methods=['GET','POST'])
def addProject():
    if request.method=='POST':
       
        project=request.form.get('project')
        in_charge=request.form.get('in_charge')
        starting_date=request.form.get('starting_date')
        due_date=request.form.get('due_date')
        status=request.form.get('status')
        id=request.form.get('id')
     

        query="INSERT INTO projects VALUES (%s,%s,%s,%s,%s,%s)"
        data=(project,in_charge,starting_date,due_date,status,id)

        mycursor.execute(query,data)
        connection.commit()
        return projects()
    return render_template('task_update.html')



#Editing/Updating Project details
@app.route('/edit_project/<string:project>', methods=['GET', 'POST'])
def edit_project(project):
    if request.method == 'POST':
        # Handle form submission (update the project in the database)
        updated_project = request.form.get('project')
        in_charge = request.form.get('in_charge')
        starting_date = request.form.get('starting_date')
        due_date = request.form.get('due_date')
        status = request.form.get('status')
        id = request.form.get('id')

        query = "UPDATE projects SET project=%s, in_charge=%s, starting_date=%s, due_date=%s, status=%s, id=%s WHERE project=%s"
        data = (updated_project, in_charge, starting_date, due_date, status, id, project)

        mycursor.execute(query, data)
        connection.commit()

        return redirect(url_for('projects'))

    else:
        mycursor.execute("SELECT * FROM projects WHERE project = %s", (project,))
        project_data = mycursor.fetchone()
        return render_template('edit_project.html', project=project_data)    

    
#Deleting the task/project    
@app.route('/delete/<string:project>', methods=['GET', 'POST'])
def delete(project):        
        mycursor.execute("DELETE FROM projects WHERE project = %s", (project,))
        connection.commit()
        return projects() 

#Filtering the project based on completion status
@app.route('/projects/<status>', methods=['GET'], endpoint='filtered_projects')
def filtered_projects(status):
    query = "SELECT * FROM projects WHERE status = %s"
    mycursor.execute(query, (status,))
    data = mycursor.fetchall()
    return render_template('projects.html', sqldata=data)



