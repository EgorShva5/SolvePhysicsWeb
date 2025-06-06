from flask import Flask, url_for, request, session, render_template, redirect
#from flask_sqlalchemy import SQLAlchemy
from DatabasesScript import Base, Article, User, UserDeepInfo, Question, QuestionThemes, Theory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_socketio import SocketIO, join_room, leave_room, send
import sqlite3, re, random , Config

#from flask_mysqldb import MySQL

#db = sqlite3.connect('SolvePhysics.db',  check_same_thread=False)
#curs = db.cursor()

#curs.execute('SELECT * FROM Questionsss')
#print(curs.fetchall())

#db.commit()

app = Flask(__name__)

app.config["SECRET_KEY"] = 'PasswordForSolvePhysicsApplicationMadeByGreatMe123321!)'

socketio = SocketIO(app)

engine = create_engine('sqlite:///SolvePhysics.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession2 = sessionmaker(bind=engine)
db_session = DBSession()
db_session_new_quest = DBSession2()

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SolvePhysics.db'
#database = SQLAlchemy(app)

#Будущая DB
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'password'
#app.config['MYSQL_DB'] = 'AllData'
#mysql = MySQL(app)

#               Берём из DB все вопросы по определённой теме
def QuizForm(thid):
    Questions = db_session.query(Question).filter_by(ThemeID = thid).all()
    #print(Questions)
    return Questions

#               Превращаем вопросы из объекта DB в список, отсекаем 10 из них, нумеруем, передаём в сессию получившийся список
def MadeQsts(id):
    questions = QuizForm(id)
    random.shuffle(questions)
    
    quests = []
    for e,i in enumerate(questions):
        if e == 10: break
        current_quest = []
        current_quest.append(e)
        current_quest.append(i.QuestionName)
        current_quest.append(i.QuestionOne)
        current_quest.append(i.QuestionTwo)
        current_quest.append(i.QuestionThree)
        current_quest.append(i.QuestionFour)
    
        quests.append(current_quest)

    session['questions'] = quests

    #print(quests)
#print(QuizForm(1))

#              Берём из DB всю теорию 
def TheoryData():
    Data = db_session.query(Theory).order_by(Theory.TheoryID).all()
    #Data = curs.execute('SELECT * FROM Theory ORDER BY TheoryID').fetchall()
    #print(Data)
    return Data

#               Берём из DB список всех тем, соотетствующих определённому разделу(1 - ОГЭ, 2 - ЕГЭ, 3 - Обычные задания)
def GetThemes(RazdelID):
    #print('Lf3')
    Themes = db_session.query(QuestionThemes).filter_by(RazdelID = RazdelID).all()
    #print(Themes)
    return Themes

#theory = TheoryData()

#db.close()

                #Старт сайта. Убираем имя пользователя, перенаправляем на домашнюю страничку
@app.route('/')
def ready():
    session['username'] = ''
    return redirect('/Main')

                #Домашняя страничка
@app.route('/Main')
def hello():
    return render_template('Main.html', username= session['username'])

                #Регистрация
@app.route('/Register', methods = ['GET','POST'])
def Registration():
    message = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        school = request.form.get('school_name')
        type_account = request.form.get('type')
        
        NewUser = User(username=username, password=password, email=email)
        
        Check = db_session.query(User).filter_by(username=NewUser.username).first()
        
        if Check:
            message = 'Такой аккаунт уже существует!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Некорректный email адрес!'
        elif not re.match(r'[A-Za-z0-9а-яА-я]+', username):
            message = 'Имя пользователя должно содержать только буквы и цифры!'
        elif not username or not password or not email:
            message = 'Пожалуйста, заполните все поля!'
        else:
            try:
                db_session.rollback()
                
                db_session.add(NewUser)
                db_session.commit()
                Account = db_session.query(User).filter_by(username=username).first()
                
                UserInfo = UserDeepInfo(ID= Account.id, EGERight = 0, EGEFalled = 0, EGECommon = 0,OGERight = 0, OGECommon = 0, OGEFalled = 0, COMMONRight = 0,COMMONFalled = 0, COMMONCommon = 0, TYPE = type_account, SCHOOl = school)
                db_session.add(UserInfo)
                db_session.commit()
                message = 'Вы успешно зарегестрировались'
            except: 
                message = 'Ошибка'
            finally:
                db_session.close()
            
    return render_template('Registration.html', message = message, username= session['username'])

#               Вход
@app.route('/Enter', methods = ['GET', 'POST'])
def Enter():
    message = ''
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #print(usernamee)
        #print(db_session.query(User).filter_by(username=usernamee).first().password)
        
        Account = db_session.query(User).filter_by(username=username).first()
        if Account:
            AccountInfo = db_session.query(UserDeepInfo).filter_by(ID=Account.id).first()
            
            SetInfo(AccountInfo, AccountInfo.SCHOOl)
            
            if password == Account.password:
                message = 'Вы успешно вошли в аккаунт!'
                session['username'] = username
                session['id'] = Account.id
                session['log_on'] = True
            else:
                message = 'Логин или пароль не верный!'
        else: message = 'Нет такого пользователя!'
        
        return render_template('Enter.html', message=message, username= session['username'])
    
    return render_template('Enter.html', message=message, username= session['username'])

#               Страничка аккаунта, передаём всю информацию по нему для статистики.
@app.route('/Account')
def AccountInfo():
    return render_template('AccountInfo.html', username = session['username'], id = session['id'], reg_date = session['RegDate'], school = session['School'], acc_type = session['Type'])

#               Выход из аккаунта
@app.route('/LogOut')
def LogOut():
    session.pop('log_on', False)
    session.pop('id', None)
    session.pop('username', '')
    return(redirect('/'))

#               Показываем список всех статей
@app.route('/Feed')
def ShowFeed():
    arts = db_session.query(Article).all()
#    print(arts)
    return render_template('Feed.html', result = arts, username= session['username'])

#               Показываем определённую статью по ID
@app.route('/Feed/<int:id>')
def ShowFeedArticle(id):
    art = db_session.query(Article).filter_by(id=id).one()
    print(art)
    return render_template('ArticleFeed.html',result=art, username= session['username'])

#               Создаём статью
@app.route('/ArticleCreate', methods = ['GET','POST'])
def CreateArticle():
    if request.method == 'POST':
        Title = request.form.get('Title')
        Text = request.form.get('MainText')
        Author = request.form.get('Author')
        Intro = request.form.get('Intro')

        Art = Article(title = Title, main_text = Text, author = Author, intro = Intro)
        
        try:
            db_session.rollback()
            db_session.add(Art)
            db_session.commit()
            return redirect('/Feed')
        except:
            return 'Ошибка!'
        finally:
            db_session.close()
    
    else:
        return render_template('ArticleCreate.html', username= session['username'])

#               Заготовка чата
@app.route('/Chat', methods = ['GET', 'POST'])
def Chat():
    pass

#               Страничка "О нас"
@app.route('/AboutUs')
def about_us():
    return render_template('AboutUs.html', username= session['username'])

#               Страничка "Скачать"
@app.route('/Download')
def download():
    return render_template('Download.html', username= session['username'])

#               Станичка выбора раздела задания
@app.route('/SolvePt')
def razdels():
    return render_template('TypeChange.html', username= session['username'])

#               Делаем теорию из объектов ДБ в списки, вложенные в список, сортируем по первому элемента(ID теории), если теория выбрана - переключаем на результат
@app.route('/Theory', methods = ['POST', 'GET'])
def TheoryPage():
    sortedTheory = []
    
    theory = TheoryData()
    
    for i in theory:
        t_lis = []
        t_lis.append(i.TheoryID)
        t_lis.append(i.Name)
        t_lis.append(i.Description)
        t_lis.append(i.Image)
        sortedTheory.append(t_lis)
    
    unsortedTheory = sortedTheory
    sortedTheory = sorted(sortedTheory, key = lambda x: x[1])
    #print(sortedTheory)
    
    if request.method == 'POST':
        answer = request.form.get('theory_btn')
     #   print(answer)
      #  print(sortedTheory)
        if answer:
            return render_template('TheoryResult.html', themes_list=unsortedTheory, theme_id=(int(answer)-1), username= session['username'])
        else:
            return render_template('Theory.html', themes_list = sortedTheory, message = 'Выберите одну из тем!', username= session['username'])
    elif request.method == 'GET':
        return render_template('Theory.html', themes_list = sortedTheory, message = '', username= session['username'])

#
@app.route('/SolvePartTheme', methods = ['GET', 'POST'])
def ChangeThemePage():
   # print(request.method)
    if request.method == 'POST':
       # print('fgfghfgh')
        answer = request.form.get('theory_btn')
        if answer:
           # print(int(answer))
            #print('/SolvePart/'+answer)
            return redirect('/SolvePart/'+answer) #redirect(url_for('solve_part',ThemeId=int(answer)))
        else:
            #print('Бадабумбумбум')
           # print('Абракадабра')
            # = 
            #print(listThem)
            listThem = {}
            TasksType = int(request.form.get('task_type'))
            Fl = request.form.get('list')[2:-2].split('), (')
            for i in Fl:
                #print(i)
                Nl = i.split(',')
                #print(Nl)#print(Nl[0])#print(Nl[-1][2:-2])
                listThem[int(Nl[0])] = Nl[-1][2:-1]
            listThem = sorted(listThem.items(), key=lambda item: item[1])
            #print('Инфа', listThem)
            return render_template('SolvePartThemes.html', task_type = TasksType, themes_list = listThem, message = 'Выберите одну из тем!', username= session['username'])
    elif request.method == 'GET':
        TasksType = request.args.get('type')
        
        try: 
            listThem = {}
        #SimpleList = []     
           # print('Lf2') 
          #  print(int(TasksType))
            if int(TasksType) in [1,2,3]:
               # print('Lf') 
                themes = GetThemes(int(TasksType))
              #  print('Темы:',themes)
                for i in themes: 
                    listThem[i.ThemeID] = i.ThemeName
                    
                listThem = sorted(listThem.items(), key=lambda item: item[1])
               # print(listThem)
                return render_template('SolvePartThemes.html', task_type = int(TasksType), themes_list = listThem, message = '', username= session['username'])
        
            else: return 'Что-то пошло не так!'
        except: 
            return 'Что-то пошло не так!'

@app.route('/SolvePart/<ThemeId>', methods = ['GET', 'POST'])
def solve_part(ThemeId):
    
    MadeQsts(id=ThemeId)
    #session['IsQuizStart'] = False
    session['RightAnswers'] = 0
    session['minus'] = None
    session['last_question'] = 0
    #if request.method == 'POST':
    #    return
    #elif request.method == 'GET':
    #    return render_template('SolvePart.html')
    return MadeQuestion(session['questions'][0])

@app.route('/question_solve', methods = ['POST'])
def Qustion():
    #if len(question) != (int(session['last_question'])):
    #answer = request.form['question1']
    #print(len(question), session['last_question'])
    if request.method == 'POST' and session['Solved'] == False:# and session['IsQuizStart']:
        #SaveAnswers()
        
        answer = request.form.get('ans_text')
        question_num = request.form.get('q_id')
        SaveAnswers(answer=answer, question_num=question_num)
        
        #print(session['last_question'])
        
        session['Solved'] = True 
        
        return render_template('SolvePart.html',Right = answer, Solve = session['questions'][int(session['last_question'])-1][2], username= session['username'])
        
    elif request.method == 'POST' and session['Solved'] == True:
        
        if len(session['questions']) == int(session['last_question']):
            session['last_question'] = 0
            session['minus'] = None
            #print(session['RightAnswers'])
            right_ans = session['RightAnswers']
            session['RightAnswers'] = 0
            return render_template('Results.html', results = right_ans, from_q = len(session['questions']), username= session['username'])
        else:
            next_question = session['questions'][int(session['last_question'])]
            # session['IsQuizStart'] = True
            return MadeQuestion(next_question)
# else:

@app.route('/KidsGames')
def KidsGames():
    return render_template('KidsGames.html', username= session['username'])

@app.route("/OpenGame")
def OpenGame():
    return redirect('https://egors-toxic-waste.itch.io/solarsystem')

@app.route('/HowToCreateArticle')
def HowArtCr():
    return render_template('HowToCreateArticle.html', username= session['username'])

@app.route('/DevScene', methods = ['GET', 'POST'])
def DeveloperScene():
    if request.method == 'GET':
        #login = request.args.get('login')
        #passworrd = request.args.get('password')
        
        return render_template('ModPage.html', log_on = 'Нет', message = '', username= session['username'])
    
    elif request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        
        ModsName = Config.Mods.keys()
        
        if login in ModsName:
            if Config.Mods[login] == password:
                return render_template('ModPage.html',user=login,passw=password,log_on = 'Да', message = '', username= session['username'])
            else:
                return render_template('ModPage.html', log_on = 'Нет', message = 'Неверный пароль!', username= session['username'])
        else:
            return render_template('ModPage.html', log_on = 'Нет', message = 'Нет такого пользователя!', username= session['username'])

@app.route('/CreateQuestion', methods = ['GET', 'POST'])
def CreateQuest():
    if request.method == 'GET':
        login = request.args.get('user')
        pw = request.args.get('passw')
        
        ModsName = Config.Mods.keys()
        
        if login in ModsName:
            if Config.Mods[login] == pw:
                return render_template('CreateQuestion.html', message='', username= session['username'])
            else:
                return redirect('/DevScene')
        else:
            return redirect('/DevScene')
    elif request.method == 'POST':
        text = request.form.get('MainText')
        RightAns = request.form.get('RightAns')
        SecondAns = request.form.get('SecondAns')
        ThirdAns = request.form.get('ThirdAns')
        FourAns = request.form.get('FourAns')
        ThemeID = request.form.get('ThemeID')
        
        Q_ID = random.randint(100000,900000)
        
        while db_session.query(Question).filter_by(OuestionID=Q_ID).first() is not None:
            Q_ID = random.randint(100000,900000)        
        
        NewQuest = Question(OuestionID = random.randint(100000,900000),QuestionName=text, QuestionOne=RightAns, QuestionTwo=SecondAns, QuestionThree=ThirdAns, QuestionFour=FourAns, ThemeID=int(ThemeID))
        
        try:
            db_session.rollback()
            db_session.add(NewQuest)
            db_session.commit()
            return render_template('CreateQuestion.html', message='Вопрос успешно создан!', username= session['username'])
        except:
            return 'Ошибка!'
        finally:
            db_session.close()

def MadeQuestion(Question):
    answer_list = [Question[2],Question[3],Question[4],Question[5]]
    random.shuffle(answer_list)
    session['Solved'] = False
    #session['last_question'] += 1
    #print(Question[0])
    if session['minus'] == None:
        session['minus'] = Question[0] - 1
    return render_template('SolvePart.html',question = Question[1], question_id = Question[0]-session['minus'], answer_list = answer_list, username= session['username'])

def SaveAnswers(answer, question_num):
    #print('ДАааа')
    #print(request.form, 'Дата')
    #print(answer, question[int(session['last_question'])][2])
    if answer == session['questions'][int(session['last_question'])][2]:
        session['RightAnswers'] += 1
    session['last_question'] = question_num
    
    #session['last_question'] += 1
    #question_id = request.form.get('question_id')
    
    #session['total'] += 1

def MadeTheory():
    return render_template('Theory.html', username= session['username'])

def SetInfo(Account, School):
    session['RegDate'] = Account.REGISTERDATE.date()
    session['School'] = School
    session['Type'] = Account.TYPE
    session['EGECommon'] = Account.EGECommon
    session['OGECommon'] = Account.OGECommon
   # session['']

if __name__ == '__main__': socketio.run(app=app, debug=True)


#Старое
"""
#def index():
#    if request.method == 'POST':
#        pass
#    elif request.method == 'GET':
#        pass
    
#app.add_url_rule('/SolvePart', 'index', index, methods = ['POST', 'GET'])
"""