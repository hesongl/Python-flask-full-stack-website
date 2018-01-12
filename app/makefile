judge.exe:database/MyDB.o judge.o
		g++ judge.o database/MyDB.o \
		-o judge.exe \
		-L/usr/bin/mysql -lmysqlclient \
		-L/usr/local/bin -lcrypto -g

database/MyDB.o:database/MyDB.cpp database/MyDB.h
	g++ database/MyDB.cpp -c -o database/MyDB.o -g 

judge.o:judge.cpp
	g++ judge.cpp -c -o judge.o -g

clean:
	rm judge.o judge.exe
