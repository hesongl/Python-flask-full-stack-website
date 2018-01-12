import pymysql
import hashlib
from config import MYSQLCONFIG
from flask import Markup
import markdown

def mark(con):
  contents = Markup(markdown.markdown(con))
  return contents

conn = pymysql.connect(
	host = MYSQLCONFIG['host'],
	port = MYSQLCONFIG['port'],
	user = MYSQLCONFIG['user'],
	#passwd = MYSQLCONFIG['password'],
        passwd = "Asong_89757",
	db = MYSQLCONFIG['db'],
	#charset = MYSQLCONFIG['charset'])
        charset = 'utf8mb4')

cursor = conn.cursor()

def get_sha1_value(src):
    mySha1 = hashlib.sha1()
    mySha1.update(src)
    mySha1_Digest = mySha1.hexdigest()
    return mySha1_Digest

def userRegist(r):
	name = r['name'].encode('utf-8')
	password = r['password'].encode('utf-8')
	effect_row = cursor.execute("select * from user where name = %s", (name))
	if (effect_row > 0):
		return False
	password = get_sha1_value(password)
	cursor.execute("insert into user(name, rating, password)values(%s, %s, %s)",
		(name, 1500, password))
	conn.commit()
	return True

def userLogin(name, password):
	name = name.encode('utf-8')
	password = password.encode('utf-8')
	password = get_sha1_value(password)
	effect_row = cursor.execute("select * from user where name = %s and  password = %s",(name, password))
	if (effect_row == 0):
		return None
	userName, psword, rating = cursor.fetchone()
	return {'name' : userName,
		'rating' : rating,}

def blogGet(r):
	if r[0] < 0:
		r[0] = 0
	if r[1] < r[0]:
		r[1] = r[0]
	effect_row = cursor.execute("select * from blog order by id desc limit %s, %s" , (r[0], r[1]))
	content = cursor.fetchall()
	res = []
	for id, title, addr, author, context, datetime in content:
		res.append({'id' : id,
				'title' : title, 
				'addr' : addr, 
				'author' : author, 
				'context' : mark(context), 
				'datetime' : datetime})
	return res

def addBlog(r):
	cursor.execute("insert into blog(title, addr, author, context, dt) values(%s, %s, %s, %s, now())", 
		(r['title'],
		r['addr'],
		r['author'],
		r['context']
		))
	conn.commit()

def courseGet(r = (0, 20)):
	if r[0] < 0:
		r[0] = 0
	if r[1] < r[0]:
		r[1] = r[0]
	effect_row = cursor.execute("select * from course order by id desc limit %s, %s" , (r[0], r[1]))
	content = cursor.fetchall()
	#print(content)
	res = []
	for id, name, teacher, dsp, bgtime, edtime, rdtime in content:
		res.append({'img' : "course/" + str(id) + "/img.jpg",
				'id' : id,
				'name' : name,
				'teacher' : teacher, 
				'dsp' : mark(dsp), 
				'bgtime' : bgtime,
				'edtime' : edtime,
				'rdtime' : rdtime})
	#print(res)
	return res

def addCourse(r):
	print("in addCourse")
	cursor.execute("insert into course(name, teacher, dsp, bgdate, eddate, rddate) values(%s, %s, %s, %s, %s, now())", 
		(r['name'],
		r['teacher'],
		r['dsp'],
		r['bgdate'],
		r['eddate']
		))
	ID = int(conn.insert_id())
	conn.commit()
	print("ok")
	print(ID)
	return ID

def courseInfoGet(courseID):
	effect_row = cursor.execute("select * from course where id = %s" , (courseID))
	id, name, teacher, dsp, bgtime, edtime, rdtime = cursor.fetchone()
	res = {'id' : id,
                                'name' : name,
                                'teacher' : teacher,
                                'dsp' : mark(dsp),
                                'bgtime' : bgtime,
                                'edtime' : edtime,
                                'rdtime' : rdtime}
	return res

def courseStudentListGet(courseID):
	effect_row = cursor.execute("select studentName from student where courseID = %s" , (courseID))
	return cursor.fetchall()

def addCourseTutor(r):
	cursor.execute("insert into tutor(courseID, tutorName) values(%s, %s)",
		(r['courseID'],
		r['tutor']
		))
	conn.commit()

def courseTutorListGet(courseID):
	effect_row = cursor.execute("select tutorName from tutor where courseID = %s" , (courseID))
	return cursor.fetchall()


