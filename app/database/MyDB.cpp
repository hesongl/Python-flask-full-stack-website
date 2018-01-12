#include "MyDB.h"
using namespace std;

MyDB::MyDB(){
	connection = mysql_init(NULL); // 
	if(connection == NULL){
		cout << "Error:" << mysql_error(connection);
		exit(1);
	}
}

MyDB::~MyDB(){
	if(connection != NULL) { //
		mysql_close(connection);
	}
}

bool MyDB::initDB(string host, string user, string pwd, string db_name)
{
	connection = mysql_real_connect(connection, host.c_str(),
			user.c_str(), pwd.c_str(), db_name.c_str(), 0, NULL, 0);
	mysql_set_character_set(connection, "utf-8");
	if(connection == NULL) {
		cout << "Error:" << mysql_error(connection);
		return false;
	}
	return true;
}

#define DEBUG() pritnf("[%s:%d]\n", __FILE__, __LINE__)

bool MyDB::exeSQL(string sql, vector<string> &res){
	if(mysql_query(connection, sql.c_str())) {
		return false;
	} else {
		result = mysql_store_result(connection); 
        if (result == NULL) return true;
        res.clear();
		int fieldcount = mysql_num_fields(result);
		while (row = mysql_fetch_row(result)){
			for(int j=0; j < fieldcount; ++j) {
				if (row[j] != NULL) {
					res.push_back(row[j]);
				} else {
					res.push_back("NULL");
				}
			}
		}
		mysql_free_result(result);
	}
	return true;
}

