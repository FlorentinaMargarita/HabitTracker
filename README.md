# HabitTracker

At first you have to download the Django-CLI. Please follow instructions on this here: https://docs.djangoproject.com/en/3.1/howto/windows/

 <br />
 
 
 **Technologies used**
 
• Language: Python 3.9.1

• Framework: Django 3.1.4

• Database: SQLite3 

• Styling: Bootstrap

• I used the DotEnv package to make this project secure for sharing here on github. In case you want to run the project, just reach out to me and I will provide you the .env file, which I did not share here on github. To use it please install: https://pypi.org/project/python-dotenv/

 <br />
 
 
 **How to run the HabitTracker on your machine**
 

In order to populate the database from the pre-provided data run: 

•	python manage.py loaddata fixtures


In order to create an admin user for the DB with all rights run:

• python manage.py createsuperuser


 <br />
 
 **Folder structure**


• All the relevant functions are in the file: views.py 

• All the testing takes place in the file: tests.py

• There are only two relevant classes for this project. “Repeats” and “Order”: Both of them you will find in the file: models.py

• The configuration of the project is in: settings.py

 

 

**Models**

In Django models are Python classes which inherit from Django models. They allow us to create classes that represent database tables. 

*Migrations* 

Every time the model is changed and the database changes the following command needs to be run:

•	python manage.py makemigrations


This creates a Migration File in the Migration Folder. This is like preparing the database for the migration we are about to run. In the background it will run SQL commands. Then we run the command to actually migrates the data. The command is as follows: 


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

One to Many relationships: In the admin panel it will give you the choice to only chose one item. In this project there are no one to many relationships.

 <br />

*Many to many relationships:*

For a many to many relationship another table, like an intermediary table, needs to be created. This stores the id-reference to both tables. Django creates that for you. You just need to add models.ForeignKey(parentOfModel)  In other words: The ManyToManyField allowes us to associate different things from different tables.

 <br />


**Query the data from command prompt**

To query data from the command prompt run the command:

• python manage.py shell



If you want to query for example all habits than you would write into the command prompt:

• from crm.models import *


if you want the last habit in the order than the command would look like this:

• lastHabit = Order.objects.last()
  print(lastHabit)
  
  
From here we can access all the attributes by using the dot-notation like so:

• print(lastHabit.name)


You can also search a specific item by id, like this: 

• habit1=Order.objects.get(id=1) 


If you use filter without specificing it, it works like .all() 

• habits = Order.objects.filter()

print(habits)


So the .filter() in this way like above would just return all habits. 
However if you had set choices than you can actually query those categories like so:

• habits = Order.objects.filter(inverval = "Daily")

  print(habits)
  
  
This will then only query habits which have an interval of "Daily".

 <br />

**Defs**

Defs in Views are basically the functions you do on the models.

 <br />

**Unit Tests**

By default Django adds a tests.py file to a new project. 
The way that tests are detected is that Django starts looking for a file which starts with "test". Then it looks for classes which also start with Test. 
To run the test you need to type the command 

•	python manage.py test crm



For testing I installed:

•	pytest 

•	pytest-django



**Deployed on Heroku**

To deploy the app on Heroku I used "whitenoise" to "help" Heroku to serve static files. Furthermore I installed Gunicorn, following the instructions given by the Heroku documentation: https://devcenter.heroku.com/articles/deploying-python


