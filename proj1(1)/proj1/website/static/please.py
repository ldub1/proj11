#mysql api
import mysql.connector
from mysql.connector import errorcode
#all recipes api
import allrecipes
from allrecipes import AllRecipes
#for the images
import os
import requests

#getting id, could change to be more efficet with max
cnx = mysql.connector.connect(user='root', password='Iu7#01kp',database='massfoodies')
cursor = cnx.cursor()

query = ("select * from massfoodies.recipes order by id Desc limit 1;")
num=0
cursor.execute(query)
for (item) in cursor:
	num=item[0]
	num=num+1
print(num)
query = ("INSERT INTO recipes " "(id, recipeTags, recipeTitle, ingreidents, instructions, authorId, cost, tasteScore, numberOfScores)" "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")

# Search:
search_string = "ham" # Query
query_result = AllRecipes.search(search_string)

for i in range(5):
	print(query_result[i]['name'])
	temp = query_result[i]['url']
	print(temp)
	test = AllRecipes.get(temp)
	print(test['ingredients'])
	list = '|'.join(str(x) for x in test['ingredients'])
	steps_list= '|'.join(str(x) for x in test['steps'])

	name=''.join(str(x) for x in query_result[i]['name'])
	image= query_result[i]['image']
	print(image)
	image=str(image)
	image_data=requests.get(image).content
	imagePath=str(num)+".jpg"
	with open(imagePath,'wb') as f:
		f.write(image_data)
	answer = (num,'ham ',name,list,steps_list,'0','10','5','1')
	num=num+1
	cursor.execute(query,answer)
	

cnx.commit()

cursor.close()
cnx.close()