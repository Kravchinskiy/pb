import sqlite3

from datetime import datetime
from pb_const import *

#---------------------------------------------------------------------
# CLASS Persons for use person from PhoneBook
#---------------------------------------------------------------------
class Persons:

#---------------------------------------------------------------------
#   CONSTRUCTOR
#---------------------------------------------------------------------
    def __init__(self):
        self.__data = []
        try:
            self.__conn = sqlite3.connect('pb.sqlite')
            self.__curs = self.__conn.cursor()
            self.__refresh()
            self.__tabname = 'person_tab'
        except:
            print('DB Error')
            return None
        else:
            pass
        print(PB_VERSION + '\n')

#---------------------------------------------------------------------
#   REFRESH CACHE
#---------------------------------------------------------------------
    def __refresh(self):
        self.__curs.execute('SELECT * FROM person_tab')
        self.__data = self.__curs.fetchall()
        
#---------------------------------------------------------------------
#   GET PERSONS LIST
#---------------------------------------------------------------------
    def get_persons(self):
        return self.__data

#---------------------------------------------------------------------
#   SEARCH BY PATTERN
#---------------------------------------------------------------------
    def person_find(self, pattern):
        result = []
        for person in self.__data:
            for fld in person:
                if pattern.lower() in str(fld).lower():
                    result.append(person)
                    break
        return result


#---------------------------------------------------------------------
#   GET FIELD
#---------------------------------------------------------------------
    def get_field(self, label):
        return input(label)

#---------------------------------------------------------------------
#   PERSON ADD NEW RECORD
#---------------------------------------------------------------------
    def person_add_new(self, per_dict):
        if True: # Variant 1
            cols = ', '.join('"{}"'.format(col) for col in per_dict.keys())
            vals = ', '.join(':{}'.format(col) for col in per_dict.keys())
            sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(self.__tabname, cols, vals)
            print(sql)
        else: # Variant 2
            cols = ', '.join('{}'.format(col) for col in per_dict.keys())
            vals = ', '.join("'{}'".format(val) for val in per_dict.values())
            sql = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(self.__tabname, cols, vals)
            print(sql)
        try: # Variant 1
            self.__curs.execute(sql, per_dict)
            # self.__conn.commit()
        except sqlite3.DatabaseError as err:
            self.__conn.rollback()
            print('Insert error')
            person_id = 0 # error
        else:
            self.__conn.commit()
            print('Insert successful')
            person_id = self.__curs.lastrowid
            # print(data)
        return person_id

#---------------------------------------------------------------------
#   DELETE PERSON RECORD BY ID
#---------------------------------------------------------------------
    def person_delete(self, person_id):
        sql = 'DELETE FROM ' + self.__tabname + \
              ' WHERE person_id = ?'
        try:
            data = self.__conn.execute(sql, (person_id,))
        except sqlite3.DatabaseError as err:
            self.__conn.rollback()
            print('Delete error. Person id ' + str(person_id))
            result = False
        else:
            self.__conn.commit()
            self.__refresh()
            print('Delete successful. Person id ' + str(person_id))
            result = True
        return result

#---------------------------------------------------------------------
#   GET DETAIL PERSON RECORD BY ID
#---------------------------------------------------------------------
    def get_detail(self, person_id):
        sql = 'SELECT * FROM ' + self.__tabname + \
              ' WHERE person_id = ?'
        try:
            data = self.__conn.execute(sql, (person_id,))
        except sqlite3.DatabaseError as err:
            self.__conn.rollback()
            print('Select error. Person id ' + str(person_id))
            data = None
        else:
            self.__conn.commit()
            print('Select successful. Person id ' + str(person_id))
        return data

#---------------------------------------------------------------------
#   READ PERSON RECORD BY ID
#---------------------------------------------------------------------
    def read_person(self, person_id):
        for person in self.__data:
            if person[0] == person_id:
                return person
        return None

#---------------------------------------------------------------------
#   MODIFY PERSON RECORD BY ID
#---------------------------------------------------------------------
    def mod_person(self, person):
        # upd = False
        for idx, item in enumerate(self.__data):
            upd = (item[0] == person[0])
            if upd:
                self.__data = person
                break
        if not upd:
            self.__data.append(person)
        return upd # Sign insert=False or update=True

#---------------------------------------------------------------------
#   DESTRUCTOR
#---------------------------------------------------------------------
    def destructor(self):
        self.__conn.close()