def addCourseStudent(r):
	cursor.execute("insert into student(courseID, studentName) values(%s, %s)",
		(r['courseID'],
		r['student']
		))
	conn.commit()



def lessonListGet(courseID):
	effect_row = cursor.execute("select id, name, courseID, rddate from lesson where courseID = %s" , (courseID))
	res = []
	for id, name, courseID, rdtime in cursor.fetchall():
		res.append({'id' : id,
                              	'name' : name,
								'courseID' : courseID,
                                'rdtime' : rdtime})
	return res

def lessonInfoGet(lessonID):
	effect_row = cursor.execute("select * from lesson where id = %s" , (lessonID))
	id, name, courseID, context, rdtime = cursor.fetchone();
	courseInfo = courseInfoGet(int(courseID))
	res = {'id' : id,
		'name' : name,
		'courseID' : courseID,
		'course' : courseInfo['name'],
		'teacher' : courseInfo['teacher'],
		'context' : mark(context),
		'rdtime' : rdtime}
	return res

def lessonInfoGet2(lessonID):
	effect_row = cursor.execute("select * from lesson where id = %s" , (lessonID))
	id, name, courseID, context, rdtime = cursor.fetchone();
	courseInfo = courseInfoGet(int(courseID))
	res = {'id' : id,
		'name' : name,
		'courseID' : courseID,
		'course' : courseInfo['name'],
		'teacher' : courseInfo['teacher'],
		'context' : context,
		'rdtime' : rdtime}
	return res


def addLesson(r):
	cursor.execute("insert into lesson(name, courseID, context, rddate) values(%s, %s, %s, now())",
		(r['name'],
		r['courseID'],
		r['context']
		))
	conn.commit()

def updateLesson(r):
	cursor.execute("update lesson set name = %s, context = %s, rddate = now() where id = %s",
		(r['name'],
		r['context'],
		r['id']
		))
	conn.commit()



def contestListGet(r):
	if r[0] < 0:
		r[0] = 0
	if r[1] < r[0]:
		r[1] = r[0]
	effect_row = cursor.execute("select * from contest order by id desc limit %s, %s" , (r[0], r[1]))
	content = cursor.fetchall()
	res = []
	for id, name, creator, judgeMethod, length, bgdate, rddate in content:
		res.append({'id' : id, 
				'name' : name, 
				'creator' : creator, 
				'length' : length, 
				'judgeMethod' : 'Yes' if judgeMethod == 1 else 'No',
				'bgdate' : bgdate,
				'rddate' : rddate})
	return res

def addContest(r):
	cursor.execute("insert into contest(name, creator, length, judgeMethod, bgdate, rddate) values(%s, %s, %s, %s, %s, now())",
		(r['name'],
		r['creator'],
		r['length'],
		r['judgeMethod'],
		r['bgdate']
		))
	conn.commit()

def contestInfoGet(contestID):
	effect_row = cursor.execute("select * from contest where id = %s" , (contestID))
	content = cursor.fetchone()
	id, name, creator, judgeMethod, length, bgdate, rddate = content
	res = {'id' : id, 
		'name' : name, 
		'creator' : creator, 
		'length' : length, 
		'judgeMethod' : 'Yes' if judgeMethod == 1 else 'No',
		'bgdate' : bgdate,
		'rddate' : rddate}
	return res

def addcontestProblem(r):
	cursor.execute("insert into contestProblem(contestID, problemID, newName) values(%s, %s, %s)",
		(r['contestID'],
		r['problemID'],
		r['newName'],
		))
	conn.commit()

def contestProblemListGet(contestID):
	effect_row = cursor.execute("select \
id, name, newName, creator, context, input, output, hint, addtion, \
memlim, timlim, rddate, status, accpected, submission \
from contestProblem, problem where \
contestProblem.problemID = problem.id and contestProblem.contestID = %s", (contestID))
	content = cursor.fetchall()
	res = []
	for id, name, newName, creator, context, input, output, hint, addtion, memlim, timlim, rddate, status, accepted, submission in content:
		ratio = 1
		if (submission != 0):
			ratio = accepted / submission
		res.append({'id' : id, 
				'name' : name, 
				'creator' : creator, 
				'context' : context, 
				'input'	: input,
				'output' : output,
				'hint' : hint,
				'addtion' : addtion,
				'memlim' : memlim,
				'timlim' : timlim,
				'rddate' : rddate,
				'status' : status,
				'accepted' : accepted,
				'submission' : submission,
                                'pid': newName,
				'ratio' : ratio})
	return res

