from flask_login import UserMixin
import os
from flask import Flask

app = Flask(__name__)

class Recipes:
    def __init__(self,Id, RecipeTags, RecipeTitle, Ingreidents, Instructions, AuthorId, Cost, TasteScore,numofScore):
        self.id=Id
        self.cost=Cost
        self.authorid=AuthorId
        self.ingredient=Ingreidents
        self.instructions=Instructions
        self.recipeTags=RecipeTags
        self.recipeTitle=RecipeTitle
        self.Score=TasteScore
        self.numOfScore=numofScore
        test=str(self.id) +'.jpg'
        if os.path.exists(os.path.join(app.static_folder,test)):
            self.imgPath=str(self.id)+'.jpg'
        else:
            self.imgPath="noImage.jpg"

#class User(db.Model, UserMixin):
    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #email = db.Column(db.String(150))
    #name = db.Column(db.String(150))
    #password = db.Column(db.String(150))
    #courses = db.relationship('Course')

class User():
    def __init__(self,id, name, email, averageTasteScore, privalge, password):
        self.id=id
        self.name=name
        self.email=email
        self.averageTasteScore=averageTasteScore
        self.privalge=privalge
        self.password=password
        self.is_active=True 
        self.is_authenticated=True
    def get_id(self):
        return str(self.id)
        

