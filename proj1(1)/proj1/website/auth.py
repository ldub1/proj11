import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import Flask
from .models import User, Recipes
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
#used for emails
import smtplib
from email.message import EmailMessage
#used for mysql database
import mysql.connector
import math


appS = Flask(__name__)

auth = Blueprint('auth', __name__)
connectUser='root'
connectPassword='Iu7#01kp'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cnx = mysql.connector.connect(user='root', password='Iu7#01kp',database='massfoodies')
        cursor = cnx.cursor()
        query = ("select * from massfoodies.accounts where email=%s and password=%s")    

        cursor.execute(query,(email,password))
        user=False
        for item in cursor:
            user= User(item[0],item[1],item[2],item[3],item[4],generate_password_hash(item[5], method='pbkdf2:sha256'))

        #user = User.query.filter_by(email=email).first()
        if user:
            print(user.password)
            print(password)
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                user.is_active=True
                login_user(user, remember=True)
                user.is_authenticated=True
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfuly logged out")
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        cnx = mysql.connector.connect(user='root', password='Iu7#01kp',database='massfoodies')
        cursor = cnx.cursor()
        query = ("select * from massfoodies.accounts where name=%s or email=%s")    

        cursor.execute(query,(name,email))
        user=False
        for item in cursor:
            user= User(item[0],item[1],item[2],item[3],item[4],generate_password_hash(item[5], method='pbkdf2:sha256'))

        #user = User.query.filter_by(email=email).first()
        if user:
            flash('Email or name already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            query= ("Select MAX(id) AS id from massfoodies.accounts")
            cursor.execute(query)
            maxid=False
            for item in cursor:
                maxid=item[0]
            print(maxid)
            #new_user = User(email=email, name=name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            new_user = User(maxid+1,name,email,0,"none",password1)
            
            query=("Insert into massfoodies.accounts " "(id, name, email, averageTasteScore, privalge, password)" "VALUES(%s,%s,%s,%s,%s,%s)")
            answer= (str(new_user.id) , new_user.name,new_user.email,str(new_user.averageTasteScore),new_user.privalge,new_user.password)
            cursor.execute(query,answer)
            cnx.commit()
            cnx.close()
            #db.session.add(new_user)
            #db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)




@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        name=request.form.get('accountName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #user = User.query.filter_by(email=email).first()
        cnx = mysql.connector.connect(user=connectUser,password=connectPassword,database="massfoodies")
        cursor=cnx.cursor()
        user=False
        query="Select * from massfoodies.accounts where email=%s and name=%s"
        cursor.execute(query,(email,name))
        for item in cursor:
            user= User(item[0],item[1],item[2],item[3],item[4],item[5])
        if user:
            if password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 7:
                flash('Password must be at least 7 characters.', category='error')
            else:
                #msg=EmailMessage()
                #msg.set_content(user.password)
                #msg['subject']="password"
                #msg['From'] = "massfoodies02@gmail.com"
                #msg['To']=user.email
                #msg.set_content(user.password)
                #s= smtplib.SMTP('localhost')
                #s.send_message("massfoodies02@gmail.com",[user.email],msg.as_string())
                #s.quit()
                
                query= "UPDATE massfoodies.accounts SET password=%s where email=%s"
                cursor.execute(query,(password1,email))
                cnx.commit()
                cursor.close()
                cnx.close
                #user.password=generate_password_hash(password1, method='pbkdf2:sha256')
                #db.session.commit()
                flash('Password Updated!', category='success')
                return redirect(url_for('views.home'))
        else:
            flash('Email or Name does not exist.', category='error')

    return render_template("forgot_password.html", user=current_user)




@auth.route('/add-ingredients', methods=['GET', 'POST'])
def add_ingredients():
    if request.method == 'POST':
        recipeName = request.form.get('recipeName')
        ingredientName = request.form.get('ingredientName')
        unit = request.form.get('unit')
        amount = request.form.get('amount')



        #course = Course.query.filter_by(recipeName=recipeName).first()

        #if course and course.userID != current_user.id:
            #flash('You do not own this recipe.', category='error')

        #elif course:
            #if len(ingredientName) < 4:
                #flash('The ingredient\'s name must be greater than 3 characters.', category='error')
            #elif len(unit) < 1:
                #flash('The type of unit must be greater than 1 character.', category='error')
            #elif len(amount) < 1:
                #flash('The amount of the ingredient must be greater than 1 character.', category='error')
            #else:
                #new_ingredient = [[ingredientName, unit, amount]]
                #course.ingredients.extend(new_ingredient)

                #new_ingredient = Ingredient(recipeID=course.id, ingredientName=ingredientName, unit=unit, amount=amount)
                #db.session.add(new_ingredient) #adding the note to the database 
                #db.session.commit()
                #flash('New ingredient added!', category='success')
                #return render_template("add_ingredients.html", user=current_user)

    return render_template("add_ingredients.html", user=current_user)


@auth.route('/search', methods=['GET','POST'])
def search():
    temp = []
    authorNames=[]
    if request.method == 'POST':
        searchWord=request.form.get('searchWord')
        if searchWord:
            searchWord="%"+searchWord+"%"
        print(searchWord)
        print(request.form.get('searchWor'))
        cnx = mysql.connector.connect(user='root',password='Iu7#01kp',database='massfoodies')
        cursor= cnx.cursor(buffered=True)
        query = ("Select * from massfoodies.recipes where recipeTitle like %s or recipeTags like %s")
        cursor.execute(query,(searchWord,searchWord))
        counter=0
        for (item) in cursor:
            if counter<=10:
                #templist=item[4].split()
                templist=item[4]
                tempListIng=item[3]
                maxlength=150
                if len(templist)>maxlength:
                    templist=templist[:maxlength]
                    middleMan=templist.split("|")
                    templist="".join(middleMan[:len(middleMan)])
                    templist=templist+"..."
                if len(tempListIng)>maxlength:
                    tempListIng=tempListIng[:maxlength]
                    middleMan=tempListIng.split("|")
                    tempListIng="".join(middleMan[:len(middleMan)])
                    tempListIng=tempListIng+"..."
                recipe = Recipes(item[0],item[1],item[2],tempListIng,templist,item[5],item[6],item[7],item[8])
                temp.append(recipe)
                counter+=1
        query= ("Select * from massfoodies.accounts where id =%s")
        for x in range(len(temp)):
            whyList=[temp[x].authorid]
            cursor.execute(query,whyList)
            for item in cursor:
                temp[x].authorid=item[1]
                if item[1] not in authorNames:
                    authorNames.append(item[1])
        cursor.close()
        cnx.close()
    
        
    return render_template("search.html", user=current_user, recipeList=temp, authorList=authorNames)

@auth.route('/viewRecipe', methods=['GET','POST'])
def viewRecipe(test=0):
    print(test)
    searchWord=request.values.get('recipeId')
    if not searchWord:
        searchWord=str(test)
    temp=[]
    cnx = mysql.connector.connect(user='root', password='Iu7#01kp',database='massfoodies')
    cursor = cnx.cursor()
    query = ("select * from massfoodies.recipes where id=%s")
    cursor.execute(query,(searchWord,))
    for item in cursor:
        #templist=item[4].split(".")
        tempList=item[4]
        tempList=tempList[:len(tempList)]
        tempIng=item[3]
        tempIng=tempIng[:len(tempIng)-1]
        recipe= Recipes(item[0],item[1],item[2],tempIng,tempList,item[5],item[6],item[7],item[8])
        temp.append(recipe)
    if (request.method=="POST"):
        if (request.form.get("score")):
            oldScore=0
            oldreview=0
            query = ("select tasteScore from massfoodies.recipes where id=%s")
            tempList2=[temp[0].id]
            cursor.execute(query,tempList2)
            for item in cursor:
                oldScore=int(item[0])
            query=("select numberOfScores from massfoodies.recipes where id=%s")
            cursor.execute(query,tempList2)
            for item in cursor:
                oldreview=int(item[0])
            oldreview += 1
            oldScore=oldScore+int(request.form.get("score"))
            recipe.numOfScore=oldreview
            recipe.Score=oldScore
            query= ("update massfoodies.recipes set tasteScore=%s, numberOfScores=%s where id=%s")
            cursor.execute(query,(oldScore,oldreview,temp[0].id))
    if len(temp)>0:
        query= ("Select * from massfoodies.accounts where id =%s")
        tempList2=[temp[0].authorid]
        cursor.execute(query,tempList2)
        for item in cursor:
            temp[0].authorid=item[1]
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template("viewRecipe.html",user=current_user,viewrecipe=temp)

@auth.route('/viewAccount', methods=['GET','POST'])
def viewAccount(test=0):
    accountId=request.values.get('accountId')
    print(test,accountId)
    if not accountId:
        accountId=test
    temp=[]
    averageScore=0
    numOfScoresers=0
    print(accountId)
    cnx=mysql.connector.connect(user=connectUser, password=connectPassword, database='massfoodies')
    cursor=cnx.cursor()
    query=("select * from massfoodies.accounts where name=%s")
    cursor.execute(query,(accountId,))
    for item in cursor:
            account=User(item[0],item[1],item[2],item[3],item[4],item[5])
            accountId=str(item[0])
            temp.append(account)
    recipeList=[]
    if request.values.get('searchType'):
        print("the user would like a search perface")
        if request.values.get('searchType')=='date':
            print("user wants a data")
            query=("select * from massfoodies.recipes where authorId=%s order by id desc")
        elif request.values.get('searchType')=='score':
            query=("select * from massfoodies.recipes where authorId=%s order by tasteScore asc")
        elif request.values.get('searchType') == 'tags':
            query = ("select * from massfoodies.recipes where authorId=%s order by recipeTags")
    else:
        query=("select * from massfoodies.recipes where authorId=%s")
    cursor.execute(query,(accountId,))
    for item in cursor:
            recipe=Recipes(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8])
            recipeList.append(recipe)
            averageScore=averageScore+item[7]
            numOfScoresers=numOfScoresers+item[8]
    cursor.close()
    cnx.close()
    return render_template("viewAccount.html",user=current_user,viewaccount=temp, listRecipe=recipeList, score=averageScore, numOfScore=numOfScoresers)

@auth.route('/createRecipe', methods=['GET','POST'])
def createRecipe(ingList="", insList="",title="",tags="",count=""):
    
    if request.form.get('existingList'):
        tempIngreidentsList=request.form.get('existingList')
    elif ingList and ingList!="":
        tempIngreidentsList=ingList
    else:
        tempIngreidentsList=""
    if request.form.get('existingInstructions'):
        tempINstructionsList=request.form.get("existingInstructions")
    elif insList and insList!="":
        tempINstructionsList=insList
    else:
        tempINstructionsList=""
    if request.form.get('currTitle'):
        currTitle=request.form.get('currTitle')
    elif title and title!="":
        currTitle=title
    else:
        currTitle=""
    if request.form.get('currTags'):
        currTags=request.form.get('currTags')
    elif tags and tags!="":
        currTags=tags
    else:
        currTags=""
    if request.form.get('counter') and request.form.get('counter') !="temp.jpg":
        counter=request.form.get('counter')
    elif count and count!="":
        counter=count
    else:
        cnx = mysql.connector.connect(user=connectUser, password=connectPassword, database="massfoodies")
        cursor= cnx.cursor()
        query= ("Select MAX(id) AS id from massfoodies.recipes")
        cursor.execute(query)
        fileName=0
        for item in cursor:
            counter=str(int(item[0])+1)
        counter=counter+".jpg"
        if os.path.exists(os.path.join(appS.static_folder, counter)) and not (tempIngreidentsList=="" and tempINstructionsList=="" and currTitle=="" and currTags==""):
            print("the file exist")
            os.remove(os.path.join(appS.static_folder,counter))
            counter="temp.jpg"
        else:
            counter="temp.jpg"
    if request.method=='POST':
        if (request.form.get("addINgriendt")):
            if not request.form.get("size") or request.form.get("size")=="none":
                size=""
            else:
                size=request.form.get("size")+" of"
            tempIngreidentsList=tempIngreidentsList +" "+ request.form.get("ingrientQuanity") +" "+ size+" " +request.form.get("addINgriendt")+"|"
        if (request.form.get("instructions")):
            tempINstructionsList=tempINstructionsList + " "+request.form.get("instructions")+"|"
        if (request.form.get('recipeTitle')):
            currTitle=request.form.get('recipeTitle')
        if (request.form.get('tags')):
            currTags=currTags+" "+request.form.get('tags')+" "
        if(request.form.get('fileCheck') and request.files['file']):
            test=request.files['file']
            cnx = mysql.connector.connect(user=connectUser, password=connectPassword, database='massfoodies')
            cursor= cnx.cursor()
            query= ("Select MAX(id) AS id from massfoodies.recipes")
            cursor.execute(query)
            fileName=0
            for item in cursor:
                fileName=str(int(item[0])+1)
            fileName=fileName+".jpg"
            counter=fileName
            print("Are we getting here")
            test.save(os.path.join('website/static/', fileName))
        if(request.form.get('deleteValueTag')):
            tagArray=(request.form.get('currTags')).split(',')
            if (len(tagArray)>2):
                temp=request.form.get('deleteValueTag')
                if temp in tagArray:
                    tagArray.remove(temp)
                currTags=",".join(tagArray)
            else:
                currTags=""
        if(request.form.get("deleteValueIng")):
            ingArray=(request.form.get('existingList')).split(',')
            if(len(ingArray)>2):
                temp=request.form.get('deleteValueIng')
                if temp in ingArray:
                    ingArray.remove(temp)
                tempIngreidentsList=",".join(ingArray)
            else:
                tempIngreidentsList=""
        if(request.form.get("deleteValueIns")):
            insArray=(request.form.get('existingInstructions')).split('|')
            print(insArray)
            if(len(insArray)>2):
                temp=request.form.get('deleteValueIns')
                print(temp)
                if temp in insArray:
                    print(temp)
                    insArray.remove(temp)
                tempINstructionsList="|".join(insArray)
            else:
                tempINstructionsList=""
    elif request.method=='GET':
        title=request.args.get('currTitl')
        tags=request.args.get('currTag')
        insList=request.args.get('existingInstruction')
        ingList=request.args.get('existingLis')
        counter=request.args.get('counte')
        if insList=="None" or insList==None:
            insList=""
        if ingList=="None" or ingList==None:
            ingList=""
        if counter=="None" or not counter:
            counter="temp.jpg"
        if tags=="None" or not tags :
            print("al")
            tags=""
        if title=="None" or title==None:
            title=""
        if not title or title=="" or title=="None":
            flash("Please add a title")
            return render_template("createRecipe.html", user=current_user, IngredientList=ingList, instructionList=insList, counter=counter,currTitle="",currTags=tags)
        elif not ingList or ingList=="" or ingList=="None":
            flash("PLease add a ingridents")
            return render_template("createRecipe.html", user=current_user, IngredientList="", instructionList=insList, counter=counter,currTitle=title,currTags=tags)
        elif not insList or insList=="" or insList=="None":
            flash("Please add a instruction")
            return render_template("createRecipe.html", user=current_user, IngredientList=ingList, instructionList="", counter=counter,currTitle=title,currTags=tags)
        elif not counter or counter=="temp.jpg":
            flash("Please add a image")
            return render_template("createRecipe.html", user=current_user, IngredientList=ingList, instructionList=insList, counter=counter,currTitle=title,currTags=tags)
        else:
            print("i amd desperate")
            return uploadRecipe(ingList,insList,title,counter,tags)
            #return viewRecipe(displayNum)
    print("are we getting here, loser", request.method)
    return render_template("createRecipe.html", user=current_user, IngredientList=tempIngreidentsList, instructionList=tempINstructionsList, counter=counter,currTitle=currTitle,currTags=currTags)

@auth.route('/editRecipe', methods=['GET','POST'])
def editRecipe():
    if request.method=="POST":
    
        if request.form.get('recipe'):
            temp=request.form.get('recipe')
            cnx =mysql.connector.connect(user=connectUser, password=connectPassword, database="massfoodies")
            cursor= cnx.cursor()
            querry = ("select * from massfoodies.recipes where id=%s")
            cursor.execute(querry,(temp,))
            for item in cursor:
                recipe=Recipes(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8])
            #return render_template("createRecipe.html", user=current_user, IngredientList=tempIngreidentsList,
            #instructionList=tempINstructionsList, counter=counter,currTitle=currTitle,currTags=currTags)
            return render_template("editRecipe.html",user=current_user, id=temp,IngredientList=recipe.ingredient,instructionList=recipe.instructions,counter=recipe.imgPath,currTitle=recipe.recipeTitle,currTags=recipe.recipeTags)
        else:
            if request.form.get('existingList'):
                tempIngreidentsList=request.form.get('existingList')
            else:
                tempIngreidentsList=""
            if request.form.get('existingInstructions'):
                tempINstructionsList=request.form.get("existingInstructions")
            else:
                tempINstructionsList=""
            if request.form.get('currTitle'):
                currTitle=request.form.get('currTitle')
            else:
                currTitle=""
            if request.form.get('currTags'):
                currTags=request.form.get('currTags')
            else:
                currTags=""
            if request.form.get('recipeId'):
                idTemp=request.form.get('recipeId')
            else:
                print(request.form.get('recipeId'), "i need an identifyer")
            if request.form.get('counter') and request.form.get('counter') !="temp.jpg":
                counter=request.form.get('counter')
            else:
                cnx = mysql.connector.connect(user=connectUser, password=connectPassword, database="massfoodies")
                cursor= cnx.cursor()
                query= ("Select MAX(id) AS id from massfoodies.recipes")
                cursor.execute(query)
                fileName=0
                for item in cursor:
                    counter=str(int(item[0])+1)
                counter=counter+".jpg"
                if os.path.exists(os.path.join(appS.static_folder, counter)) and not (tempIngreidentsList=="" and tempINstructionsList=="" and currTitle=="" and currTags==""):
                    print("the file exist")
                    os.remove(os.path.join(appS.static_folder,counter))
                    counter="temp.jpg"
                else:
                    print("the file does not exist")
                    counter="temp.jpg"
            if (request.form.get("addINgriendt")):
                if not request.form.get("size") or request.form.get("size")=="none":
                    size=""
                else:
                    size=request.form.get("size")+" of"
                tempIngreidentsList=tempIngreidentsList +" "+ request.form.get("ingrientQuanity") +" "+ size+" " +request.form.get("addINgriendt")+"|"
            if (request.form.get("instructions")):
                tempINstructionsList=tempINstructionsList + " "+request.form.get("instructions")+"|"
            if (request.form.get('recipeTitle')):
                currTitle=request.form.get('recipeTitle')
            if (request.form.get('tags')):
                currTags=currTags+" "+request.form.get('tags')+","
            if(request.form.get('fileCheck') and request.files['file']):
                test=request.files['file']
                cnx = mysql.connector.connect(user=connectUser, password=connectPassword, database='massfoodies')
                cursor= cnx.cursor()
                query= ("Select MAX(id) AS id from massfoodies.recipes")
                cursor.execute(query)
                fileName=0
                for item in cursor:
                    fileName=str(int(item[0])+1)
                fileName=fileName+".jpg"
                counter=fileName
                test.save(os.path.join('website/static/', fileName))
            if(request.form.get('deleteValueTag')):
                tagArray=(request.form.get('currTags')).split(',')
                if (len(tagArray)>2):
                    temp=request.form.get('deleteValueTag')
                    if temp in tagArray:
                        tagArray.remove(temp)
                    currTags=",".join(tagArray)
                else:
                    currTags=""
            if(request.form.get("deleteValueIng")):
                ingArray=(request.form.get('existingList')).split(',')
                if(len(ingArray)>2):
                    temp=request.form.get('deleteValueIng')
                    if temp in ingArray:
                        ingArray.remove(temp)
                    tempIngreidentsList="|".join(ingArray)
                else:
                    tempIngreidentsList=""
            if(request.form.get("deleteValueIns")):
                insArray=(request.form.get('existingInstructions')).split('|')
                print(insArray)
                if(len(insArray)>2):
                    temp=request.form.get('deleteValueIns')
                    print(temp)
                    if temp in insArray:
                        print(temp)
                        insArray.remove(temp)
                    tempINstructionsList="|".join(insArray)
                else:
                    tempINstructionsList=""
        return render_template("editRecipe.html", user=current_user, id=idTemp,IngredientList=tempIngreidentsList, instructionList=tempINstructionsList, counter=counter,currTitle=currTitle,currTags=currTags) 
    elif request.method=="GET":
        title=request.args.get("currTitl")
        if not title:
            title=""
        tags=request.args.get("currTag")
        if not tags:
            tags=""
        instructions=request.args.get("existingInstruction")
        if not instructions:
            instructions=""
        ingridents=request.args.get("existingLis")
        if not ingridents:
            ingridents=""
        if request.args.get("id"):
            idTemp=request.args.get("id")
        counter=request.args.get("counter")
        if not title:
            counter="temp.jpg"
        if title=="":
            flash("Please add a title")
            return render_template("editRecipe.html", user=current_user,id=idTemp ,IngredientList=tempIngreidentsList, instructionList=tempINstructionsList, counter=counter,currTitle=currTitle,currTags=currTags)
        elif instructions=="":
            flash("Please add a instruction")
            return render_template("editRecipe.html", user=current_user, id=idTemp ,IngredientList=tempIngreidentsList, instructionList=tempINstructionsList, counter=counter,currTitle=currTitle,currTags=currTags)
        elif ingridents=="":
            flash("Please add a ingrident")
            return render_template("editRecipe.html", user=current_user, id=idTemp ,IngredientList=tempIngreidentsList, instructionList=tempINstructionsList, counter=counter,currTitle=currTitle,currTags=currTags)
        elif counter=="temp.jpg":
            flash("Please add a image (it must be a jpg)")
            return render_template("editRecipe.html", user=current_user, id=idTemp ,IngredientList=tempIngreidentsList, instructionList=tempINstructionsList, counter=counter,currTitle=currTitle,currTags=currTags)
        else:
            return updateRecipe(ingList=ingridents, insList=instructions, title=title, counter=counter,tags=tags)