def contestProblemGet(contestID, problemID):
	effect_row = cursor.execute("select \
id, name, newName, creator, context, input, output, hint, addtion, \
memlim, timlim, rddate, status, accpected, submission \
from contestProblem, problem where \
contestProblem.problemID = problem.id and \
contestProblem.contestID = %s and contestProblem.problemID = %s", (contestID, problemID))
	content = cursor.fetchone()
	id, name, newName, creator, context, input, output, hint, addtion, memlim, timlim, rddate, status, accpected, submission = content
	ratio = 1
	if (submission != 0):
		ratio = accpected / submission
	res = {'id' : id, 
	'name' : name, 
	'creator' : creator, 
	'context' : context, 
	'input'	: input,
	'output' : output,
		'hint' : hint,
	'addtion' : addtion,
	'memlim' : memlim,
	'timlim' : timlim,
	'rddate' : rddate,
	'status' : status,
	'accepted' : accpected,
	'submission' : submission,
        'pid': newName,
	'ratio' : ratio}
	return res

def problemListGet(r):
	if r[0] < 0:
		r[0] = 0
	if r[1] < r[0]:
		r[1] = r[0]
	effect_row = cursor.execute("select id, name, difficulty, accpected, submission from problem order by id asc limit %s, %s" , (r[0], r[1]))
	content = cursor.fetchall()
	res = []
	for id, name, difficulty, accpected, submission in content:
		ratio = 1
		if (submission != 0):
			ratio = accpected / submission
		res.append({'id' : id, 
				'name' : name,
				'difficulty' : difficulty,
				'ratio' : ratio})
	return res

def addContestProblem(r):
	cursor.execute("insert into contestProblem(contestID, problemID, newName) values(%s, %s, %s)",
		(r['contestID'],
		r['problemID'],
		r['newName']
		))
	conn.commit()

def problemGet(problemID):
	problemID = int(problemID)
	effect_row = cursor.execute("select id, name, creator, context, input, output, hint, addtion, difficulty, memlim, timlim, rddate, status, accpected, submission from problem where id = %s" , problemID)
	content = cursor.fetchone()
	res = []
	id, name, creator, context, input, output, hint, addtion, difficulty, memlim, timlim, rddate, status, accepted, submission = content
	ratio = 1
	if (submission > 0):
		ratio = accepted / submission
	res={'id' : id, 
				'name' : name, 
				'creator' : creator, 
				'context' : context, 
				'input'	: input,
				'output' : output,
				'hint' : hint,
				'addtion' : addtion,
				'memlim' : memlim,
				'timlim' : timlim,
				'rddate' : rddate,
				'status' : status,
				'accepted' : accepted,
				'submission' : submission,
				'ratio' : ratio}
	return res

def addProblem(r):
	print(r)
	print(cursor.execute("insert into problem(name, creator, context, input, output, hint, addtion, memlim, timlim, status, rddate) \
		values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())",
		(r['name'],
		r['creator'],
		r['context'],
		r['input'],
		r['output'],
		r['hint'],
		r['addtion'],
		r['memlim'],
		r['timlim'],
		r['status']
		)))
	ID = int(conn.insert_id())
	conn.commit()
	return ID


def submissionListGet(r, userName, pID, cID):
	cconn = pymysql.connect(
        	host = MYSQLCONFIG['host'],
        	port = MYSQLCONFIG['port'],
        	user = MYSQLCONFIG['user'],
        	passwd = MYSQLCONFIG['password'],
        	db = MYSQLCONFIG['db'],
        	charset = MYSQLCONFIG['charset'])
	cursor = cconn.cursor()
	statusDic = {0 : 'Wating',
			1 : 'Compiling',
			2 : 'Runing',
			3 : 'Yes',
			4 : 'No',
			5 : 'CE',
			6 : 'RE'}
	colorDic = {0 : 'sky',
			1 : 'sky',
			2 : 'sky',
			3 : 'green',
			4 : 'red',
			5 : 'red',
			6 : 'red'}
	if r[0] < 0:
		r[0] = 0
	if r[1] < r[0]:
		r[1] = r[0]
	if (pID == None and cID == None):
		effect_row = cursor.execute("select * from submission where userName = %s order by submitTime desc limit %s, %s", (userName, r[0], r[1]))
	elif (pID != None):
		effect_row = cursor.execute("select * from submission where userName = %s and problemID = %s order by submitTime desc limit %s, %s", (userName, pID, r[0], r[1]))
	else:
		effect_row = cursor.execute("select * from submission where userName = %s and contestID = %s order by submitTime desc limit %s, %s", (userName, cID, r[0], r[1]))

	content = cursor.fetchall()
	res = []
	for id, submitTime, userName, problemID, contestID, cProblemID, status, runTime, memory, language, source, pbStatus in content:
		res.append({'id': id,
				'userName' : userName, 
				'problemID' : problemID, 
				'contestID' : contestID, 
				'cProblemID' : cProblemID, 
				'status' : statusDic[status],
				'runTime' : runTime,
				'memory' : memory,
				'language' : language,
				'source' : source,
				'pbStatus' : pbStatus,
				'submitTime' : submitTime,
				'color' : colorDic[status],
				})
	cconn.close()
	return res

