from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
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
    currentHP = db.Column(db.Integer)
    tempHP = db.Column(db.Integer)
    #Proficiency Bonus
    proficiency = db.Column(db.Integer)
    #Ability Scores
    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)
    #MONEY
    charCopper = db.Column(db.Integer)
    charSilver = db.Column(db.Integer)
    charGold = db.Column(db.Integer)
    charPlatinum = db.Column(db.Integer)

    #MUST DEFINE RELATIONSHIPS WITH OTHER TABLES
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
#    items = db.relationship('Item')

    def __init__(self, name, race, charclass, level, background, alignment, exp, hp, currentHP, tempHP, proficiency, strength, dexterity, constitution, intelligence, wisdom, charisma, charCopper, charSilver, charGold, charPlatinum, owner):
        self.name = name
        self.race = race
        self.charclass = charclass
        self.level = level
        self.background = background
        self.alignment = alignment
        self.exp = exp
        self.hp = hp
        self.currentHP = currentHP
        self.tempHP = tempHP
        self.proficiency = proficiency
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.charCopper = charCopper
        self.charSilver = charSilver
        self.charGold = charGold
        self.charPlatinum = charPlatinum
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

#CREATES NEW CHARACTER UPON SUBMISSION - NEEDS MORE INFORMATION TO FULLY CREATE CHARACTER, BUT CURRENTLY IS FUNCTIONING
@app.route('/newCharacter', methods=['POST', 'GET'])
def createNew():
    name = request.form['charName']
    race = request.form['charRace']
    charclass = request.form['charClass']
    level = int(request.form['level'])
    background = request.form['background']
    alignment = request.form['alignment']

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

#SET RACIAL ABILITY SCORE MODIFIERS <--FUNCTIONING; WILL NEED SPECIFICS FOR PARTICULAR SUBRACES (IE HILL DWARF AND HIGH ELF)
    strbns = 0
    dexbns = 0
    conbns = 0
    intbns = 0
    wisbns = 0
    chabns = 0
    if race == 'Dwarf':
        conbns = 2
        wisbns = 1
    if race == 'Elf':
        dexbns = 2
        intbns = 1
        wisbns = 1
    if race == 'Halfling':
        dexbns = 2
    if race == 'Human':
        strbns = 1
        dexbns = 1
        conbns = 1
        intbns = 1
        wisbns = 1
        chabns = 1
    if race == 'Dragonborn':
        strbns = 2
        chabns = 1
    if race == 'Gnome':
        intbns = 2
    if race == 'Half-Elf':
        intbns = 1
        chabns = 2
    if race == 'Half-Orc':
        strbns = 2
        conbns = 1
    if race == 'Tiefling':
        intbns = 1
        chabns = 2

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

#SET HP
    #Need TOTAL Constitution Mod for start HP
    if int(constitution + conbns)%2==0:
        conmod = int((int((constitution + conbns)-10))/2)
    else:
        conmod = int((int((constitution + conbns)-11))/2)
    #HP Functions
    hp = 0
    if charclass == "Barbarian":
        hp = 12 + conmod + (7*(level-1))
    if charclass == "Bard" or charclass == "Cleric" or charclass == "Druid" or charclass == "Monk" or charclass == "Rogue" or charclass == "Warlock":
        hp = 8 + conmod + (5*(level-1))
    if charclass == "Fighter" or charclass == "Paladin" or charclass == "Ranger":
        hp = 10 + conmod + (6*(level-1))
    if charclass == "Sorcerer" or charclass == "Wizard":
        hp = 6 + conmod + (4*(level-1))
#SETS CHARACTERS MONEY (CURRENTLY STATIC, BUT WILL BE MADE TO FIT DIFFERENT CLASSES)
    charCopper = 0
    charSilver = 0
    charGold = 15
    charPlatinum = 0
# #SUBMITS CHARACTER STATS TO DB
    owner = User.query.filter_by(email=session['email']).first()
    if request.method == 'POST':
        newChar = Character(name, race, charclass, level, background, alignment, exp, hp, proficiency, strength, dexterity, constitution, intelligence, wisdom, charisma, charCopper, charSilver, charGold, charPlatinum, owner)
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