@auth.route('/uploadRecipe', methods=['GET','POST'])
def uploadRecipe(ingList, insList,title,counter,tags):
    cost='0'
    cnx = mysql.connector.connect(user=connectUser, password=connectPassword, database='massfoodies')
    cursor= cnx.cursor()
    query= ("Select MAX(id) AS id from massfoodies.recipes")
    cursor.execute(query)
    currId=0
    for item in cursor:
        currId=item[0]
        currId=int(currId)+1

    query = ("INSERT INTO recipes " "(id, recipeTags, recipeTitle, ingreidents, instructions, authorId, cost, tasteScore, numberOfScores)" "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    
    answer=(currId, tags,title,ingList,insList,current_user.id,cost,'5','1')
    cursor.execute(query,answer)
    cnx.commit()
    cursor.close()
    cnx.close()
    return viewRecipe(currId)
    return createRecipe()

    #return render_template("createRecipe.html",user=current_user)
    #return render_template("home.html",user=current_user)

@auth.route('/updateRecipe', methods=['GET','POST'])
def updateRecipe():
    title=request.values.get("currTitl") 
    tags=request.values.get("currTag")
    instructions=request.values.get("existingInstruction")
    ingridents=request.values.get("existingLis")
    counter=request.values.get("counte")
    id=request.values.get("recipeId")
    cnx = mysql.connector.connect(user=connectUser, password=connectPassword, database='massfoodies')
    cursor= cnx.cursor()
    if (title==""):
        flash("Please add a title")
        return render_template("editRecipe.html", user=current_user, IngredientList=ingridents, instructionList=instructions, counter=counter,currTitle=title,currTags=tags)
    elif (instructions==""):
        flash("Please add a instruction")
        return render_template("editRecipe.html", user=current_user, IngredientList=ingridents, instructionList=instructions, counter=counter,currTitle=title,currTags=tags)
    elif (ingridents==""):
        flash("Please add a ingrident")
        return render_template("editRecipe.html", user=current_user, IngredientList=ingridents, instructionList=instructions, counter=counter,currTitle=title,currTags=tags)
    
    print(id, " lmao it tape ",counter)
    if counter.split()[0]!=id:
        print("Do we get here at al")
        temp=str(id)+".jpg"
        print(temp, " breal ",counter)
        #os.replace((os.path.join(app.static_folder,temp)),(os.path.join(app.static_folder, counter)))
        os.replace((os.path.join(appS.static_folder,counter)),(os.path.join(appS.static_folder, temp)))
    #we still need to do image update
    query = (" update massfoodies.recipes set recipeTags=%s, recipeTitle=%s, ingreidents=%s, instructions=%s where id=%s")
    answer=(tags,title,ingridents,instructions,id)
    cursor.execute(query,answer)
    cnx.commit()
    cursor.close()
    cnx.close()
    return viewRecipe(id)
    return createRecipe()


@auth.route('/deleteRecipe', methods=['GET','POST'])
def deleteRecipe():
    maxid=0
    id=request.values.get("recipeId")
    accountId=request.values.get("accountI")
    path=id+".jpg"
    deleteFile=True
    cnx=mysql.connector.connect(user=connectUser,password=connectPassword,database="massfoodies")
    cursor=cnx.cursor()
    query=("SELECT * from massfoodies.accounts where id=%s")
    cursor.execute(query,(accountId,))
    temp=""
    for item in cursor:
        temp=item[1]
    query= ("Select MAX(id) AS id from massfoodies.recipes")
    cursor.execute(query)
    for item in cursor:
        maxid=item[0]
    query=("DELETE from massfoodies.recipes where id=%s")
    cursor.execute(query,(id,))
    for i in range(int(id)+1,int(maxid)+1):
        tempI=i
        print("do we do anything", i)
        oldPath=str(tempI)+".jpg"
        newPath=str(tempI-1)+".jpg"
        print("we should repalceing %s with %s", oldPath,newPath)
        os.replace (os.path.join(appS.static_folder,oldPath),os.path.join(appS.static_folder,newPath))
        query=("UPDATE massfoodies.recipes SET id=%s where id=%s")
        cursor.execute(query,(i-1,i))
        deleteFile=False
    if deleteFile:
        if os.path.exists(os.path.join(appS.static_folder,path)):
            os.remove(os.path.join(appS.static_folder, path))
    cnx.commit()
    cursor.close()
    cnx.close()
    return viewAccount(temp)

@auth.route('/updateAccount', methods=['GET','POST'])
def updateAccount():
    if request.method=="POST":
        id = request.form.get('id')
        cnx= mysql.connector.connect(user=connectUser,password=connectPassword,database="massfoodies")
        cursor = cnx.cursor()
        if request.form.get('userName'):
            userNameExists=False
            query = "select * from massfoodies.accounts where name=%s"
            cursor.execute(query,(request.form.get('userName'),))
            for item in cursor:
                userNameExists=True
            if not userNameExists:
                print(id)
                query="update massfoodies.accounts set name=%s where id=%s"
                cursor.execute(query,(request.form.get('userName'),id))
                cnx.commit()
                flash("Your Name has been updated")
            else:
                flash("That name is already taken") 
        elif request.form.get("email"):
            emailExists=False
            query=("select * from massfoodies.accounts where email=%s")
            cursor.execute(query,(request.form.get('email'),))
            for item in cursor:
                emailExists=True
            if not emailExists:
                query = ("update massfoodies.accounts set email=%s where id=%s")
                cursor.execute(query,(request.form.get('email'),id))
                cnx.commit()
                flash("Your email has been updated")
            else:
                flash("that email is already inuse")
        elif request.form.get('password') and request.form.get('oldPassword'):
            passwordCorrect=False
            query = ("select * from massfoodies.accounts where password =%s and id=%s")
            cursor.execute(query,(request.form.get('oldPassword'),id))
            for item in cursor:
                passwordCorrect=True
            if passwordCorrect:
                query=("update massfoodies.accounts set password=%s where id=%s")
                cursor.execute(query,(request.form.get('password'),id))
                cnx.commit()
                flash("Your password has been updated")
            else:
                flash("That is not your existing password")
        cursor.close()
        cnx.close()
    return render_template('updateAccount.html',user=current_user)