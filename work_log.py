from entry import Entry, initialize


from datetime import datetime
from collections import OrderedDict
import sys
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

    
def employees_name():
    while True:
        employee_name = input("Enter the employees name: ")
        if len(employee_name) == 0:
            print("Invalid, please enter your name")
            continue
        else:
            return employee_name

        
def task_title():
    while True:
        task_name = input("Enter the name of the task: ")
        if len(task_name) == 0:
            print("Invalid, please enter a task")
            continue
        else:
            return task_name

        
def time_spent():
    while True:
        minutes = input("Enter the amount of time spent in minutes: ")
        try:
            int(minutes)
        except ValueError:
            print("\nInvalid, please enter the time spent: ")
            continue
        else:
            return minutes

        
def task_notes():
    notes = input("Enter any notes for this task (Click enter to leave blank): ")
    return notes


def task_date():
    while True:
        date = input("Enter the date of the task in YYYY-MM-DD Format: ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("That is not a valid date, please check the format and try again ")
            continue
        else:
            return date
        

def entry_preview(entry):
    clear()
    print("""
Date: {date}
Employee Name: {employee_name}
Task Name: {task_name}
Minutes: {minutes}
Notes: {notes}
""".format(**entry))
    
    
def create_entry(entry):
    Entry.create(**entry)
    return entry


def get_user_entry():
    clear()
    date = string_to_datetime(task_date())
    employee_name = employees_name()
    task_name = task_title()
    minutes = time_spent()
    notes = task_notes()    
    
    entry = {
        "employee_name": employee_name,
        "date": date,
        "task_name": task_name,
        "minutes": minutes,
        "notes": notes
    }
    
    entry_preview(entry)
    
    while True:
        save = input("\nSave Entry? [Y/N] ").lower().strip()
        if save == 'y':
            input("The entry has been saved. Press ENTER to continue.")
            return entry
        else: 
            input("The entry was not saved. Press ENTER to continue")
            return None
        

def add_entry():
    """Add a work entry to the database."""
    entry = get_user_entry()
    if entry:
        return create_entry(entry)
    

def select_entries():
    entries = Entry.select().order_by(Entry.date.desc())
    return entries


def find_employee():
    """Search by an employee's name"""
    clear()
    print("Search by employees name\n")
    user_input = employees_name()
    entries = select_entries()
    entries = entries.where(Entry.employee_name.contains(user_input))
    entries = check_employee_matches(entries)
    list_entries(entries, user_input)
    return entries


def check_employee_matches(entries):
    names = []
    for entry in entries:
        name = entry.employee_name.strip()
        if name not in names:
            names.append(name)
        if len(names) > 1:
            while True:
                clear()
                print("These employees match your search: ")
                for name in names:
                    print(name)
                employee_name = input("\nWhich employee would you like to search?").strip()
                if employee_name in names:
                    entries = Entry.select().order_by(Entry.date.desc()).where(
                        Entry.employee_name == employee_name)
                    return entries
                else:
                    print("\n {} is not an employees name that is displayed above.\n"
                          "".format(employee_name))
                    input("Press ENTER to try again")
        return entries
    

def find_by_date():
    """Search by date"""
    clear()
    dates = distinct_dates()
    print("Search by date")
    print("Here are the dates that we have entries for: \n")
    for date in dates:
        print(datetime_to_string(date))
    print("\n")
    user_input = task_date()
    
    entries = select_entries()
    entries = entries.where(Entry.date == user_input)
    list_entries(entries, user_input)
    return entries


def date_range_search():
    """Search by a range of dates"""
    while True:
        clear()
        print("Search for a range of dates\n")
        print("Start date")
        start_date = task_date()
        print("End date")
        end_date = task_date()
        
        if end_date < start_date:
            input("End date must be later than the start date. Press ENTER to continue")
            continue
            
        entries = select_entries()
        entries = entries.where(Entry.date >= start_date, Entry.date <= end_date)
        clear()
        if entries:
            display_entries(entries)

            
def time_search():
    """Search by time spent"""
    clear()
    user_input = input("Enter the time amount you would like to search for: ")
    try: 
        val = int(user_input)
    except ValueError:
        print("That is not a valid number")
    else:
        entries = select_entries()
        entries = entries.where(Entry.minutes == user_input)
        list_entries_int(entries, user_input)
        return entries


def time_search_matches(entries):
    times = []
    for entry in entries:
        time = entry.minutes
        if time not in times:
            times.append(time)
        if len(times) > 1:
            while True:
                clear()
                print("These times match your search")
                for time in times:
                    print(time)
                minutes = input("\nWhich time would you like to search?").strip()
                if minutes in times:
                    entries = Entry.select().order_by(Entry.minutes.desc()).where(
                        Entry.minutes == minutes)
                    return entries
        
            
def keyword_search():
    """Search by keyword"""
    clear()
    print("Search by keyword\n")
    user_input = input("Enter a keyword you would like to search: ")
    entries = select_entries()
    entries = entries.where(
        Entry.task_name.contains(user_input)|Entry.notes.contains(user_input))
    list_entries(entries, user_input)
    return entries


def keyword_matches(entries):
    keywords = []
    for entry in entries:
        keyword = entry.notes.strip()
        if keyword not in keywords:
            keywords.append(name)
        if len(keywords) > 1:
            while True:
                clear()
                print("These entries match your keywords")
                for keyword in keywords:
                    print(keyword)
                notes = input("\nWhich keyword would you like to search").strip()
                if notes in keywords:
                    entries = Entry.select().order_by(Entry.date.desc()).where(
                        Entry.notes == notes)
                    return entries
            
    


def distinct_dates():
    """Find all distinc dates in the database."""
    dates = []
    entries = select_entries()    
    entries = entries.order_by(Entry.date.desc())
    for entry in entries:
        date = entry.date
        if date not in dates:
            dates.append(date)
    return dates
     


def string_to_datetime(date):
    date_to_datetime = datetime.strptime(date, "%Y-%m-%d").date()
    return date_to_datetime


def datetime_to_string(date):
    date = date.strftime("%Y-%m-%d")
    return date
    

def list_entries(entries, user_input):
    clear()
    if entries:
        return display_entries(entries)        
    else:
        print("Nothing matching {} was found".format(user_input))
        response = input("\nWould you like to search for something else? [Y/N] ")
        if response.lower().strip() == 'y':
            return menu_loop()
        else:
            clear()
            return search_entries()
        
def list_entries_int(entries, user_input):
    clear()
    if entries.count() > 0:
        return display_entries(entries)        
    else:
        print("Nothing matching {} was found".format(user_input))
        response = input("\nWould you like to search for something else? [Y/N] ")
        if response.lower().strip() == 'y':
            return menu_loop()
        else:
            clear()
            return search_entries()
        


def display_entry(entry):
    print("Date: {}\nEmployee Name: {}\nTask Name: {}\nMinutes: {}\nNotes: {}"
          "".format(
            entry.date,
            entry.emmployee_name,
            entry.task_name,
            entry.minutes,
            entry.notes))

            
        
def display_entries(entries):
    index = 0
    
    while True:
        clear()
        print_entries(index, entries)
        
        if entries.count() == 1:
            print("""
            C) Press C to return to the main menu
            """)
            user_input = input("\nSelect a option from above: ").lower().strip()
            if user_input == 'c':
                menu_loop()
            else:
                input("\n{} is not a available choice, please try again."
                      "".format(user_input))
                
                
        display_nav_menu(index, entries)
        
        user_input = input("\nPlease select a option from above: ").lower().strip()
        
        if index == 0 and user_input == 'b':
            index += 1
            clear()
        elif index > 0 and index < entries.count() - 1 and user_input == 'b':
            index += 1
            clear()
        elif index == entries.count() - 1 and user_input == 'a':
            index -= 1
            clear()
        elif user_input == 'e':
            return menu_loop()
        else:
            input("{} is not a valid option, please enter A, B, or E."
                  "".format(user_input))
            
                               
                               
def print_entries(index, entries, display=True):
    if display:
        print("Showing {} of {} entry(s)".format(index + 1, entries.count()))

        
        
    print("Date: {}\nEmployee Name: {}\nTask Name: {}\nMinutes: {}\nNotes: {}"
        "".format(
            datetime_to_string(entries[index].date),
            entries[index].employee_name,
            entries[index].task_name,
            entries[index].minutes,
            entries[index].notes))      

    
def exit_program():
    """Exit the program"""
    print("The program will now close")
    sys.exit()
    
    
def display_nav_menu(index, entries):
    a = "A) Previous Entry"
    b = "B) Next Entry"
    e = "E) Return to Main Menu"
    menu = [a, b, e]
    
    if index == 0:
        menu.remove(a)
    elif index == entries.count() - 1:
        menu.remove(b)
        
    print("\n")
    for option in menu:
          print(option)
    return menu


def search_entries():
    """Lookup previous work entries"""
    choice = None
    
    while True:
        clear()
        print("Search Menu\n")
        for key, value in search_menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("\nEnter a choice: ").lower().strip()
                       
        if choice in search_menu:
            clear()
            search = search_menu[choice]()
            return search
            
        
def menu_loop():
    """Return to Main Menu"""
    choice = None
    
    while True:
        clear()
        print("Main Menu\n")
        for key, value in main_menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("\nEnter a choice: ").lower().strip()
        
        if choice in main_menu:
            clear()
            main_menu[choice]()
            
main_menu = OrderedDict([
        ('a', add_entry),
        ('b', search_entries),
        ('c', exit_program),
])
                       
search_menu = OrderedDict([
        ('e', find_employee),
        ('d', find_by_date),
        ('r', date_range_search),
        ('k', keyword_search),
        ('m', time_search),
        ('q', menu_loop)
])
    
                        
if __name__ == '__main__':
    initialize()
    clear()
    input("Welcome, press ENTER to continue")
    menu_loop()
