from flask import render_template, request, current_app, session, g, redirect
from app import app
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from .forms import LoginForm
from .models import userRegist, userLogin, blogGet, courseGet, courseInfoGet, lessonListGet, lessonInfoGet, lessonInfoGet2
from .models import messageListGet, submissionListGet, contestListGet
from .models import contestListGet, contestInfoGet, contestProblemListGet, contestProblemGet
from .models import problemListGet, problemGet, submissionListGet, solutionListGet
from .models import codeGet, problemRankGet
from .models import addBlog, addCourse, addLesson, addSubmission, addProblem, addContestProblem
from .models import updateLesson
from .models import deleteBlog, deleteCourse, deleteLesson, deleteProblem
#from PIL import Image
import os

def isAdmin(name):
  if (name == 'admin'):
    return True
  return False


@app.route('/adminCourseDelete/<courseID>')
def adminCourseDelete(courseID):
  #if (not isAdmin(loginStatus())):
  #  return redirect('/home')
  deleteCourse(courseID)
  return redirect('/courses')

@app.route('/lessonDelete/<lessonID>')
def lessonDelete(lessonID):
  lessonID = int(lessonID)
  lessonInfo = lessonInfoGet2(lessonID)
  courseID = int(lessonInfo['courseID'])
  if (lessonInfo['teacher'] != loginStatus()):
    return redirect('/home')
  deleteLesson(lessonID)
  return redirect('/course/' + str(courseID))

@app.route('/deleteProblem/<ID>')
def deleteproblem(ID):
    print(type(ID))
    deleteProblem(ID)
    print("deleteProblem success")
    return redirect('/problems/problemList')
  #return render_template('deleteProblem.html',
  #  userName = loginStatus())

def store(file, ID):
  path = "app/static/course/" + str(ID)
  os.system("mkdir " + path)
  imgN = path + "/upload"
  #file.save(imgN)
  #im = Image.open(imgN)
  #im = im.resize((128, 128))
  im.save(path + "/img.jpg")

def storeIOFile(ifile, ofile, ID):
  path = os.path.abspath('.')+"/data/" + str(ID) + "/"
  print("path is" + path)
  if os.path.exists(path):
    pass
  else:
    print("dir not exist!")
    #os.system("mkdir " + path)
    os.makedirs(path)
  ifile.save(path + "1.in")
  ofile.save(path + "1.out")

def loginStatus():
  if (session.permanent == True):
    return session['username']
  else:
    return None

@app.route('/')
@app.route('/home')
def home():
  blogs = blogGet((0, 21))
  messages = messageListGet((0, 5), loginStatus())
  contests = contestListGet((0, 5))
  submissions = submissionListGet((0, 5), loginStatus(), None, None)
  return render_template('home.html',
    page = "home",
    userName = loginStatus(),
    blogs = blogs,
    messages = messages,
    contests = contests,
    submissions = submissions)

@app.route('/adminBlogAdd', methods = ['GET', 'POST'])
def adminBlogAdd():
  #if (not isAdmin(loginStatus())):
  #  return redirect('/home')
  if (request.method == 'POST'):
    addBlog(request.form)
    return redirect('/home') 
  return render_template('adminAddBlog.html',
    userName = loginStatus())

@app.route('/adminBlogDelete/<blogID>')
def adminBlogDelete(blogID):
  #content=blogID.split('+')
  #blogID = content[0]
  #blogAuthor = content[1]
  #if (not isAdmin(loginStatus())):
  #  return redirect('/home')
  deleteBlog(blogID)
  return redirect('/home')

@app.route('/adminCourseAdd', methods = ['GET', 'POST'])
def adminCourseAdd():
  #if (not isAdmin(loginStatus())):
  #  return redirect('/home')
  if (request.method == 'POST'):
    print("wtf?")
    ID = addCourse(request.form)
    #store(request.files['cImg'], ID)
    return redirect('/courses') 
  return render_template('adminCourseAdd.html',
    userName = loginStatus())

