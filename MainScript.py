from flask import Flask, url_for, request, session
from flask import render_template
import sqlite3

db = sqlite3.connect('SolvePhysics.db')
curs = db.cursor()

list_q = [('Сколько апрьпатр', 
           2,'1','2','3','4'),
           ('Pi =',
            3,'3.14','123','444','233'
           )]

curs.execute("""PRAGMA foreign_keys=on""")

#curs.execute("DROP TABLE questions")
#curs.execute(""" CREATE TABLE IF NOT EXISTS quiz
#(id INTEGER PRIMARY KEY, name TEXT)
#""")

#curs.execute(""" CREATE TABLE IF NOT EXISTS quiz_content 
#(
#    id INTEGER PRIMARY KEY,
#    quiz_id INTEGER,
#    question_id INTEGER,
#    FOREIGN KEY (quiz_id) REFERENCES quiz (id)
#)
#""")

#curs.execute("""CREATE TABLE IF NOT EXISTS questions (
#    question TEXT,
#    max_score INTEGER,
#    correct_answer TEXT,
#    uncorrect_one TEXT,
#    uncorrect_two TEXT,
#    uncorrect_three TEXT
#)  """)

#curs.executemany(''' INSERT INTO questions VALUES(?,?,?,?,?,?)''', list_q)

#curs.execute("INSERT INTO quiz VALUES (2,'Викторина2')")

#query = "INSERT INTO quiz_content VALUES(?,?)"
#answer = input('y/n')
#while answer != 'n':
#    quiz_id = int(input('id викторины'))
#    question_id = int(input('id вопроса'))
#    curs.execute(query, [quiz_id, question_id])
#    db.commit()
#    answer = input('Добавить связь yn')

#curs.execute('SELECT * FROM questions')
#print(curs.fetchall())
#curs.execute('SELECT * FROM quiz')
#print(curs.fetchall())
#curs.execute('SELECT * FROM quiz_content')
#print(curs.fetchall())


app = Flask(__name__)

@app.route('/Main')
@app.route('/')
def hello():
    return render_template('Main.html')

@app.route('/AboutUs')
def about_us():
    return render_template('AboutUs.html')

@app.route('/Download')
def download():
    return render_template('Download.html')

@app.route('/SolvePart')
def solve_part():
    return render_template('SolvePart.html')

if __name__ == '__main__':
    app.run(debug=True)

#Добавление таблицы
#curs.execute("""CREATE TABLE questions (
#    question TEXT,
#    max_score INTEGER,
#    correct_answer TEXT,
#    uncorrect_one TEXT,
#    uncorrect_two TEXT,
#    uncorrect_three TEXT
#)  """)

#Добавление данных
#curs.execute('INSERT INTO questions VALUES ("Какая фирма у орлпрлдоьпр?", 2, "Бfghgh", "Боинг", "Чётропро там", "Рпрорпрпкосмос")')

#Удаление данных
#curs.execute('DELETE FROM questions WHERE rowid = 2')

#Обновление данных
#curs.execute('UPDATE questions SET correct_answer = "Боунггг" WHERE uncorrect_one = "Боинг"')

#Вывод данных
#curs.execute('SELECT rowid, * FROM questions WHERE rowid <= 5 ORDER BY rowid')
#print(curs.fetchone()) # | Др. команды с fetch - all, many, one(Возвращает сразу кортеж), [1] - индекс

#print(curs.fetchall())

db.commit()

db.close()