def solutionListGet(r, pID):
	statusDic = {0 : 'Wating',
			1 : 'Compiling',
			2 : 'Runing',
			3 : 'Yes',
			4 : 'No'}
	colorDic = {0 : 'sky',
			1 : 'sky',
			2 : 'sky',
			3 : 'green',
			4 : 'red'}
	if r[0] < 0:
		r[0] = 0
	if r[1] < r[0]:
		r[1] = r[0]
	effect_row = cursor.execute("select * from submission where status = 3 and problemID = %s order by submitTime desc limit %s, %s", (pID, r[0], r[1]))

	content = cursor.fetchall()
	res = []
	for id, submitTime, userName, problemID, contestID, cProblemID, status, runTime, memory, language, source, pbStatus in content:
		res.append({'id': id,
				'userName' : userName, 
				'problemID' : problemID, 
				'contestID' : contestID, 
				'cProblemID' : cProblemID, 
				'status' : statusDic[status],
				'runTime' : runTime,
				'memory' : memory,
				'language' : language,
				'source' : source,
				'pbStatus' : pbStatus,
				'submitTime' : submitTime,
				'color' : colorDic[status],
				})
	return res

def codeGet(submissionID, userName):
	effect_row = cursor.execute("select userName, problemID, runTime, memory, language, source, submitTime \
from submission where id = %s and (userName = %s or pbStatus = 0)", (submissionID, userName))
	content = cursor.fetchone()
	userName, problemID, runTime, memory, language, source, submitTime = content
	res = {'userName' : userName, 
		'problemID' : problemID, 
		'runTime' : runTime, 
		'memory' : memory, 
		'language': language,
		'source' : source,
		'submitTime': submitTime}
	return res

def problemRankGet(r):
	cconn = pymysql.connect(
        	host = MYSQLCONFIG['host'],
        	port = MYSQLCONFIG['port'],
        	user = MYSQLCONFIG['user'],
        	passwd = MYSQLCONFIG['password'],
        	db = MYSQLCONFIG['db'],
        	charset = MYSQLCONFIG['charset'])
	cursor = cconn.cursor()
	
	if r[0] < 0:
		r[0] = 0
	if r[1] < r[0]:
		r[1] = r[0]

	effect_row = cursor.execute("select userName, count(distinct problemID) as pNum from submission \
where status = 3 group by userName order by count(distinct problemID) desc limit %s, %s", (r[0], r[1]))
	content = cursor.fetchall()
	res = []
	rank = 1
	for userName, pNum in content:
		res.append({'userName' : userName,
			'pNum' : pNum,
			'rank' : rank})
		rank = rank + 1
	cconn.close()
	return res;

def addSubmission(r):
	cursor.execute("update problem set submission = submission + 1 where id = %s", (r['problemID']))
	cursor.execute("insert into submission\
(userName, problemID, contestID, cProblemID, status, runTime, Memory, language, source, pbStatus, submitTime) \
		values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())",
		(r['userName'],
		r['problemID'],
		r['contestID'],
		r['cProblemID'],
		r['status'],
		r['runTime'],
		r['memory'],
		r['language'],
		r['source'],
		r['pbStatus']
		))
	conn.commit()
	

