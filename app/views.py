import os
from pathlib import Path
import sqlite3
import sqlalchemy
from sqlalchemy import or_, and_
from app import app
from app import db
from app.models import Dish, Ingredient, DishIngredients, IngredientCategory
from flask import render_template, redirect, request, session, abort, send_from_directory
from datetime import datetime, timedelta, timezone


import string

# returns all food categories
@app.route('/ingredient_categories')
def get_categories():
    print('hello ')

# returns all ingredients
@app.route('/ingredient')
def get_ingredients():
    print('hello ')

# returns ingredients from specified category
@app.route('/ingredient/<category>')
def get_categorys_ingredients():
    print('hello ')

# returns dishes that contain user's ingredients 
@app.route('/dishes')
def get_dishes():
    print('hello ')