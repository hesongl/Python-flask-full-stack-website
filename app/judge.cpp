#include "database/MyDB.h"
#include <iostream>
#include <utility>
#include <string>
#include <sstream>

int strToNum(std::string s){
	std::stringstream sbuf;
	int res;
	sbuf << s;
	sbuf >> res;
	return res;
}

template<class T>
std::string toStr(T t){
	std::stringstream sbuf;
	sbuf << t;
	std::string res;
	sbuf >> res;
	return res;
}

class DBoperator{
private:
	MyDB db;
public:
	DBoperator();
	void debugOut(std::string s);
	std::vector<int> getWatingID();
	std::pair<std::pair<int, std::string>, std::string> readCode(const int ID);
	int setSubmissionStatus(const int ID, const int status, const int runTime);
};

DBoperator::DBoperator(){
	db.initDB("localhost", "root", "Asong_89757", "oj");
}

void DBoperator::debugOut(std::string s){
	std::cout << s << std::endl;
}

std::vector<int> DBoperator::getWatingID(){
	std::vector<std::string> SQL_ans;
	std::vector<int> res;
	std::string command;
	//command = "SELECT id FROM submission";// where status = 0";
	command = "SELECT id FROM submission where status = 0";
	if (db.exeSQL(command, SQL_ans)) {
		for (int i = 0; i < SQL_ans.size(); ++i) {
			res.push_back(strToNum(SQL_ans[i]));
		}
	}
	return res;
}

std::pair<std::pair<int, std::string>, std::string> DBoperator::readCode(const int ID){
	std::vector<std::string> SQL_ans;
	std::vector<int> res;
	std::string command;
	command = std::string("SELECT problemID, language, source FROM submission where id = ") +
		"\"" + toStr(ID) + "\"";
	if (db.exeSQL(command, SQL_ans)) {
		return std::make_pair(std::make_pair(strToNum(SQL_ans[0]), SQL_ans[1]), SQL_ans[2]);
	}
	return std::make_pair(std::make_pair(0, ""), "");
}

int DBoperator::setSubmissionStatus(const int ID, const int status, const int runTime){
	std::vector<std::string> SQL_ans;
	std::vector<int> res;
	std::string command;
	command = std::string("UPDATE submission SET status = ") +
		"\"" + toStr(status) + "\", runtime = " + 
		"\"" + toStr(runTime) + "\"" + " where id = " +
		"\"" + toStr(ID) + "\"";
	debugOut(command);
	return db.exeSQL(command, SQL_ans);
}

using namespace std;

#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/resource.h>

void sys_err(const char * str){
        perror(str);
        exit(1);
}

#define PIPE_ERROE -1
#define FORK_ERROR -2

int readFromC(const char * cmd, char * const argv[]){
        pid_t pid;
        int fd[2];
        if (pipe(fd) == -1)
                return PIPE_ERROE;

        pid = fork();
        if (pid < 0) {
                return FORK_ERROR;
        } else if (pid != 0) {
		int status;
                waitpid(pid, &status, 0);
                close(fd[1]);
        } else {
                close(fd[0]);
                dup2(fd[1], 1);
                execv(cmd, argv);
                close(fd[1]);
        }
        return fd[0];
}


int execp(const char * cmd, char * const argv[]){
        pid_t pid;
        pid = fork();
        if (pid < 0) {
                return FORK_ERROR;
        } else if (pid != 0) {
		int status;
                waitpid(-1, &status, 0);
        } else {
                execv(cmd, argv);
        }
        return 0;
}


#define MLE 11
#define TLE 9
#define FLOATERR 8

int pRunErr = 0;

const char * getRunErr(const int err){
	pRunErr = 0;
        switch (err) {
                case MLE : pRunErr = 6;
			return "MLE";
                case TLE : 
			   pRunErr = 6;
			return "TLE";
                case FLOATERR: pRunErr = 6;
			return "FLOATERR";
        }
        return "";
}

