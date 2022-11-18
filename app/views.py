import os
from pathlib import Path
import sqlite3
import sqlalchemy
from sqlalchemy import or_, and_
from app import app
from app import db
from app.models import Dish, Ingredient, DishIngredients, IngredientCategory
from flask import render_template, redirect, request, session, abort, send_from_directory, jsonify
from datetime import datetime, timedelta, timezone
import json


import string

# returns all food categories
@app.route('/ingredient_categories')
def get_categories():
    categories = IngredientCategory.query.all()
    print(categories)
    json_categories = {}
    for c in categories:
        json_categories[c.id] = { 'id': c.id, 'name': c.name }
        
    return json.dumps(json_categories)

# returns all ingredients
@app.route('/ingredients')
def get_ingredients():
    ingredients = Ingredient.query.all()
    json_ingr = {}
    for i in ingredients:
        json_ingr[i.id] = { 'id': i.id, 'name': i.name }
        
    return json.dumps(json_ingr)

# returns ingredients from specified category
@app.route('/ingredients/<category>')
def get_categorys_ingredients(category):
    cat_id = IngredientCategory.query.filter_by(name=category).first().id
    ingredients = Ingredient.query.filter_by(category=cat_id).all()

    json_ingr = {}
    json_ingr['ingredients'] = []

    for i in ingredients:
        json_ingr['ingredients'].append({ 'id': i.id, 'name': i.name })
        
    response = jsonify(json_ingr)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

# returns dishes that contain user's ingredients 
@app.route('/dishes<ingredients>')
def get_dishes():
    pass

# returns dishes that contain user's ingredients 
@app.route('/addUser')
def add_user():
    pass