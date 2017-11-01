from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#pylint: disable=no-member

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dndchar:Fr@nkl1n@localhost:8889/dndchar'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '11a2b3000destruct'

#CREATES CHARACTER CLASSES IN DB
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #Modifiers, character info
    name = db.Column(db.String(20))
    race = db.Column(db.String(20))
    charclass = db.Column(db.String(20))
    level = db.Column(db.Integer)
    background = db.Column(db.String(20))
    alignment = db.Column(db.String(20))
    #Experience Points
    exp = db.Column(db.Integer)
    #Hit Points
    hp = db.Column(db.Integer)
    #Proficiency Bonus
    proficiency = db.Column(db.Integer)
    #Ability Scores
    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)

    #MUST DEFINE RELATIONSHIPS WITH OTHER TABLES
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
#    items = db.relationship('Item')

    def __init__(self, name, race, charclass, level, background, alignment, exp, hp, proficiency, strength, dexterity, constitution, intelligence, wisdom, charisma, owner):
        self.name = name
        self.race = race
        self.charclass = charclass
        self.level = level
        self.background = background
        self.alignment = alignment
        self.exp = exp
        self.hp = hp
        self.proficiency = proficiency
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.owner = owner


#class Item(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    character = db.relationship('Character')
#    owner = db.Column(db.String, db.ForeignKey(character.id))
    # def __init__(self, owner):
    #     self.blog_title = blog_title
    #     self.blog_text = blog_text
    #     self.owner = owner