#SAVE DC CALCULATION <-- Works, but FIGHTER CLASS could use work either on this end or in HTML
    savedc = 0
    strmansavedc = "N/A" #FOR FIGHTERS ONLY
    dexmansavedc = "N/A" #FOR FIGHTERS ONLY
    if thisCharacter.charclass == "Bard" or thisCharacter.charclass == "Paladin" or thisCharacter.charclass == "Warlock" or thisCharacter.charclass == "Sorcerer":
        savedc = 8 + thisCharacter.proficiency + chamod
    if thisCharacter.charclass == "Cleric" or thisCharacter.charclass == "Druid" or thisCharacter.charclass == "Ranger":
        savedc = 8 + thisCharacter.proficiency + wismod
    if thisCharacter.charclass == "Fighter" or thisCharacter.charclass == "Rogue" or thisCharacter == "Wizard":
        savedc = 8 + thisCharacter.proficiency + intmod
    if thisCharacter.charclass == "Fighter":
        strmansavedc = 8 + thisCharacter.proficiency + strmod
        dexmansavedc = 8 + thisCharacter.proficiency + dexmod

#AC CALCULATION <-- INCOMPLETE, BUT WORKING
    armor = 0
    shield = 0

    if armor > 0:
        ac = dexmod + armor + shield
    elif thisCharacter.charclass == "Barbarian":# and thisCharacter.armor = 0: <Need to create an armor handler
        ac = 10 + dexmod + conmod + shield
    else:
        ac = 10 + dexmod + shield

#ATTACK BONUS CALCULATIONS FOR PRIMARY ATTACK METHOD <-- DO THIS ONE
    meleeAttackMod = 0
    rangedAttackMod = 0
    spellAttackMod = 0

#CHARACTER BACKGROUND PROFICIENCY BONUS
#All Skills proficiencies initialized at 0
    charPro = int(thisCharacter.proficiency)

    acrpro = 0
    anipro = 0
    arcpro = 0
    athpro = 0
    decpro = 0
    hispro = 0
    inspro = 0
    intpro = 0
    invpro = 0
    medpro = 0
    natpro = 0
    perpro = 0
    prfpro = 0
    prspro = 0
    relpro = 0
    slgpro = 0
    stepro = 0
    surpro = 0
#Modifies 
    if thisCharacter.background == "Acolyte":
        inspro = charPro
        relpro = charPro
    if thisCharacter.background == "Charlatan":
        decpro = charPro
        slgpro = charPro
    if thisCharacter.background == "Criminal":
        decpro = charPro
        stepro = charPro
    if thisCharacter.background == "Entertainer":
        acrpro = charPro
        prfpro = charPro
    if thisCharacter.background == "Folk Hero":
        anipro = charPro
        surpro = charPro
    if thisCharacter.background == "Guildartisan":
        inspro = charPro
        prspro = charPro
    if thisCharacter.background == "Hermit":
        medpro = charPro
        relpro = charPro
    if thisCharacter.background == "Noble":
        hispro = charPro
        prspro = charPro
    if thisCharacter.background == "Out Lander":
        athpro = charPro
        surpro = charPro
    if thisCharacter.background == "Sage":
        arcpro = charPro
        hispro = charPro
    if thisCharacter.background == "Sailor":
        athpro = charPro
        perpro = charPro
    if thisCharacter.background == "Soldier":
        athpro = charPro
        intpro = charPro
    if thisCharacter.background == "Urchin":
        slgpro = charPro
        stepro = charPro

#SETS HP BASED ON LEVEL (USES AVERAGE PROVIDED IN PH FOR EACH CLASS)
    hp = 0
    if thisCharacter.charclass == "Barbarian":
        hp = 12 + conmod + (7*(thisCharacter.level-1))
    if thisCharacter.charclass == "Bard" or thisCharacter.charclass == "Cleric" or thisCharacter.charclass == "Druid" or thisCharacter.charclass == "Monk" or thisCharacter.charclass == "Rogue" or thisCharacter.charclass == "Warlock":
        hp = 8 + conmod + (5*(thisCharacter.level-1))
    if thisCharacter.charclass == "Fighter" or thisCharacter.charclass == "Paladin" or thisCharacter.charclass == "Ranger":
        hp = 10 + conmod + (6*(thisCharacter.level-1))
    if thisCharacter.charclass == "Sorcerer" or thisCharacter.charclass == "Wizard":
        hp = 6 + conmod + (4*(thisCharacter.level-1))

