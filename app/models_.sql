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
	dt datetime,
        foreign key(author) references user(name)
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

exit;

insert into user(name, password) values("admin", "plxdcvsq");

insert into blog(title, addr, author, context, dt) values("主页简介", "/home", "admin", "主页用于展示一些公告信息，当然，这些公告信息主要由官方进行发布。", now());

insert into blog(title, addr, author, context, dt) values("课程简介", "/courses", "admin", "课程主要用来放置课程相关信息，主要作用为为学生提供有序的学习空间。", now());


insert into blog(title, addr, author, context, dt) values("比赛简介", "/contests", "admin", "比赛主要用来放置比赛信息，主要用来为学生提供竞技场所，同时也举办对外比赛。", now());


insert into blog(title, addr, author, context, dt) values("题目简介", "/problems", "admin", "题目主要用来放置大量题集，主要用来为学生提供差缺不漏的空间。", now());



insert into course(name, teacher, dsp, bgdate, eddate, rddate) 
	values("C语言程序设计", "znw", "大神带你C语言入门", "2017-04-26 08:00:00", "2017-05-31 08:00:00", now());

insert into course(name, teacher, dsp, bgdate, eddate, rddate) 
	values("CPP程序设计", "ztl", "大神带你快速入门CPP", "2017-05-01 08:00:00", "2018-01-31 08:00:00", now());

insert into course(name, teacher, dsp, bgdate, eddate, rddate) 
	values("python程序设计", "lxn", "机械大师带你玩转PYTHON", "2017-05-15 08:00:00", "2017-05-31 08:00:00", now());

insert into course(name, teacher, dsp, bgdate, eddate, rddate) 
	values("C#程序设计", "lhl", "美工带你玩转UI", "2030-04-26 08:00:00", "2030-05-31 08:00:00", now());


insert into lesson(name, courseID, context, rddate) 
	values("课程介绍", 1, "这是一门计算机专业的基础必修课，这节课将会为大家简要的介绍下这个课程的课时安排。", now());
insert into lesson(name, courseID, context, rddate) 
	values("输入输出和基本数据类型", 1, "这是一门计算机专业的基础必修课，这节课将会为大家简要的介绍下这个课程的课时安排。", now());
insert into lesson(name, courseID, context, rddate) 
	values("条件语句", 1, "这是一门计算机专业的基础必修课，这节课将会为大家简要的介绍下这个课程的课时安排。", now());


insert into lesson(name, courseID, context, rddate) 
	values("课程介绍", 2, "这是一门计算机专业的基础必修课，这节课将会为大家简要的介绍下这个课程的课时安排。", now());

insert into lesson(name, courseID, context, rddate) 
	values("课程介绍", 3, "这是一门计算机专业的基础必修课，这节课将会为大家简要的介绍下这个课程的课时安排。", now());

insert into lesson(name, courseID, context, rddate) 
	values("课程介绍", 4, "这是一门计算机专业的基础必修课，这节课将会为大家简要的介绍下这个课程的课时安排。", now());


insert into contest(name, creator, length, bgdate, rddate)
	values("测试00", "admin", "05:00:00", "2017-04-26 12:00:00", now());

insert into contest(name, creator, length, bgdate, rddate)
	values("再次测试", "admin", "05:00:00", "2017-04-26 12:00:00", now());

insert into contest(name, creator, length, bgdate, rddate)
	values("测试02", "admin", "05:00:00", "2017-04-26 12:00:00", now());


insert into problem(name, creator, context, memlim, timlim, rddate, status)
	values("a+b problem", "admin", "这是一道入门测试", 1024, 1024,  now(), "public");

insert into problem(name, creator, context, memlim, timlim, rddate, status)
	values("a+b problem", "admin", "这是一道入门测试", 1024, 1024,  now(), "private");


select * from user;
select * from blog;
select * from course;
select * from lesson;
select * from contest;
select * from problem;
