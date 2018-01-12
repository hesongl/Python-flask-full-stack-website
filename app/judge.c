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
                wait(NULL);
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
                wait(NULL);
        } else {
                execv(cmd, argv);
        }
        return 0;
}


#define MLE 11
#define TLE 9
#define FLOATERR 8

const char * getRunErr(const int err){
        switch (err) {
                case MLE : return "MLE";
                case TLE : return "TLE";
                case FLOATERR: return "FLOATERR";
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
                printf("pid = %d\n",waitpid(pid, &status, 0));
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



int main(int argn, char ** argc){
	char * argcp[] = {"g++", "main.cpp", "-o", "main.exe", NULL};
	execp("/usr/bin/g++", argcp);

	int memlim = 1024 * 1024 * 32;
	int timelim = 1;

	char ifn[256];
	char ofn[256];
	char tfn[256];
	sprintf(ifn, "/home/freecss/data/%d/1.in", 1);
	sprintf(ofn, "/home/freecss/data/%d/1.out", 1);
	//sprintf(tfn, "/home/freecss/data/%d/1.tmp", 1);
	sprintf(tfn, "1.tmp");
	printf("%s %s\n", ifn, ofn);
	struct timeval bgTime;
	struct timeval edTime;
	gettimeofday(&bgTime, NULL);
	char * argr[] = {"main.exe", NULL};
	runp("./main.exe", argr, ifn, tfn, memlim, timelim + 1);
	gettimeofday(&edTime, NULL);
	printf("%d ms\n", (int)(1000 * (edTime.tv_sec - bgTime.tv_sec) + (edTime.tv_usec - bgTime.tv_usec)/ 1000));

        char buf[1024];
        char * argv[] = {"check", ofn, tfn, NULL};
        int pipe_fd = readFromC("./check", argv);

        int len = read(pipe_fd, buf, sizeof(buf));
	printf("%s\n", buf);
        close(pipe_fd);

	//char cmd[1024];
	//sprintf(cmd, "rm main.exe %s", tfn);
	//system(cmd);
	return 0;
}
