from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3

app = Flask(__name__)
app.secret_key = "Secret Key"

DATABASE = 'data.db'
# @app.before_first_request
# def create_all():
#     # db.create_all()



@app.route('/', methods=['POST', 'GET'])
def home():
    
    return render_template("index.html", projects = getProjects(), tasks = getTasks())

@app.route('/add_project', methods=['POST'])
def addProject():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO projects('project') VALUES('{request.form['project_input']}')")
    connection.commit()
    return redirect('/')

@app.route('/add_task', methods=['POST'])
def addTask():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO tasks('project', 'task', 'finished') VALUES('{request.form['project']}', '{request.form['task_input']}', 0)")
    connection.commit()
    return redirect('/')

@app.route('/delete_task', methods=['POST'])
def deleteTask():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM tasks WHERE ID = '{request.form['taskID']}'")
    connection.commit()
    return redirect('/')

@app.route('/delete_project', methods=['POST'])
def deleteProject():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM projects WHERE project = '{request.form['project']}'")
    connection.commit()

    # tasks = getProjectsTasks(request.form['project'])
    # for task in tasks:
    cursor.execute(f"DELETE FROM tasks WHERE project = '{request.form['project']}'")
    connection.commit()

    return redirect('/')

@app.route('/complete_toggle', methods=['POST'])
def updateComplete():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"UPDATE tasks SET 'finished' = {request.form['complete']} WHERE ID = '{request.form['taskID']}'")
    connection.commit()
    return redirect('/')

def getProjectsTasks(project):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    tasks = cursor.execute(f"SELECT * FROM tasks WHERE project = '{project}'")
    return tasks

def getProjects():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    projects = cursor.execute(f"SELECT project FROM projects")
    connection.commit()
    projectReturns = []
    for project in projects:
        projectReturns.append(project[0])
    return projectReturns

def getTasks():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    projects = getProjects()

    returnTasks = {}
    for project in projects:
        tasks = cursor.execute(f"SELECT * FROM tasks WHERE project = '{project}'")
        
        connection.commit()
        taskList = []
        for task in tasks:
            subTaskList = []
            complete = False
            if (task[3] == 1):
                complete = True
            subTaskList.append(task[1])
            subTaskList.append(task[2])
            subTaskList.append(complete)
            taskList.append(subTaskList)
        returnTasks[project] = taskList
    return returnTasks
