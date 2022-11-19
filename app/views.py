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
@app.route('/dishes', methods=['POST'])
def get_dishes():

    users_ingredients_ids = set() # ids of user's ingredients
    users_ingredients_names = set() # ids of user's ingredients
    json_user_ingr = request.get_json()

    # getting ingredients from db specified by user
    for i in json_user_ingr:
        if not json_user_ingr[i] == '...':
            ingredient_id = (Ingredient.query.filter_by(name=json_user_ingr[i]).first())
            print(ingredient_id)
            users_ingredients_ids.add(ingredient_id.id)
            users_ingredients_names.add(ingredient_id.name)

    # print(users_ingredients)

    possible_dishes = set()
    dishes = set()              # stores final set of dishes

    # getting users ingredients ids
    for i in users_ingredients_ids:
        # getting all dishes that contain ingredient i
        res = db.session.query(DishIngredients).filter_by(ingredient_id=i).all()
        print(res)

        # getting dish's id from result's tuple(dish_id, ingredient_id)
        for d in res:
            possible_dishes.add(d[0])

    # checking if user has all ingridients for dishes in possible_dishes 
    for pd in possible_dishes:
        # print(pd)

        # SELECT * FROM DishIngredients WHERE dish_id=pd;
        res = db.session.query(DishIngredients).filter_by(dish_id=pd).all()
        ingredients_needed = set()

        # getting ingredients needed for specific dish
        for i in res:
            ingredients_needed.add(i[1])

        # checking if ingredients_needed is subset of users_ingredients
        if ingredients_needed.issubset(users_ingredients_ids):
            print('is subset: ', pd)
            dishes.add((db.session.query(Dish).filter_by(id=pd).first()).name)

    return jsonify(list(dishes))

@app.route('/all_dishes')
def get_all_dishes():
    dishes = []
    res = db.session.query(Dish).all()  
    for d in res:
        dishes.append(d.name)

    return jsonify(dishes)



# returns dishes that contain user's ingredients 
@app.route('/addUser')
def add_user():
    pass