def chatListGet(r, userName, pID, cID):
	if r[0] < 0:
		r[0] = 0
	if r[1] < r[0]:
		r[1] = r[0]
	if (pID == None and cID == None):
		effect_row = cursor.execute("select * from chat where userName = %s \
			order by chatDate desc limit %s, %s", (userName, r[0], r[1]))
	elif (pID != None):
		effect_row = cursor.execute("select * from chat where userName = %s and problemID = %s \
			order by chatDate desc limit %s, %s", (userName, pID, r[0], r[1]))
	else:
		effect_row = cursor.execute("select * from chat where userName = %s and contestID = %s \
			order by chatDate desc limit %s, %s" , (userName, cID, r[0], r[1]))

	content = cursor.fetchall()
	res = []
	for id, userName, problemID, contestID, cProblemID, context, replyID, status in content:
		res.append({'userName' : userName, 
				'problemID' : problemID, 
				'contestID' : contestID, 
				'cProblemID' : cProblemID, 
				'context' : context,
				'replyID' : replyID,
				'status' : status,
				})
	return res
	
def addChat(r):
	cursor.execute("insert into chat(userName, contestID, problemID, cProblemID, title, context, replyID, chatDate) \
		values(%s, %s, %s, %s, %s, %s, %s, now())",
		(r['userName'],
		r['contestID'],
		r['problemID'],
		r['title'],
		r['context'],
		r['replyID'],
		r['status']
		))
	conn.commit() 

def messageListGet(r, userName):
	if r[0] < 0:
		r[0] = 0
	if r[1] < r[0]:
		r[1] = r[0]
	effect_row = cursor.execute("select source, context, rddate from message where dest = %s \
			order by rddate desc limit %s, %s", (userName, r[0], r[1]))
	
	content = cursor.fetchall()
	res = []
	for source, context, rddate in content:
		res.append({'source' : source,
				'context' : context, 
				'rddate' : rddate
				})
	return res
	
	
def addMessage(r):
	cursor.execute("insert into message(source, dest, replyID, context, rddate) \
		values(%s, %s, %s, %s, now())",
		(r['source'],
		r['dest'],
		r['replyID'],
		r['context']
		))
	conn.commit()

def utf8S(str):
	return str.encode('utf-8')


def deleteBlog(ID):
	cursor.execute("delete from blog where id = %s", (ID))
	conn.commit()

def deleteCourse(ID):
	cursor.execute("delete from course where id = %s", (ID))
	conn.commit()

def deleteLesson(ID):
	cursor.execute("delete from lesson where id = %s", (ID))
	conn.commit()

def deleteProblem(id):
	#delstatmt = "DELETE FROM `problem` WHERE id = ?"
	#cursor.execute(delstatmt, (id))
	cursor.execute("SET foreign_key_checks = 0")
	cursor.execute("delete from problem where id = %s", (id))		
	cursor.execute("SET foreign_key_checks = 1")
	conn.commit()

def userTest():
	r1 = {'name' : 'hesongl', 'password' : 'abc123'};
	r2 = {'name' : 'admin', 'password' : 'tjojadmin'};
	print('userRegist : ', userRegist(r1))
	print('userRegist : ', userRegist(r2))
	print('userLogin : ', userLogin(r1['name'], r1['password']))
	print('userLogin : ', userLogin(r2['name'], r2['password']))
	print('userLogin : ', userLogin(r1['name'], 'abc321'))

def blogTest():
	r1 = {'title' : 'Summary of the mainpage',
		'addr' : '/home', 
		'author' : 'admin', 
		'context' : 'Mainpage is used for announcing some official news.'}
	addBlog(r1)
	print('blog : ', blogGet((0, 20)))


def courseTest():
	r1 = {'name' : 'Engineering Computation',
		'teacher' : 'Yamakawa Soji',
		'dsp' : 'C++ course for Mechanical Students',
		'bgdate' : '2017-04-26 08:00:00',
		'eddate' : '2017-05-31 08:00:00'}
	addCourse(r1)
	print('courseInfo : ', courseInfoGet(1))
	print('course : ', courseGet())

def lessonTest():
	r1 = {'name' : "Course Introduction",
		'courseID' : 1,
		'context' : "A CS course for non-cs students."}
	addLesson(r1)
	print('lessonList : ', lessonListGet(1))
	print('lessonInfo : ', lessonInfoGet(1))

def contestTest():
	r1 = {'name' : "test00",
		'creator' : "admin",
		'length' : "05:00:00",
		'bgdate' : "2017-04-26 12:00:00",
		'judgeMethod' : 0
		}
	r1 = {'name' : "test01",
		'creator' : "admin",
		'length' : "04:00:00",
		'bgdate' : "2017-04-27 12:00:00",
		'judgeMethod' : 1
		}
	addContest(r1)
	print('contestList :', contestListGet((0, 20)))
	print('contestInfo :', contestInfoGet(1))

