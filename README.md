# HabitTracker

At first you have to download the Django-CLI. Please follow instructions on this here: https://docs.djangoproject.com/en/3.1/howto/windows/

 <br />
 
 
 **Other technologies used**

• Database: SQLite

• Styling: Bootstrap

 <br />
 
 
 **How to run the HabitTracker on your machine**
 

In order to populate the database from the pre-provided data run: 

•	python manage.py loaddata fixtures


In order to create an admin user for the DB with all rights run:

• python manage.py createsuperuser


 <br />
 
 
 

**Models**

In Django models are Python classes which inherit from Django models. And allow us to create classes that represent database tables. 

*Migrations* 

Every time the model is changed and the database changes the following commands need to be run:

•	python manage.py makemigrations


This creates a Migration File in the Migration Folder. This is like preparing the database for the migration we are about to run. In the background it will run SQL commands. Then we run the command to actually migrate the data. The command goes as follows: 


•	python manage.py migrate

This command adds the table to the database. 


Now we run the server with the following command:

•	python manage.py runserver


In the admin panel this table cannot be seen yet. That table needs to be registered with the admin table. This is done by 

1.	Open the admin.py file 
2.	Import the new models with from .models import *     admin.site.register(NameOfModel)
From now on it can be seen on the database on the admin panel. 

*Deleting the Database*

If you want to delete the entire Database (careful, it will also flush away the user including the main developer) via the console type the following command:

• python manage.py flush

 <br />

**Relationships**

One to Many relationships: User to habit relationship  => One user many habits. 
In the admin panel it will give you the choice to only chose one item. 

 <br />

*Many to many relationships:*

For a many to many relationship another table, like an intermediary table, needs to be created. This stores the id-reference to both tables. Django creates that for you. You just need to add models.ForeignKey(parentOfModel)  
In Django there is the possibility to set models.ManyToManyField(NameToFieldForRelationShip) 
The ManyToManyField allowes us to associate different things from different tables.
Many-to-on relationships are done with the foreign-key

 <br />


**Query the data from command prompt**

To query data from the command prompt run the command:
• python manage.py shell



If you want to query for example all habits than you would write into the command prompt:

• from crm.models import *


if you want the last habit in the order than the command would look like this:

• lastHabit = Order.objects.last()
  print(lastHabit)
  
  
From here we can access all the attributes by using the dot-notation. 
print(lastHabit.name)


You can also search a specific item by id, like this: 

• habit1=Order.objects.get(id=1) 


If you use filter without specificing it, it works like .all() 

• habits = Order.objects.filter()

print(habits)


So the .filter() in this way like above would just return all habits. 
However if you had set choices than you can actually query those categories like so:

• habits = Order.objects.filter(category = "Family")

  print(habits)
  
  
This will then only query habits which fall under the category “Family”.
If you want to query many to many realtionships

 <br />

**Defs**

Defs in Views are basically the functions you do on the models.

 <br />

**Unit Tests**

By default Django adds a tests.py file to a new project. 
The way that tests are detected is that Django starts looking for a file which starts with "test". Then it looks for classes which also start with Test. 
To run the test you need to type the command 

•	py.test



For testing I installed

•	pytest 

•	pytest-django

•	pytest-cov

•	mixer 



