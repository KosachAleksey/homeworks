import sqlite3


conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    major TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT,
    grade INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(id)
);
''')

students_data = [
    ('Иван Иванов', 20, 'Физика'),
    ('Анна Смирнова', 21, 'Информатика'),
    ('Сергей Петров', 22, 'Биология'),
    ('Елена Кузнецова', 23, 'Химия'),
    ('Дмитрий Сидоров', 24, 'История')
]

grades_data = [
    (1, 'Алгебра', 5),
    (1, 'Геометрия', 4),
    (2, 'Программирование', 5),
    (2, 'Статистика', 4),
    (3, 'Зоология', 3),
    (3, 'Анатомия', 4),
    (4, 'Органическая химия', 5),
    (4, 'Физическая химия', 4),
    (5, 'История древнего мира', 5),
    (5, 'Средневековая история', 4)
]


cursor.executemany("INSERT INTO students(name, age, major) VALUES (?, ?, ?)", students_data)
cursor.executemany("INSERT INTO grades(student_id, subject, grade) VALUES (?, ?, ?)", grades_data)

conn.commit()

print("\nВсе студенты и их средний балл:")
for row in cursor.execute('''
SELECT s.name, AVG(g.grade) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
'''):
    print(row)

print("\nСтуденты со средним баллом больше 4:")
for row in cursor.execute('''
SELECT s.name, AVG(g.grade) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
HAVING AVG(g.grade) > 4
'''):
    print(row)

print("\nКоличество студентов по каждому направлению:")
for row in cursor.execute('''
SELECT major, COUNT(*) as count_students
FROM students
GROUP BY major
'''):
    print(row)

conn.close()