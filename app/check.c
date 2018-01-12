#include<stdio.h>

int main(int argv, char ** argc){
	FILE * fa = fopen(argc[1], "r");
	FILE * fb = fopen(argc[2], "r");
	char a, b;
	while (1) {
		int mark1 = fscanf(fa, "%c", &a);
		int mark2 = fscanf(fb, "%c", &b);
	//	printf("%d %d\n", mark1, mark2);
	//	printf("%c %c\n", a, b);
		if (mark1 != mark2) {
			puts("No");
			return 0;
		}
		if (mark1 == 0 || mark1 == -1) {
			puts("Yes");
			return 0;
		}	
		if (a != b) {
			puts("No");
			return 0;
		}
	}
	return 0;
}
