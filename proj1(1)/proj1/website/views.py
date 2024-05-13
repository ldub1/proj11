from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Recipes
import json
import mysql.connector
import numpy as np
import random


views = Blueprint('views', __name__)
connectUser='root'
connectPassword='Iu7#01kp'

@views.route('/', methods=['GET', 'POST'])
#@login_required
def home():

    return homePage()
    #return render_template("home.html",user=current_user)
    #return render_template("add_course.html", user=current_user)

@views.route('/homePage')
def homePage():
    randomRecipes=[]
    listOfRandomNum=[]
    listofTags=[]
    cnx = mysql.connector.connect(user=connectUser,password=connectPassword,database="massfoodies")
    cursor= cnx.cursor()
    temp=""
    query=("select recipeTags from massfoodies.recipes")
    cursor.execute(query)
    for item in cursor:
        for i in item:
            temp=temp + str(i)

    temp=temp.split()
    numberOfTags=15
    for i in range(len(temp)):
        if temp[i] not in listofTags and temp[i] !="'',":
            listofTags.append(temp[i])
    np.random.shuffle(listofTags)
    listofTags=listofTags[:numberOfTags]

    query= ("Select MAX(id) AS id from massfoodies.recipes")
    maxId=0
    cursor.execute(query)
    for item in cursor:
        maxId=item[0]
    query = ("select * from massfoodies.recipes where id=%s or id=%s or id=%s or id=%s or id=%s or id=%s or id=%s or id=%s or id=%s or id=%s  or id=%s or id=%s or id=%s or id=%s or id=%s or id=%s")
    while len(listOfRandomNum)<16:
        randomInt=random.randint(1,maxId)
        if randomInt not in listOfRandomNum:
            listOfRandomNum.append(randomInt) 
    cursor.execute(query,listOfRandomNum)
    #cursor.execute(query,(random.randint(1,maxId),random.randint(1,maxId)))
    for item in cursor:
        recipe=Recipes(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8])
        randomRecipes.append(recipe)
    cnx.close()

    return render_template("home.html",user=current_user,recipeList=randomRecipes, tagslist=listofTags)