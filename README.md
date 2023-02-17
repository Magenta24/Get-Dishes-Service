# dist-systems-cw2-service1



### Name of the Web Service: **Get Dishes Service**
### Order in workflow: 1
### Brief description
Firstly, the service returns all the categories and ingredients to the client in order to use them in the form. Used service's endpoints are /ingredient_categories and /ingredients/<category>.
Then after submitting the form, client sends a JSON to the service with ingredients specified by a user in the form. 
The service gets the JSON with user's ingredients and retrieve dishes from the database that contains at least one ingredient from the user's ingredient list.
Afterwards, the dishes are placed in a JSON of form 
```javascript
{
       'dishes':[
                          {
                               'name':dish_name, 
                               'missing_ingredients_ids':[], 
                               'missing_ingredients_names':[]
                           }
                       ]
}
```
  
where key 'dishes' stores list of dictionaries where each dictionary stores single dish that is possible to make.
So, for example if user provided service with only one ingredient - 'Tomato' the returned  JSON will contain dishes like Spaghetti and Chicken with specified missing ingredients under respective keys.

To sum up, there are 9 endpoints that allowt o perform all CRUD operations (GET, POST, PUT, DELETE):
1. **localhost:port_number/ingredient_categories** - GET method that returns json with all ingredient categories
2. **localhost:port_number/ingredients** - GET method that returns JSON with all available ingredients objects
3. **localhost:port_number/ingredients/<category>** - GET method returning specified category's Ingredient objects
4. **localhost:port_number/dishes** - POST method that returns JSON with all dishes that contains at least one ingredient from ingredients specified by client. Additional information for each returned dish are missing_ingredients_ids and missing_ingredients_names
5. **localhost:port_number/all_dishes** - GET method returning JSON with all dishes available and ingredients needed to make specific dish
6. **localhost:port_number/add_ingredient?name=ingredient_name&category=category_name** - POST method that allows to insert a new ingredient to the database
7. **localhost:port_number/delete_ingredient/<ingredient_name>** - DELETE method that deletes an ingredient specified by its name
8. **localhost:port_number/update_ingredient_category?name=name_of_ingredient&new_cat=name_of_new_category_for_previously_specified_ingredient** - PUT method that updates already existing ingredient's category
  
### Server Design/implementation
The service is implemented with Python and Flask. The database engine used is SQLite. Moreover, SQLAlchemy is used to manage the database and as an object-relational mapper. 
All the service logic is stored in app/views.py file.
 
### How service is invoked
To run the service following commands need to be invoked after downloading the source code:

1. Creating new environment
python3 -m venv <name of environment>

2. Activating the environment
source <name of environment>/bin/activate

3. Installing all the needed packages
pip install -r requirements.txt

4. Running the application
flask run -h localhost -p <port_ number>