def problemTest():
	r1 = {'name' : 'a+b problem',
		'creator' : 'admin',
		'context' : 'give you two number a, b, please output the sum of a and b.',
		'input' : '2 3',
		'output' : '5',
		'hint' : '2 + 3 = 5',
		'addtion' : '',
		'memlim' : 65536,
		'timlim' : 1000,
		'status' : 'close'
	}
	addProblem(r1)
	print('problemList : ', problemListGet((0, 20)))
	print('problem : ', problemGet(1))

def submissionTest():
	r1 = {'userName' : 'hesongl',
		'problemID' : 1,
		'contestID' : 1,
		'cProblemID' : 0,
		'status' : 0,
		'runTime' : 30,
		'memory' : 2345,
		'language' : 'C++',
		'source' : "int main() {return 0;}",
		'pbStatus' : 0}
	r2 = {'userName' : 'admin',
		'problemID' : 1,
		'contestID' : 1,
		'cProblemID' : 0,
		'status' : 0,
		'runTime' : 300,
		'memory' : 5345,
		'language' : 'java',
		'source' : "int main() {return 0;}",
		'pbStatus' : 0}
	r3 = {'userName' : 'admin',
		'problemID' : 1,
		'contestID' : 1,
		'cProblemID' : 0,
		'status' : 3,
		'runTime' : 300,
		'memory' : 5345,
		'language' : 'java',
		'source' : "int main() {return 0;}",
		'pbStatus' : 0}
	r4 = {'userName' : 'hesongl',
		'problemID' : 2,
		'contestID' : 1,
		'cProblemID' : 0,
		'status' : 3,
		'runTime' : 30,
		'memory' : 2345,
		'language' : 'C++',
		'source' : "int main() {return 0;}",
		'pbStatus' : 0}
	r5 = {'userName' : 'hesongl',
		'problemID' : 1,
		'contestID' : 1,
		'cProblemID' : 0,
		'status' : 4,
		'runTime' : 30,
		'memory' : 2345,
		'language' : 'C++',
		'source' : "int main() {return 0;}",
		'pbStatus' : 0}
	addSubmission(r1)
	addSubmission(r2)
	addSubmission(r3)
	addSubmission(r4)
	addSubmission(r5)
	print(submissionListGet((0, 10), 'admin', None, None))

def contestProblemTest():
	r1 = {'contestID' : 1,
		'problemID' : 1,
		'newName' : 1}
	r2 = {'contestID' : 1,
		'problemID' : 2,
		'newName' : 2}
	r3 = {'contestID' : 2,
		'problemID' : 1,
		'newName' : 1}
	r4 = {'contestID' : 2,
		'problemID' : 2,
		'newName' : 2}
	addcontestProblem(r1)
	addcontestProblem(r2)
	addcontestProblem(r3)
	addcontestProblem(r4)
	print('contestProblemList 1: ' , contestProblemListGet(1))
	print('contestProblemList 2: ' , contestProblemListGet(2))
	print('contestProbelm: ', contestProblemGet(1, 1))
	print('contestProbelm: ', contestProblemGet(1, 2))

def tutorTest():
	r1 = {'courseID': 1,
		'tutor' : 'hesongl'}
	r2 = {'courseID' : 1,
		'tutor' : 'admin'}
	addCourseTutor(r1);
	addCourseTutor(r2);
	print('tutor : ', courseTutorListGet(1))	

def studentTest():
	r1 = {'courseID': 1,
		'student' : 'hesongl'}
	r2 = {'courseID' : 1,
		'student' : 'admin'}
	addCourseStudent(r1);
	addCourseStudent(r2);
	print('student : ', courseStudentListGet(1))	

def messageTest():
	r1 = {'source' : 'admin',
		'dest' : 'hesongl',
		'replyID' : 0,
		'context' : 'welcome to my demo OJ'}
	addMessage(r1)
	print('Message : ', messageListGet((0, 10), r1['dest']))

def test():
	userTest()
	blogTest()
	courseTest()
	lessonTest()
	contestTest()
	problemTest()
	submissionTest()
	contestProblemTest()
	tutorTest()
	studentTest()
	messageTest()
#	print(blogGet([0, 20]))
#	print(courseGet([0, 20]))
#	print(courseInfoGet(1))
#	print(courseInfoGet(2))
#	print(lessonListGet(1))
#	print(lessonListGet(2))
#	print(lessonInfoGet(1))
#	print(contestListGet())
#	print(problemListGet((0, 100)))
#	print(problemGet(1))

if __name__ == '__main__' :
	test()
