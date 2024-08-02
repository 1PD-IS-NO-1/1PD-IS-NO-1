import sqlite3
import csv
from io import StringIO

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('attendance.db', check_same_thread=False)
        self.create_tables()
        self.initialize_courses()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS attendance
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      student_id TEXT,
                      date TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS courses
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT)''')
        self.conn.commit()

    def get_courses(self):
        c = self.conn.cursor()
        c.execute("SELECT name FROM courses")
        return [row[0] for row in c.fetchall()]

    def mark_attendance(self, matched_image_name, date):
        student_id = matched_image_name.split('_')[0]
        c = self.conn.cursor()
        c.execute("INSERT INTO attendance (student_id, date) VALUES (?, ?)",
                  (student_id, date))
        self.conn.commit()

    def export_to_csv(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM attendance")
        rows = c.fetchall()

        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['id', 'student_id', 'date'])
        cw.writerows(rows)
        return si.getvalue()
    
    def initialize_courses(self):
        courses = ['M.Sc. IN ai & ml', 'M.Sc. IN Data Science', 'M.Sc. Echonomics']
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM courses")
        if c.fetchone()[0] == 0:
            for course in courses:
                c.execute("INSERT INTO courses (name) VALUES (?)", (course,))
            self.conn.commit()