@app.route('/adminProblemAdd', methods = ['GET', 'POST'])
def adminProblemAdd():
  #if (not isAdmin(loginStatus())):
  #  return redirect('/home')
  if (request.method == 'POST'):
    r = request.form.copy()
    r.update({'creator' : loginStatus(), 'status' : 'close'})
    ID = addProblem(r)
    storeIOFile(request.files['inputF'], request.files['outputF'], ID)
    return redirect('/problems/problemList') 
  return render_template('adminProblemAdd.html',
    userName = loginStatus())

@app.route('/lessonAdd/<courseID>', methods = ['GET', 'POST'])
def lessonAdd(courseID):
  courseInfo = courseInfoGet(courseID)
  if (courseInfo['teacher'] != loginStatus()):
    return redirect('/home')
  if (request.method == 'POST'):
    r = {'name' : request.form['name'],
	'context': request.form['context'],
	'courseID' : courseID}
    print(r)
    addLesson(r)
    return redirect('/course/' + str(courseID)) 
  return render_template('lessonAdd.html',
    userName = loginStatus(),
    courseID = courseID)

@app.route('/lessonF/<lessonID>', methods = ['GET', 'POST'])
def lessonF(lessonID):
  lessonID = int(lessonID)
  lessonInfo = lessonInfoGet2(lessonID)
  if (lessonInfo['teacher'] != loginStatus()):
    return redirect('/home')
  if (request.method == 'POST'):
    r = {'name' : request.form['name'],
	'context': request.form['context'],
	'courseID' : lessonInfo['courseID'],
	'id' : lessonID}
    updateLesson(r)
    return redirect('/lesson/' + str(lessonID)) 
  print(lessonInfo)
  return render_template('lessonFix.html',
	userName = loginStatus(),
	lesson = lessonInfo)

@app.route('/adminContestAdd', methods = ['GET', 'POST'])
def adminContestAdd():
  if (not isAdmin(loginStatus())):
    return redirect('/home')
  if (request.method == 'POST'):
    print(r)
    r = {'name' : request.form['name'],
	'context': request.form['context'],
	'courseID' : courseID}
    print(r)
    addLesson(r)
    return redirect('/course/' + str(courseID)) 
  return render_template('adminContestAdd.html',
    userName = loginStatus())

@app.route('/contestProblemAdd/<contestID>', methods = ['GET', 'POST'])
def contestProblemAdd(contestID):
  if (not isAdmin(loginStatus())):
    return redirect('/home')
  if (request.method == 'POST'):
    r = {'problemID' : request.form['problemID'], 
	'contestID' : contestID,
	'newName' : request.form['newName']}
    addContestProblem(r)
    return redirect('/contest/' + contestID) 
  return render_template('contestProblemAdd.html',
    userName = loginStatus(),
    contestID = contestID)


@app.route('/codeSubmit', methods = ['GET', 'POST'])
def codeSubmit():
  if loginStatus() == None:
    return
  if (request.method == 'POST'):
    print(request.form)
    r = {'userName' : loginStatus(),
	'problemID' : request.form['problemID'],
	'contestID' : 1,
	'cProblemID' : 0,
	'status' : 0,
	'runTime' : 0,
	'memory' : 0,
	'language' : request.form['language'],
	'source' : request.form['source'],
	'pbStatus': 0}
    print(r)
    addSubmission(r)

@app.route('/courses')
@app.route('/courses/<pageNum>')
def courses(pageNum = None):
  bg = 0
  if (pageNum is None):
    bg = 0
  else:
    pageNum = int(pageNum)
    bg = pageNum * 16
  courses = courseGet((bg, bg + 16))
  messages = messageListGet((0, 15), loginStatus())
  return render_template('courses.html',
    page = "courses",
    userName = loginStatus(),
    courses = courses,
    messages = messages)

@app.route('/course/<courseID>')
def course(courseID):
  courseID = int(courseID)
  courseInfo = courseInfoGet(courseID)
  lessonList = lessonListGet(courseID)
  return render_template('course_overview.html',
    page = "courses",
    course = courseInfo,
    userName = loginStatus(),
    lessons = lessonList)

@app.route('/lesson/<lessonID>')
def lesson(lessonID):
  lessonID = int(lessonID)
  lessonInfo = lessonInfoGet(lessonID)
  return render_template('lesson.html',
    page = "courses",
    userName = loginStatus(),
    lesson = lessonInfo)