#RETURN STATEMENT
    return render_template('character.html', title=thisCharacter.name, thisCharacter=thisCharacter, strmod=strmod, dexmod=dexmod, conmod=conmod, intmod=intmod, wismod=wismod, chamod=chamod, ac=ac, charPro=charPro, acrpro=acrpro, anipro=anipro, arcpro=arcpro, athpro=athpro, decpro=decpro, hispro=hispro, inspro=inspro, intpro=intpro, invpro=invpro, medpro=medpro, natpro=natpro, perpro=perpro, prfpro=prfpro, prspro=prspro, relpro=relpro, slgpro=slgpro, stepro=stepro, surpro=surpro, savedc=savedc, strmansavedc=strmansavedc, dexmansavedc=dexmansavedc, hp=hp)#meleeAttackMod=meleeAttackMod, rangedAttackMod=rangedAttackMod, spellAttackMod=spellAttackMod)

#UPDATE CHARACTER FROM CHARACTERSHEET SCREEN <--NEW SECTION (SUCCESSFULLY RETRIEVS ID, XP, AND UPDATES XP; NEEDS TO UPDATE LEVEL, WHEN APPROPRIATE)
@app.route('/updateXP', methods=['POST', 'GET'])
def updateXP():
    #Identify Character with Character ID
    CID = request.form["charID"]
    thisCharacter = Character.query.get(CID)
    #Get Current XP from TABLE
    currentXP = thisCharacter.exp
    plusXP = int(request.form['additionalXP']) #CRASHES IF THIS IS BLANK
    newXP = currentXP + plusXP
#GIVES NEW LEVEL AND NEW PROFICIENCY BONSU
    if newXP <= 299:
        newLevel = 1
        newProficiency = 2
    if newXP > 299 and newXP < 900:
        newLevel = 2
        newProficiency = 2
    if newXP >= 900 and newXP < 2700:
        newLevel = 3
        newProficiency = 2
    if newXP >= 2700 and newXP < 6500:
        newLevel = 4
        newProficiency = 2
    if newXP >= 6500 and newXP < 14000:
        newLevel = 5
        newProficiency = 3
    if newXP >= 14000 and newXP < 23000:
        newLevel = 6
        newProficiency = 3
    if newXP >= 23000 and newXP < 34000:
        newLevel = 7
        newProficiency = 3
    if newXP >= 34000 and newXP < 48000:
        newLevel = 8
        newProficiency = 3
    if newXP >= 48000 and newXP < 64000:
        newLevel = 9
        newProficiency = 4
    if newXP >= 64000 and newXP < 85000:
        newLevel = 10
        newProficiency = 4
    if newXP >= 85000 and newXP < 100000:
        newLevel = 11
        newProficiency = 4
    if newXP >= 100000 and newXP < 120000:
        newLevel = 12
        newProficiency = 4
    if newXP >= 120000 and newXP < 140000:
        newLevel = 13
        newProficiency = 5
    if newXP >= 140000 and newXP < 165000:
        newLevel = 14
        newProficiency = 5
    if newXP >= 165000 and newXP < 195000:
        newLevel = 15
        newProficiency = 5
    if newXP >= 195000 and newXP < 225000:
        newLevel = 16
        newProficiency = 5
    if newXP >= 225000 and newXP < 265000:
        newLevel = 17
        newProficiency = 6
    if newXP >= 265000 and newXP < 305000:
        newLevel = 18
        newProficiency = 6
    if newXP >= 305000 and newXP < 355000:
        newLevel = 19
        newProficiency = 6
    if newXP > 355000:
        newLevel = 20
        newProficiency = 6

    if request.method == 'POST':
        thisCharacter.exp = newXP
        thisCharacter.level = newLevel
        thisCharacter.proficiency = newProficiency
        db.session.commit()
        return redirect('/characterSheet?id='+CID)

#CALCULATES CHARACTER'S MONEY, BOTH SPENDING AND EARNING
@app.route('/calcMoney', methods=['POST', 'GET'])
def calcMoney():
    CID = request.form["charID"]
    thisCharacter = Character.query.get(CID)

#GET +/- MONEY FROM FORM (WORKS; NEEDS REFINMENT)
    addPlat = int(request.form['addPlat'])
    addGold = int(request.form['addGold'])
    addSilv = int(request.form['addSilv'])
    addCopp = int(request.form['addCopp'])
    subPlat = int(request.form['subPlat'])
    subGold = int(request.form['subGold'])
    subSilv = int(request.form['subSilv'])
    subCopp = int(request.form['subCopp'])