#CREATES USERS CLASSES IN DB
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(20))
    characters = db.relationship('Character', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

#REQUIRES LOGIN BEFORE ALLOWING ACCESS
@app.before_request
def require_login():
    allowed_routs = ['login', 'register']
    if request.endpoint not in allowed_routs and 'email' not in session:
        return redirect('/login')

#ALLOWS EXISTING USERS TO LOG IN
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged In")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html', title="Account Login")

#ALLOWS NEW USERS TO REGISTER
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        if len(password) <= 2 or len(password) >= 21 or ' ' in password:
            flash('Password must be at least three (3) characters long and CANNOT contain spaces.', 'error')
            return render_template('register.html', email=email)

        if password != verify:
            flash('Passwords MUST match.  Please re-enter.', 'error')
            return render_template('register.html', email=email)

        existing_user = User.query.filter_by(email=email).first()

        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/login')
        else:
            flash('User name already exists', 'error')
            return redirect('/login')

    return render_template('register.html', title="Register New Account")

#LINKS TO HOME PAGE - CURRENTLY THE SAME AS USERCHARACTERS; NEEDS SOMETHING ELSE
@app.route('/', methods=['POST', 'GET'])
def index():
    owner = User.query.filter_by(email=session['email']).first()
    characters = Character.query.filter_by(owner=owner).all()
    return render_template('characters.html', title='Manage Your Characters', characters=characters, owner=owner)

#LINKS TO CREATE NEW USER FORM
@app.route('/createNewChar', methods=['POST', 'GET'])
def createForm():
    return render_template('create.html', title="Create New Character")

#CREATES NEW USER UPON SUBMISSION - NEEDS MORE INFORMATION TO FULLY CREATE CHARACTER, BUT CURRENTLY IS FUNCTIONING
@app.route('/newCharacter', methods=['POST', 'GET'])
def createNew():
    name = request.form['charName']
    race = request.form['charRace']
    charclass = request.form['charClass']
    level = int(request.form['level'])
    background = request.form['background']
    alignment = request.form['alignment']
    hp = 0
#SET STARTING EXPERIENCE POINTS, BASED ON STARTING LEVEL
    if level == 1:
        exp = 0
    if level == 2:
        exp = 300
    if level == 3:
        exp = 900
    if level == 4:
        exp = 2700
    if level == 5:
        exp = 6500
    if level == 6:
        exp = 14000
    if level == 7:
        exp = 23000
    if level == 8:
        exp = 34000
    if level == 9:
        exp = 48000
    if level == 10:
        exp = 64000
    if level == 11:
        exp = 85000
    if level == 12:
        exp = 100000
    if level == 13:
        exp = 120000
    if level == 14:
        exp = 140000
    if level == 15:
        exp = 165000
    if level == 16:
        exp = 195000
    if level == 17:
        exp = 225000
    if level == 18:
        exp = 265000
    if level == 19:
        exp = 305000
    if level == 20:
        exp == 355000

#SET PROFICIENCY BONUS BASED ON CHARACTER LEVEL
    if level <= 4:
        proficiency = 2
    if level >= 5 and level <= 8:
        proficiency = 3
    if level >= 9 and level <= 12:
        proficiency = 4
    if level >= 13 and level <= 16:
        proficiency = 5
    if level >= 17:
        proficiency = 6

#SET RACIAL ABILITY SCORE MODIFIERS <--THIS IS CAUSING ERRORS?
    if race == 'Dwarf':
        strbns = 4
        dexbns = 0
        conbns = 2
        intbns = 0
        wisbns = 1
        chabns = 0

    if race == 'Elf':
        strbns = 0
        dexbns = 2
        conbns = 0
        intbns = 1
        wisbns = 1
        chabns = 0

    if race == 'Halfling':
        strbns = 0
        dexbns = 2
        conbns = 0
        intbns = 0
        wisbns = 0
        chabns = 0

    if race == 'Human':
        strbns = 1
        dexbns = 1
        conbns = 1
        intbns = 1
        wisbns = 1
        chabns = 1

    if race == 'Dragonborn':
        strbns = 2
        dexbns = 0
        conbns = 0
        intbns = 0
        wisbns = 0
        chabns = 1

    if race == 'Gnome':
        strbns = 0
        dexbns = 0
        conbns = 0
        intbns = 2
        wisbns = 0
        chabns = 0

    if race == 'Half-Elf':
        strbns = 0
        dexbns = 0
        conbns = 0
        intbns = 1
        wisbns = 0
        chabns = 2

    if race == 'Half-Orc':
        strbns = 2
        dexbns = 0
        conbns = 1
        intbns = 0
        wisbns = 0
        chabns = 0

    if race == 'Tiefling':
        strbns = 0
        dexbns = 0
        conbns = 0
        intbns = 1
        wisbns = 0
        chabns = 2

#SET CLASS ABILITY MODIFIERS <-- NEXT <-- NEXT

#ABILITY SCORES WITH MODIFIERS
    strength = int(request.form['strength'])
    strength = strength + strbns
    dexterity = int(request.form['dexterity'])
    dexterity = dexterity + dexbns
    constitution = int(request.form['constitution'])
    constitution = constitution + conbns
    intelligence = int(request.form['intelligence'])
    intelligence = intelligence + intbns
    wisdom = int(request.form['wisdom'])
    wisdom = wisdom + wisbns
    charisma = int(request.form['charisma'])
    charisma = charisma + chabns

#SUBMITS CHARACTER STATS TO DB
    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        newChar = Character(name, race, charclass, level, background, alignment, exp, hp, proficiency, strength, dexterity, constitution, intelligence, wisdom, charisma, owner)
        db.session.add(newChar)
        db.session.commit()
        thisChar = str(newChar.id)
        return redirect('/characterSheet?id='+thisChar)

#PRODUCES CHARACTER SHEET PAGE - PAGE NEEDS ALL INFORMATION AND FORMATTING IN HTML
@app.route('/characterSheet', methods=['POST', 'GET'])
def charSheet():
    character_id = request.args.get('id')
    thisCharacter = Character.query.get(character_id)

#ABILITY SCORE MODIFIERS - DOES NOT CHANGE ABILITY SCORE; CALCULATES MODIFIERS BASED ON ABILITY SCORES
    if int(thisCharacter.strength)%2==0:
        strmod = int((int(thisCharacter.strength-10))/2)
    else:
        strmod = int((int(thisCharacter.strength-11))/2)

    if int(thisCharacter.dexterity)%2==0:
        dexmod = int((int(thisCharacter.dexterity-10))/2)
    else:
        dexmod = int((int(thisCharacter.dexterity-11))/2)

    if int(thisCharacter.constitution)%2==0:
        conmod = int((int(thisCharacter.constitution-10))/2)
    else:
        conmod = int((int(thisCharacter.constitution-11))/2)

    if int(thisCharacter.intelligence)%2==0:
        intmod = int((int(thisCharacter.intelligence-10))/2)
    else:
        intmod = int((int(thisCharacter.intelligence-11))/2)

    if int(thisCharacter.wisdom)%2==0:
        wismod = int((int(thisCharacter.wisdom-10))/2)
    else:
        wismod = int((int(thisCharacter.wisdom-11))/2)

    if int(thisCharacter.charisma)%2==0:
        chamod = int((int(thisCharacter.charisma-10))/2)
    else:
        chamod = int((int(thisCharacter.charisma-11))/2)

#SAVE DC CALCULATION
    savedc = 0

#AC CALCULATION
    ac = 10 + dexmod

#ATTACK BONUS CALCULATIONS FOR PRIMARY ATTACK METHOD
    meleeAttackMod = 0
    rangedAttackMod = 0
    spellAttackMod = 0
    return render_template('character.html', title=thisCharacter.name, thisCharacter=thisCharacter, strmod=strmod, dexmod=dexmod, conmod=conmod, intmod=intmod, wismod=wismod, chamod=chamod, ac=ac)#, savedc=savedc, ac=ac, meleeAttackMod=meleeAttackMod, rangedAttackMod=rangedAttackMod, spellAttackMod=spellAttackMod)

#RENDERS PAGE OF CHARACTERS CREATED BY CURRENT USER
@app.route('/userCharacters', methods=['POST', 'GET'])
def characters():
    owner = User.query.filter_by(email=session['email']).first()
    characters = Character.query.filter_by(owner=owner).all()
    return render_template('characters.html', characters=characters, owner=owner, title=owner.email)

#LOGS OUT CURRENT LOGGED-IN USER
@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

if __name__ == '__main__':
    app.run()