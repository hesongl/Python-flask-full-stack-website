DROP DATABASE IF EXISTS oj;

CREATE DATABASE oj;
use oj;

DROP TABLE IF EXISTS user;
create table user(
	name varchar(32) NOT NULL PRIMARY KEY,
	password varchar(40),
	rating int
);

DROP TABLE IF EXISTS blog;
create table blog(
        id int not null auto_increment primary key,
	title varchar(128),
	addr varchar(256),
	author varchar(32) NOT NULL,
	context text,
	dt datetime
);

DROP TABLE IF EXISTS course;
create table course(
	id int not null auto_increment primary key,
	name varchar(128),
	teacher varchar(32) NOT NULL,
	dsp varchar(256),
	bgdate datetime,
	eddate datetime,
	rddate datetime
);

DROP TABLE IF EXISTS student;
create table student(
	courseID int,
	studentName varchar(32),
	foreign key(courseID) references course(id),
	foreign key(studentName) references user(name)
);

DROP TABLE IF EXISTS tutor;
create table tutor(
	courseID int,
	tutorName varchar(32),
	foreign key(courseID) references course(id),
	foreign key(tutorName) references user(name)
);

DROP TABLE IF EXISTS lesson;
create table lesson(
	id int not null auto_increment primary key,
	name varchar(128),
	courseID int,
	context text,
	rddate datetime,
        foreign key(courseID) references course(id)
);

DROP TABLE IF EXISTS contest;
create table contest(
	id int not null auto_increment primary key,
	name varchar(128),
	creator varchar(32),
	judgeMethod int,
	length time,
	bgdate datetime,
	rddate datetime
);

DROP TABLE IF EXISTS problem;
create table problem(
	id int not null auto_increment primary key,
	name varchar(128),
	creator varchar(128),
	context text,
	input text,
	output text,
	hint text,
	addtion text,
	difficulty int,
	memlim int,
	timlim int,
	rddate datetime,
	status varchar(16),
	tag varchar(128),
	accpected int default 0,
	submission int default 0,
        foreign key(creator) references user(name)
);

DROP TABLE IF EXISTS contestProblem;
create table contestProblem(
	contestID int not null,
	problemID int not null,
	newName int,
	foreign key(contestID) references contest(id),
	foreign key(problemID) references problem(id)
);

DROP TABLE IF EXISTS submission;
create table submission(
	id int not null auto_increment primary key,
	submitTime datetime,
	userName varchar(32),
	problemID int,
	contestID int,
	cProblemID int,
	Status int,
	runtime int,
	Memory int,
	language varchar(32),
	source text,
	pbStatus int,
	foreign key(userName) references user(name)
);

DROP TABLE IF EXISTS chat;
create table chat(
	id int not null auto_increment primary key,
	userName varchar(32),
	contestID int,
	problemID int,
	cProblemID int,
	title varchar(128),
	context text,
	replyID int,
	status int default 0,
	chatDate datetime,
	foreign key(userName) references user(name),
	foreign key(problemID) references problem(id),
	foreign key(contestID) references contest(id)
);

DROP TABLE IF EXISTS message;
create table message(
	id int not null auto_increment primary key,
	source varchar(32),
	dest varchar(32),
	replyID int,
	context varchar(256),
	rddate datetime,
	foreign key(source) references user(name),
	foreign key(dest) references user(name)
);