#GET CHARACTERS CURRENT MONEY AMMOUNT
    currentplat = thisCharacter.charPlatinum
    currentgold = thisCharacter.charGold
    currentsilv = thisCharacter.charSilver
    currentcopp = thisCharacter.charCopper

#SETS ROUND UP VARIABLE TO 0
    uppSilv = 0
    uppGold = 0
    uppPlat = 0
#CHANGE CHARACTERS CURRENT MONEY AMMOUNT (NEED TO MAKE CHANGES FOR values greater than one conversion)
    newCopp = currentcopp + addCopp - subCopp

    while newCopp > 99 or currentcopp > 99:
        newCopp = newCopp - 100
        uppSilv = 1
    if newCopp <= 0 or currentcopp <=0:
        newCopp = newCopp + 100
        uppSilv = -1
    newSilv = currentsilv + uppSilv + addSilv - subSilv

    if newSilv > 99 or currentsilv > 99:
        newSilv = newSilv - 100
        uppGold = 1
    if newSilv <=0 or currentsilv <= 0:
        newSilv = newSilv +100
        uppGold = -1
    newGold = currentgold + uppGold + addGold - subGold

    if newGold > 49 or currentgold > 49:
        newGold = newGold - 50
        uppPlat = 1
    if newGold <= 0 or currentgold <=0:
        newGold = newGold + 50
        uppPlat = -1
    newPlat = currentplat + uppPlat + addPlat - subPlat

#UPDATES CHARACTER MONEY
    if request.method == 'POST':
        thisCharacter.charPlatinum = newPlat
        thisCharacter.charGold = newGold
        thisCharacter.charSilver = newSilv
        thisCharacter.charCopper = newCopp
        db.session.commit()
        return redirect('/characterSheet?id='+CID)

#IN-GAME HP CONTROLS
@app.route('/hpMods', methods=['POST', 'GET'])
def hpMods():
    #Identify Character with Character ID
    CID = request.form["charID"]
    thisCharacter = Character.query.get(CID)

    #GET CURRENT HP LEVELS
    currentHP = thisCharacter.currentHP
    tempHP = int(thisCharacter.tempHP)
    hitHP = int(request.form['hitHP'])
    addTempHP = int(request.form['addTempHP'])

    #add Temp HP
    if addTempHP > 0:
        tempHP = thisCharacter.tempHP + addTempHP
    else:
        tempHP = thisCharacter.tempHP

    #take Damage
    if tempHP >= hitHP:
        tempHP = tempHP - hitHP
    elif tempHP < hitHP:
        hitHP = hitHP - tempHP
        tempHP = 0
        currentHP = currentHP - hitHP
    else:
        currentHP = currentHP - hitHP

#UPDATES CHARACTER HP
    if request.method == 'POST':
        thisCharacter.tempHP = tempHP
        thisCharacter.currentHP = currentHP + tempHP
        db.session.commit()
        return redirect('/characterSheet?id='+CID)

#SHORT REST (WILL NEED SPECIFICS FOR EACH CLASS, ETC.)
@app.route('/shortRest', methods=['POST', 'GET'])
def shortRest():
    #Identify Character with Character ID
    CID = request.form["charID"]
    thisCharacter = Character.query.get(CID)
    srHPup = int(request.form['srHPup'])

    currentHP = thisCharacter.currentHP + srHPup

    if currentHP >= thisCharacter.hp:
        currentHP = thisCharacter.hp

    if request.method == 'POST':
        thisCharacter.tempHP = 0
        thisCharacter.currentHP = currentHP
        db.session.commit()
        return redirect('/characterSheet?id='+CID)

#RESETS CHARACTER HP, SPELL SLOTS, ETC FOR NEW GAME
@app.route('/newGame', methods=['POST', 'GET'])
def newGame():
    #Identify Character with Character ID
    CID = request.form["charID"]
    thisCharacter = Character.query.get(CID)
    #Resets
    if request.method == 'POST':
        thisCharacter.currentHP = thisCharacter.hp
        thisCharacter.tempHP = 0
        db.session.commit()
        return redirect('/characterSheet?id='+CID)

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