import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query, (first_name, last_name, github,))
    CONN.commit()
    print "Successfully added student: %s %s"%(first_name, last_name)

def get_project_title(project_title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (project_title,))
    row = DB.fetchone()
    print """\
Title: %s, Description: %s, Max Grade: %s"""%(row[0], row[1], row[2])
    # return row

def get_all_grades_project(project_title):
    query = """SELECT first_name, last_name, grade FROM Grades2 INNER JOIN Students ON Grades2.student_github=Students.github WHERE Grades2.project_title = ?"""
    DB.execute(query, (project_title,))
    all_info = DB.fetchall()
    counter = 0
    dictionary = {}
    length = len(all_info)
    
    while counter in range(0, length):
        first_name = all_info[counter][0]
        last_name = all_info[counter][1]
        name = first_name + " " + last_name
        grade = all_info[counter][2]
        dictionary[name] = grade
        counter += 1
    return dictionary


def new_project(title, max_grade, description):
    query = """INSERT into Projects values (?, ?, ?)"""
    DB.execute(query, (title, max_grade, description,))
    CONN.commit()
    print "Successfully added project: %s"%title

def get_grade(first_name, last_name, project_title):
    query1 = """SELECT github FROM Students WHERE first_name = ? AND last_name = ?"""
    query2 = """SELECT grade FROM Grades2 WHERE project_title = ? AND student_github = ?"""
    DB.execute(query1, (first_name, last_name,))
    github = DB.fetchone()
    DB.execute(query2, (project_title, github[0],))
    row = DB.fetchone()
    print "Grade is %s"%(row[0])

def record_grade(first_name, last_name, project_title, grade):
    query = """SELECT github FROM Students WHERE first_name = ? AND last_name = ?"""
    query2 = """UPDATE Grades2 set grade = ? WHERE student_github = ? AND project_title = ?"""
    DB.execute(query, (first_name, last_name,))
    github = DB.fetchone()
    DB.execute(query2, (grade, github[0], project_title,))
    CONN.commit()
    
def show_all_grades(first_name, last_name):
    query = """SELECT github FROM Students WHERE first_name = ? AND last_name = ?"""
    query2 = """SELECT project_title, grade FROM Grades2 WHERE student_github = ?"""
    DB.execute(query, (first_name, last_name,))
    github = DB.fetchone()
    DB.execute(query2, (github[0],))
    grades = DB.fetchall()
    counter = 0
    all_grades = {}
    length = len(grades)
    while counter in range(0, length):
        project_name = grades[counter][0]
        project_grade = grades[counter][1]
        all_grades[project_name] = project_grade
        counter += 1
    return all_grades

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        if command == "new_project":
            if len(tokens)>3:
                desc = ""
                for word in tokens[3:]:
                    desc += word + " "
                tokens[3] = desc
                print tokens[3]
                del tokens[4:]    
            args = tokens[1:]
            new_project(*args)
        else: 
            args = tokens[1:]

        if command == "student_by_github":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "get_project_title":
            get_project_title(*args)
        elif command == "get_grade":
            get_grade(*args)
        elif command == "record_grade":
            record_grade(*args)
        elif command == "show_all_grades":
            show_all_grades(*args)
        elif command == "get_all_grades_project":
            get_all_grades_project(*args)

    CONN.close()

if __name__ == "__main__":
    main()
