from sqlalchemy import Column, ForeignKey, Integer, String, Text, PrimaryKeyConstraint, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine  

import sys  

from datetime import datetime

Base = declarative_base()  
engine = create_engine('sqlite:///SolvePhysics.db')
Base.metadata.create_all(engine)  

class Article(Base):
    __tablename__ = 'article'
    
    id = Column(Integer, primary_key = True)
    title = Column(String(100), nullable = False)
    author = Column(String(30), nullable = False)
    main_text = Column(Text, nullable = False)
    intro = Column(Text, nullable=False)
    time =  Column(DateTime, default = datetime.utcnow)

class User(Base):
    __tablename__ = 'accounts'

    username = Column(String(40), nullable = False)
    password = Column(String(128), nullable = False)
    email = Column(String(40), nullable = False)
    id = Column(Integer, primary_key=True)

class UserDeepInfo(Base):
    __tablename__ = 'accounts_deep_info'
    
    ID = Column(Integer)
    EGERight = Column(Integer, nullable = False)
    EGEFalled = Column(Integer, nullable = False)
    EGECommon = Column(Integer, nullable = False)
    OGERight = Column(Integer, nullable = False)
    OGECommon = Column(Integer, nullable = False)
    OGEFalled = Column(Integer, nullable = False)
    COMMONRight = Column(Integer, nullable = False)
    COMMONCommon = Column(Integer, nullable = False)
    COMMONFalled = Column(Integer, nullable = False)
    TYPE = Column(String(20), nullable = False)
    SCHOOl = Column(String(100), nullable = False)
    REGISTERDATE = Column(DateTime, default = datetime.utcnow)
    INFOID = Column(Integer, primary_key = True)

class Question(Base):
    __tablename__ = 'Questionsss'
    
    OuestionID = Column(Integer, primary_key=True)
    QuestionName = Column(String(500), nullable = False)
    QuestionOne = Column(String(200), nullable = False)
    QuestionTwo = Column(String(200), nullable = False)
    QuestionThree = Column(String(200), nullable = False)
    QuestionFour = Column(String(200), nullable = False)
    ThemeID = Column(Integer, nullable=False)

#1: ОГЭ
#2: ЕГЭ
#3: Обычные задания

class QuestionThemes(Base):
    __tablename__ = 'VoprosThemes'
    
    ThemeID = Column(Integer, primary_key=True)
    ThemeName = Column(String(50), nullable = False)
    RazdelID = Column(Integer, nullable = False)
    
class Theory(Base):
    __tablename__ = 'Theory'
    
    TheoryID = Column(Integer, primary_key=True)
    Name = Column(Text, nullable= False)
    Description = Column(Text, nullable=True)
    Image = Column(Text, nullable=False)
    
# def __repr__(self):
#    return '<Article %r>' % self.id

# def __init__(self):
#    super().__init__()

#import sqlite3

#Работа с SQLITE


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

#curs.executemany(""" INSERT INTO questions VALUES(?,?,?,?,?,?)""", list_q)

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

#curs.execute("""
#    CREATE TABLE VoprosThemes (
#  ThemeID INT PRIMARY KEY,
#  ThemeName VARCHAR(50) NOT NULL
#);
#"""
#)

#curs.execute('ALTER TABLE Questionsss RENAME TO old_table2ghjghjghhgjghjghhghgjghjghjghj')

#curs.execute("""
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
#"""
#)

#curs.execute("""
#INSERT INTO VoprosThemes (ThemeID, ThemeName)
#VALUES (1, 'Изопроцессы'), (2, 'Термодинамика'), (3, 'Статика');
#""")

#curs.execute("""
#INSERT INTO Questionsss (OuestionID, QuestionName, QuestionOne, QuestionTwo, QuestionThree,QuestionFour, ThemeID)
#VALUES (1, "Чё как?", "один", "два", "три", "четыре", 1), (2, "Чё как два?", "одиндва","двадва","тритри","четыречетыре", 2), (3, "Чё как три?","одинтри","одинчепыре","одинпять","одиншесть", 3);
#""")