int runp(const char * cmd, char * const argv[],
        const char * inFile, const char * outFile,
        const int maxMem, const int maxTime){
 
        pid_t pid;
        pid = fork();
        if (pid < 0) {
                return FORK_ERROR;
        } else if (pid != 0) {
		int status;
                printf("pid = %d\n",waitpid(-1, &status, 0));
		printf("%d\n", WIFEXITED(status));
                printf("%d\n", WIFSIGNALED(status));
                printf("%s\n", getRunErr(WTERMSIG(status)));

        } else {
		int ifd = open(inFile, O_RDONLY);
		int ofd = open(outFile, O_WRONLY | O_CREAT, S_IRWXU);
		dup2(ifd, 0);
		dup2(ofd, 1);

		struct rlimit memLim, timeLim, procLim, fileLim;
		memLim.rlim_cur = maxMem;
		memLim.rlim_max = maxMem;
		timeLim.rlim_cur = maxTime;
		timeLim.rlim_max = maxTime;
		
		procLim.rlim_cur = 1;
		procLim.rlim_max = 1;

		fileLim.rlim_cur = 10;
		fileLim.rlim_max = 10;

		setrlimit(RLIMIT_AS, &memLim);
		setrlimit(RLIMIT_CPU, &timeLim);
		setrlimit(RLIMIT_NPROC, &procLim);
		setrlimit(RLIMIT_NOFILE, &fileLim);

		execv(cmd, argv);
		close(ifd);
		close(ofd);
        }
	return 0;
}



int judge(int ID, int & runTime){
	char * argcp[] = {"g++", "main.cpp", "-o", "main.exe", NULL};
	execp("/usr/bin/g++", argcp);
	if (access("main.exe", F_OK) == -1) return 5;
	
	int memlim = 1024 * 1024 * 32;
	int timelim = 1;

	char ifn[256];
	char ofn[256];
	char tfn[256];
	sprintf(ifn, "/home/hesongl/12780/flask/data/%d/1.in", ID);
	sprintf(ofn, "/home/hesongl/12780/flask/data/%d/1.out", ID);
	//sprintf(tfn, "/home/freecss/data/%d/1.tmp", 1);
	sprintf(tfn, "1.tmp");
	printf("%s %s\n", ifn, ofn);
	struct timeval bgTime;
	struct timeval edTime;
	gettimeofday(&bgTime, NULL);
	char * argr[] = {"main.exe", NULL};
	runp("./main.exe", argr, ifn, tfn, memlim, timelim + 1);
	gettimeofday(&edTime, NULL);
	runTime = (int)(1000 * (edTime.tv_sec - bgTime.tv_sec) 
		+ (edTime.tv_usec - bgTime.tv_usec)/ 1000);
        char buf[1024];
	buf[0] = 0;
        char * argv[] = {"check", ofn, tfn, NULL};
        int pipe_fd = readFromC("./check", argv);
        int len = read(pipe_fd, buf, sizeof(buf));
	if (len == 0) return 4;
	buf[len-1] = 0;
	int flag = 4;
	if (strcmp(buf, "Yes") == 0) flag = 3;
	printf("%s %s %d\n", buf, "Yes", flag);
	printf("%s\n", buf);
        close(pipe_fd);

	char cmd[1024];
	sprintf(cmd, "rm main.exe %s", tfn);
	system(cmd);
	return flag;
}

int main(){
	DBoperator test;
while(1){
	std::vector<int> IDs = test.getWatingID();
	std::cout << IDs.size() << std::endl;
	for (int i = 0; i < IDs.size(); ++i) {
		std::pair<std::pair<int, std::string>, std::string> code = test.readCode(IDs[i]);
		ofstream sf("main.cpp");
			sf << code.second << endl;
		sf.close();
		int runTime = 0;
		int res = judge(code.first.first, runTime);
		if (pRunErr) res = 6;
		std::cout << "ID: " << IDs[i] << " language: " << code.first.second << std::endl;
		std::cout << code.second << std::endl;
		test.setSubmissionStatus(IDs[i], res, runTime);
	}
	sleep(1);
}
	return 0;
}