@app.route('/contests')
@app.route('/contests/<pageNum>')
def contests(pageNum = None):
  bg = 0
  if (pageNum is None):
    bg = 0
  else:
    pageNum = int(pageNum)
    bg = pageNum * 16
 
  contests = contestListGet((bg, bg+15))
  return render_template('contests.html',
    userName = loginStatus(),
    page = "contests",
    contests = contests)



@app.route('/contest/<contestID>')
@app.route('/contest/<contestID>/<problemID>')
def contest(contestID, problemID = None):
  contest = contestInfoGet(contestID)
  if (problemID is None):
    problems = contestProblemListGet(contestID)
    print(problems)
    return render_template('contest_overview.html',
      page = "contests",
      userName = loginStatus(),
      contest = contest,
      problems = problems)
  else:
    problem = contestProblemGet(contestID, problemID)
    return render_template('problem.html',
      page = "contests",
      userName = loginStatus(),
      contest = contest,
      problem = problem)

@app.route('/problems/<problemPage>')
@app.route('/problems/<problemPage>/problemID')
def problems(problemPage, problemID = None):
  if (problemPage is None):
    problemPage = "problemList"
  if (problemID == None):
    bg = 0
  else :
    bg = problemID * 100
  if (problemPage == "problemList") :
    problems = problemListGet((bg, bg + 100))
    return render_template('problems.html',
      problems = problems,
      page = "problems",
      problemsPage = "problemList",
      userName = loginStatus(),
      problemList = "True")
  elif (problemPage == "submissionList") :
    submissions = submissionListGet((0, 100), loginStatus(), None, None)
    return render_template('problems.html',
      submissions = submissions,
      page = "problems",
      problemsPage = "submissionList",
      userName = loginStatus(),
      problemList = "True")
  elif (problemPage == "rank") :
    rankList = problemRankGet((0, 100))
    return render_template('problems.html',
      rankList = rankList,
      page = "problems",
      problemsPage = "rank",
      userName = loginStatus(),
      problemList = "True")

@app.route('/problem/<problemID>')
@app.route('/problem/<problemID>/<problemPage>')
def problem(problemID, problemPage = None):
  problem = problemGet(problemID)
  if (problemPage == None):
    problemPage = "description"
  if (problemPage == "description" or problemPage == "hint"):
    return render_template('problem.html',
      page = "problems",
      problemPage = problemPage,
      problem = problem,
      userName = loginStatus(),
      problemList = "True")
  elif problemPage == "submission":
    submissions = submissionListGet((0, 100), loginStatus(), problemID, None)
    return render_template('problem.html',
      page = "problems",
      problemPage = problemPage,
      submissions = submissions,
      problem = problem,
      userName = loginStatus(),
      problemList = "True")
  elif problemPage == "solution":
    solutions = solutionListGet((0, 100), problemID)
    return render_template('problem.html',
      page = "problems",
      problemPage = problemPage,
      solutions = solutions,
      problem = problem,
      userName = loginStatus(),
      problemList = "True")

@app.route('/code/<submissionID>')
def code(submissionID):
   code = codeGet(submissionID, loginStatus())
   return render_template('code.html', userName = loginStatus(), code = code) 

@app.route('/login', methods = ['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    print(username, password)
    if (userLogin(username, password) == None):
      error = "username is not exists or password is error"
      session.permanent = False
    else:
      session.permanent = True
      session['username'] = request.form['username']
      g.user = request.form['username']
      return redirect('/home')
  return render_template('login.html',
    login = "TJOJ",
    error = error)

@app.route('/regist', methods = ['GET', 'POST'])
def regist():
  error = None
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    _password = request.form['_password']
    if (password != _password):
      error = "password is not match"
    elif (userRegist({'name':username, 'password':password}) == False):
      error = "username %s already exists" % username
    else:
      return redirect('/home')

  return render_template('regist.html',
    regist = "TJOJ",
    error = error)

@app.route('/info')
def info():
  return render_template('info.html',
    userName = loginStatus(),
    info = "TJOJ")

@app.route('/logout')
def logout():
  session.permanent = False
  return redirect('/home')
#  return render_template('logout.html',
#    logout = "TJOJ")
