from flask_mongoengine.wtf import model_form
from mongoengine import *
from flask_admin.contrib.mongoengine import ModelView
from flask import abort


class Ingredient(Document):
	ingredient_id = StringField(unique=True)
	ingredient_name = StringField(unique=True)

	def __unicode__(self):
		return self.ingredient_name


class IngredientForm(Document):
	ingredient_form_id = StringField(unique=True)
	ingredient_form_name = StringField(unique=True)

	def __unicode__(self):
		return self.ingredient_form_name


class CookingStyle(Document):
	cooking_style_id = StringField(unique=True)
	cooking_style_name = StringField(unique=True)

	def __unicode__(self):
		return self.cooking_style_name


class AromaCompound(Document):
	compound_id = StringField(unique=True)
	compound_name = StringField(unique=True)
	aroma_description = ListField(StringField())
	threshold_OAV = IntField()
	threshold_FD = IntField()
	characteristics = StringField()
	CAS = StringField()
	source_info = URLField()

	def __unicode__(self):
		return self.compound_name


class TasteCompound(Document):
	compound_id = StringField(unique=True)
	compound_name = StringField(unique=True)
	taste_descriptors = ListField(StringField())
	taste_level = DecimalField()
	CAS = StringField()
	source_info = URLField()

	def __unicode__(self):
		return self.compound_name


class IngredientCompoundRelation(Document):
	ingredient = ReferenceField(Ingredient, required=True)
	aroma_compound = ReferenceField(AromaCompound)
	taste_compound = ReferenceField(TasteCompound)
	quantity = DecimalField()
	cooking_style = ReferenceField(CookingStyle)
	ingredient_form = ReferenceField(IngredientForm)

	def save(self, *args, **kwargs):
		if ((self.aroma_compound is None and self.taste_compound is None) or (self.aroma_compound != None and self.taste_compound != None)):
		 	abort(400 , {'message' : 'Please enter only one of AromaCompound or TasteCompound'})
		else:
			super(IngredientCompoundRelation, self).save(*args, **kwargs)
