from flask import Flask, url_for, request, session
from flask import render_template
import sqlite3
import random

db = sqlite3.connect('SolvePhysics.db')
curs = db.cursor()

#list_q = [('Сколько апрьпатр', 
#           2,'1','2','3','4'),
#           ('Pi =',
#            3,'3.14','123','444','233'
#           )]

#curs.execute("""PRAGMA foreign_keys=on""")

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

#curs.execute('''
#    CREATE TABLE VoprosThemes (
#  ThemeID INT PRIMARY KEY,
#  ThemeName VARCHAR(50) NOT NULL
#);
#'''
#)

#curs.execute('ALTER TABLE Questionsss RENAME TO old_table2ghjghjghhgjghjghhghgjghjghjghj')

#curs.execute('''
#    CREATE TABLE Questionsss (
#    OuestionID INT PRIMARY KEY,
#    QuestionName TEXT NOT NULL,
#    QuestionOne TEXT NOT NULL,
#    QuestionTwo TEXT NOT NULL,
#    QuestionThree TEXT NOT NULL,
#    QuestionFour TEXT NOT NULL,
#    ThemeID INT,
#    FOREIGN KEY (ThemeID) REFERENCES VoprosThemes(ThemeID)
#);
#'''    
#)

#curs.execute('''
#INSERT INTO VoprosThemes (ThemeID, ThemeName)
#VALUES (1, 'Изопроцессы'), (2, 'Термодинамика'), (3, 'Статика');
#''')

#curs.execute('''
#INSERT INTO Questionsss (OuestionID, QuestionName, QuestionOne, QuestionTwo, QuestionThree,QuestionFour, ThemeID)
#VALUES (1, "Чё как?", "один", "два", "три", "четыре", 1), (2, "Чё как два?", "одиндва","двадва","тритри","четыречетыре", 2), (3, "Чё как три?","одинтри","одинчепыре","одинпять","одиншесть", 3);
#''')

curs.execute('SELECT * FROM Questionsss')
#print(curs.fetchall())

db.commit()

app = Flask(__name__)

app.config["SECRET_KEY"] = 'PasswordForSolvePhysicsApplicationMadeByGreatMe123321!)'

def QuizForm():
    DataQuiz = curs.execute('SELECT * FROM Questionsss ORDER BY OuestionID').fetchall()
    return DataQuiz

question = QuizForm()

db.close()

#def index():
#    if request.method == 'POST':
#        pass
#    elif request.method == 'GET':
#        pass
    
#app.add_url_rule('/SolvePart', 'index', index, methods = ['POST', 'GET'])

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
    #session['IsQuizStart'] = False
    session['RightAnswers'] = 0
    session['last_question'] = 0
    #if request.method == 'POST':
    #    return
    #elif request.method == 'GET':
    #    return render_template('SolvePart.html')
    return MadeQuestion(question[0])

@app.route('/question_solve', methods = ['POST'])
def Qustion():
    #if len(question) != (int(session['last_question'])):
    #answer = request.form['question1']
    #print(len(question), session['last_question'])
    if request.method == 'POST':# and session['IsQuizStart']:
        SaveAnswers()

    if len(question) == int(session['last_question']):
        session['last_question'] = 0
        print(session['RightAnswers'])
        return render_template('Results.html', results = session['RightAnswers'], from_q = len(question))
    else:
        next_question = question[int(session['last_question'])]
        # session['IsQuizStart'] = True
        return MadeQuestion(next_question)
# else:
           
def MadeQuestion(Question):
    answer_list = [Question[2],Question[3],Question[4],Question[5]]
    random.shuffle(answer_list)
    #session['last_question'] += 1
    return render_template('SolvePart.html',question = Question[1], question_id = Question[0], answer_list = answer_list)
    
def SaveAnswers():
    answer = request.form.get('ans_text')
    question_num = request.form.get('q_id')
    #print(request.form, 'Дата')
    #print(answer, question[int(session['last_question'])][2])
    if answer == question[int(session['last_question'])][2]:
        session['RightAnswers'] += 1
    session['last_question'] = question_num
    
    #session['last_question'] += 1
    #question_id = request.form.get('question_id')
    
    #session['total'] += 1
    
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

