'''
Created on 5/12/2013

@author: johnefe
'''

import MySQLdb

class DataBase:
    def __init__(self, host, user, passwd, db_name):
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__db_name = db_name
    
    def connect(self):
        self.__db = MySQLdb.connect(host=self.__host, user=self.__user, 
            passwd=self.__passwd, db=self.__db_name)   

    def execute(self, command):
        cursor = self.__db.cursor()
        cursor.execute(command)
        return cursor;

    def commit(self):
        self.__db.commit()
        
    def rollback(self):
        self.__db.rollback()
    
    def close(self):
        self.__db.close()
        