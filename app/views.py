import os
from pathlib import Path
import sqlite3
import sqlalchemy
from sqlalchemy import or_, and_, intersect
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
    json_categories = {}
    json_categories['categories'] = []
    for c in categories:
        json_categories['categories'].append({ 'id': c.id, 'name': c.name })
        
    return json.dumps(json_categories)

# returns all ingredients
@app.route('/ingredients')
def get_ingredients():
    ingredients = Ingredient.query.all()
    json_ingr = {}
    json_ingr['ingredients'] = []
    for i in ingredients:
        json_ingr['ingredients'].append({ 'id': i.id, 'name': i.name }) 
        
    return json.dumps(json_ingr)

# returns ingredients from specified category
@app.route('/ingredients/<category>')
def get_categorys_ingredients(category):
    cat_id = (IngredientCategory.query.filter_by(name=category).first()).id
    ingredients = Ingredient.query.filter_by(category=cat_id).all()

    json_ingr = {}
    json_ingr['ingredients'] = []

    for i in ingredients:
        json_ingr['ingredients'].append({ 'id': i.id, 'name': i.name })
        
    response = jsonify(json_ingr)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

# returns dishes that contain user's ingredients 
@app.route('/dishes', methods=['POST'])
def get_dishes():

    users_ingredients_ids = set() # ids of user's ingredients
    users_ingredients_names = set() # ids of user's ingredients
    json_user_ingr = request.get_json()
    dishes_from_ingredients = {}
    dishes_from_ingredients['dishes'] = []

    # getting ingredients from db specified by user
    for i in json_user_ingr:
        if not json_user_ingr[i] == '...':
            ingredient = (Ingredient.query.filter_by(name=json_user_ingr[i]).first())
            # print(ingredient)
            users_ingredients_ids.add(ingredient.id)
            users_ingredients_names.add(ingredient.name)

    # print(users_ingredients)

    possible_dishes_ids = set()     # possible dishes user can make from the ingredients
    dishes = set()              # stores final set of dishes

    # getting possible dishes' ids
    for i in users_ingredients_ids:
        # getting all dishes that contain ingredient i in form tuples (dish_id, ingredient_id)
        res = db.session.query(DishIngredients).filter_by(ingredient_id=i).all()
        # print(res)
        
        for j in res:
            possible_dishes_ids.add(j[0])

    # checking what ingredients user is missing
    for pd in possible_dishes_ids:

        # SELECT * FROM DishIngredients WHERE dish_id=pd[0]; -- pd[0] is id
        res = db.session.query(DishIngredients).filter_by(dish_id=pd).all()
        ingredients_needed = set()

        # getting ingredients' ids needed for specific dish
        for i in res:
            ingredients_needed.add(i[1])

        # checking if ingredients_needed is subset of users_ingredients
        dish = {}
        dish['name'] = ((db.session.query(Dish).filter_by(id=pd).first()).name).lower()
        dish['missing_ingredients_ids'] = list(ingredients_needed.difference(users_ingredients_ids))
        dish['missing_ingredients_names'] = []

        for mi in dish['missing_ingredients_ids']:
            dish['missing_ingredients_names'].append(((db.session.query(Ingredient).filter_by(id=mi).first()).name).lower())

        dishes_from_ingredients['dishes'].append(dish)

    # print(dishes_from_ingredients)
    return jsonify(dishes_from_ingredients)

# getting all available dishes in db along with ingredients needed for those dishes
@app.route('/all_dishes')
def get_all_dishes():
    dishes = {}
    res = db.session.query(Dish).all()  
    for d in res:
        dishes[d.name] = []
        for i in d.ingredients:
            dishes[d.name].append(i.name)
        

    return jsonify(dishes)



# adding new ingredient
@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():

    try:
        category_id = (db.session.query(IngredientCategory).filter_by(name=request.form.get('category')).first()).id
        ingredient = Ingredient(name=request.form.get('name'), category=category_id)
        db.session.add(ingredient)
        db.session.commit()

        return str('You added: ' + request.form.get('name')) 

    except:
        return 'Invalid ingredient\'s data'

# delete ingredient
@app.route('/delete_ingredient/<ingredient_name>', methods=['DELETE'])
def delete_ingredient(ingredient_name):
    try:
        Ingredient.query.filter_by(name=ingredient_name).delete()
        db.session.commit()

        return 'You just deleted: ' + ingredient_name
    except:
        return 'There is no ingredient with such a name'

# update ingredient
@app.route('/update_ingredient_category', methods=['PUT'])
def update_ingredient():
    try:
        print(request.form)
        ingr_name = request.form.get('name')
        new_cat = request.form.get('new_cat')
        print('new cat ', new_cat)
        print('name ', ingr_name)
        new_cat_id = (IngredientCategory.query.filter_by(name=new_cat).first()).id

        db.session.query(Ingredient).filter_by(name=ingr_name).update({'category': new_cat_id})
        db.session.commit()

        return 'OK'

    except:
        return 'Invalid data'

    