import unittest
import unittest.mock as mock


from playhouse.test_utils import test_database
from datetime import datetime
from peewee import *

import work_log
from entry import Entry


test_db = SqliteDatabase(':memory:')
test_db.connect()
test_db.create_tables([Entry], safe=True)

TEST = {
    "employee_name": "Mason",
    "task_name": "Cleaning",
    "minutes": 40,
    "notes": "Some notes.",
    "date": "2012-12-12"
}

TEST2 = {
    "employee_name": "Carter",
    "task_name": "Mopping",
    "minutes": 30,
    "notes": "Some more notes",
    "date": "2018-10-12"
}

class LogTest(unittest.TestCase):

    @staticmethod
    def entry_creator():
        work_log.Entry.create(
            employee_name=TEST["employee_name"],
            task_name=TEST["task_name"],
            date=TEST["date"],
            minutes=TEST["minutes"],
            notes=TEST["notes"])

        work_log.Entry.create(
            employee_name=TEST2["employee_name"],
            task_name=TEST2["task_name"],
            date=TEST2["date"],
            minutes=TEST2["minutes"],
            notes=TEST2["notes"])
        
    def test_employees_name(self):
        with unittest.mock.patch('builtins.input', side_effect = ["", "", "alex"]):
            assert work_log.employees_name() == "alex"

    def test_time_spent(self):
        with unittest.mock.patch('builtins.input', side_effect = ["", "", 10]):
            assert work_log.time_spent() == 10

    def test_task_title(self):
        with unittest.mock.patch('builtins.input', side_effect = ["", "", "proj"]):
            assert work_log.task_title() == "proj"            

    def test_task_date(self):
        with unittest.mock.patch('builtins.input', side_effect = ["", "", "2018-12-12"]):
            assert work_log.task_date() == "2018-12-12"  
            
    def test_add_entry(self):
        with unittest.mock.patch('builtins.input',
            side_effect=["2012-12-12", "Name", "Cleaning", 45,
            "Very Clean", "y", ""]
            , return_value=TEST):
            assert work_log.add_entry()["task_name"] == TEST["task_name"]

        with unittest.mock.patch('builtins.input',
            side_effect=["2016-12-25", "Name", "Cleaning", 45,
            "Very Clean", "n", ""]
            , return_value=TEST):
            assert work_log.add_entry() == None
            

    def test_display_nav_menu(self):
        a = "A) Previous Entry"
        b = "B) Next Entry"
        e = "E) Return to Main Menu"

        with test_database(test_db, (Entry,)):
            self.entry_creator()
            entries = Entry.select()
            Entry.create(**TEST2)
            index = 0
            menu = [b, e]

            work_log.display_nav_menu(index, entries)
            self.assertNotIn(a, menu)
                       
    
    def test_search_menu(self):
        self.assertIsInstance(work_log.search_menu, dict)
        
    def test_main_menu(self):
        self.assertIsInstance(work_log.main_menu, dict)
    
    
    @unittest.mock.patch('work_log.search_entries', side_effect=['q', 'c'])
    def test_list_entries_calls_search_entries(self, mock):
        entries = []
        user_input = ''
        
        with unittest.mock.patch('builtins.input', side_effect=["n"]):
                        
            work_log.list_entries(entries, user_input)
            self.assertTrue(mock.called)
        
            

if __name__ == '__main__':
    unittest.main()
