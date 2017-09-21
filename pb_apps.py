import os
import persons as prsn

from datetime import datetime
from pb_const import *


#---------------------------------------------------------------------
#   CLASS PB_Application (PhoneBook Application)
#---------------------------------------------------------------------
class PB_Application:

#---------------------------------------------------------------------
#   CONSTRUCTOR
#---------------------------------------------------------------------
    def __init__(self):
        self.__persons = prsn.Persons()
        self.__meth = { CMD_EXIT:           'exit',
                        CMD_PERSON_LIST:    'show_all_persons',
                        CMD_PERSON_FIND:    'person_find',
                        CMD_PERSON_ADD_NEW: 'person_add_new',
                        CMD_PERSON_DELETE:  'person_delete',
                        CMD_PERSON_CHANGE:  'person_change',
                        CMD_PERSON_DETAIL:  'person_detail'
                      }
        self.__cmd = CMD_PERSON_LIST

#---------------------------------------------------------------------
#   CLEAR SCREEN
#---------------------------------------------------------------------
    def __cls(self):
        if os.name == 'nt':             # check operation system
            os.system('cls')            # command for windows
        else:
            os.system('clear')          # command for others
            
#---------------------------------------------------------------------
#   RUN APPLICATION
#---------------------------------------------------------------------
    def run(self, mode=1):
        if mode == 1:
            cmd = self.show_all_persons()
        else:
            cmd = CMD_UNKNOWN
        while cmd != CMD_EXIT:
            self.show_menu()
            cmd = self.dispatch()
        
#---------------------------------------------------------------------
#   SHOW MENU
#---------------------------------------------------------------------
    def show_menu(self):
        self.__cls()
        print('\t1.Список записей телефонной книги')
        print('\t2.Поиск записи')
        print('\t3.Новая запись')
        print('\t4.Удалить запись')
        print('\t5.Изменить запись')
        print('\t6.Подробная информация')
        print('\t0.Выход')
    
#---------------------------------------------------------------------
#   DISPATCH USER COMMANDS
#---------------------------------------------------------------------
    def dispatch(self):
        self.__cmd = input('Your Command> ')
        if self.__cmd in self.__meth.keys():
            meth_name = self.__meth[self.__cmd]
            __method = getattr(self, meth_name)
            return __method()
        else:
            print('Unkown Command')
            return None

#---------------------------------------------------------------------
#   WAITING USER
#---------------------------------------------------------------------
    def __wait(self):
        s = input(LBL_CONTINUE)

#---------------------------------------------------------------------
#   SECONDS TO DATE
#---------------------------------------------------------------------
    def conv_date(self, ms):
        sec = ( ms / 1000 ) * -1
        dt = datetime.fromtimestamp(sec)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

#---------------------------------------------------------------------
#   SHOW PERSON
#---------------------------------------------------------------------
    def show_person(self, person):
        print(LBL_USER_ID + str(person[0]))
        print(LBL_LAST_NAME + person[1])
        print(LBL_FIRST_NAME + person[2])
        print(LBL_MIDDLE_NAME + person[3])
        print(LBL_ALIAS + person[4])
        print(LBL_BIRTHDAY + self.conv_date(person[5]))
        print('')
        
#---------------------------------------------------------------------
#   SHOW PERSONS LIST
#---------------------------------------------------------------------
    def show_persons(self, persons):
        self.__cls()
        for person in persons:
            self.show_person(person)
        self.__wait()
        return self.__cmd

#---------------------------------------------------------------------
#   SHOW ALL PERSONS LIST
#---------------------------------------------------------------------
    def show_all_persons(self):
        cmd = self.show_persons(self.__persons.get_persons())
        return cmd
    
#---------------------------------------------------------------------
#   EXIT FROM APPLICATION
#---------------------------------------------------------------------
    def exit(self):
        self.__persons.destructor()
        self.__wait()
        self.__cls()
        return self.__cmd

#---------------------------------------------------------------------
#   FIND PERSON BY PATTERN
#---------------------------------------------------------------------
    def person_find(self):
        pattern = input(LBL_PATTERN)
        persons = self.__persons.person_find(pattern)
        self.show_persons(persons)
        return self.__cmd

#---------------------------------------------------------------------
#   ADD NEW PERSON RECORD
#---------------------------------------------------------------------
    def person_add_new(self):
        person = {}
        last_name = { FLD_LAST_NAME: self.__persons.get_field(LBL_LAST_NAME) }
        person.update(last_name)
        first_name = { FLD_FIRST_NAME: self.__persons.get_field(LBL_FIRST_NAME) }
        person.update(first_name)
        middle_name = { FLD_MIDDLE_NAME: self.__persons.get_field(LBL_MIDDLE_NAME) }
        person.update(middle_name)
        alias = { FLD_ALIAS: self.__persons.get_field(LBL_ALIAS) }
        person.update(alias)
        birthday = { FLD_BIRTHDAY: int(self.__persons.get_field(LBL_BIRTHDAY)) }
        person.update(birthday)
        person_id = self.__persons.person_add_new(person)
        if person_id != 0: # upd cache
            item = []
            item.append(person_id)
            item.append(person[FLD_LAST_NAME])
            item.append(person[FLD_FIRST_NAME])
            item.append(person[FLD_MIDDLE_NAME])
            item.append(person[FLD_ALIAS])
            item.append(person[FLD_BIRTHDAY])
            self.__data.append(item)
        self.__wait()
        self.__cls()
        return self.__cmd

#---------------------------------------------------------------------
#   DELETE PERSON RECORD BY ID
#---------------------------------------------------------------------
    def person_delete(self):
        self.__cls()
        print('Delete person record')
        s = input('Input person id > ')
        if s != '' and s.isdigit():
            person_id = int(s)
            result = self.__persons.person_delete(person_id)
        else:
            print('Invalid person id')
        self.__wait()
        self.__cls()
        return self.__cmd

#---------------------------------------------------------------------
#   DETAIL PERSON RECORD BY ID
#---------------------------------------------------------------------
    def person_detail(self):
        print('Detail person record')
        s = input('Input person id > ')
        person_id = int(s)
        person = self.__persons.read_person(person_id)
        if person != None:
            self.show_person(person)
        self.__wait()
        self.__cls()
        return self.__cmd

#---------------------------------------------------------------------
#   CHANGE PERSON RECORD BY ID
#---------------------------------------------------------------------
    def person_change(self):
        print('Change person record')
        s = input('Input person id > ')
        self.__wait()
        self.__cls()
        return self.__cmd

