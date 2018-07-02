from flask import Flask
import xlrd
from flask_admin import Admin
from mongoengine import *
from flask_mongoengine import MongoEngine
from flask_admin.contrib.mongoengine import ModelView
from models import AromaCompound, Ingredient, IngredientForm, CookingStyle, TasteCompound, IngredientCompoundRelation


app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MONGODB_SETTINGS'] = {
    'db': 'dishq',
    'host': 'mongodb://127.0.0.1:27017/dishq'
}
admin = Admin(app, name='inground', template_mode='bootstrap3')
db = connect('dishq')
admin.add_view(ModelView(AromaCompound))
admin.add_view(ModelView(Ingredient))
admin.add_view(ModelView(IngredientForm))
admin.add_view(ModelView(CookingStyle))
admin.add_view(ModelView(TasteCompound))
admin.add_view(ModelView(IngredientCompoundRelation))


@app.route('/')
def initialize():
	dishq_data_book = xlrd.open_workbook('ingredientforms.xlsx')
	ingredient_sheet = dishq_data_book.sheet_by_index(0)
	for i in range(1,57):
		ingredient = IngredientForm(ingredient_form_id=str(ingredient_sheet.cell(i,0).value),
								ingredient_form_name=str(ingredient_sheet.cell(i,1).value))
		ingredient.save()
	return "Hello"

if __name__ == '__main__':
   app.run()