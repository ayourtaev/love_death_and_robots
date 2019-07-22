# Robot City Navigation System

### About
That's a little application which provide a navigation city system for the robots.
General features of application are: 

* create a route from file
* give the ability for robots moving forward according to the route
* give the ability to create landmarks
* ability for robots to interact with the landmarks 
* ability to see the list of the routes and landmarks which saved in the database

### Dependencies
General dependencies are:
* python3 ( core platform )
* sqlalchemy ( general library for working with database, sqlite in our case)
* marshmallow ( like a base for future validation)
* asyncio ( for our robots )

for install this and other dependencies: 
```
pip install -r req.txt

```

### How to use it

**manage.py** is a entry point into the application

Try to start with --help
```
python manage.py --help
```

----------------------------

With help of command *--landmark* we can create landmark with any coordinates and any names
that we want, example below.
```
python manage.py --landmark (277,166) "Statue of Old Man with Large Hat"
```

----------------------------
Next command give the ability to load **.txt** file with instructions data.

```
python manage.py --loaddata route_data.txt
```

----------------------------
Command with which we run the robot is very simple:

```
python manage.py --run robot
```

### Routing Specification

**.txt** file

Example: 

```
Start at (100, 100)
Go North 5 blocks
Turn right
Go until you reach landmark 'Statue of Old Man with Large Hat'
Go West 25 blocks
Turn left
Go 3 blocks
```

###How it works

That application is divided into two different parts, first part is responsible for uploading and saving data into database. 
Second part it's actually our robots that take data from the database and handle it. 

Current design was chosen for scaling and competitiveness ability.
In the case of increasing the load on the system, we will be able to balance it as by increasing the instances of the application 
itself and by increasing the number of processes working on the implementation of routes.
 
Current database schema:

![Alt text](http://joxi.net/D2P5N1Oiq8GzZA.png?raw=true "Title")

### Answers

* **A system with millions of routes vs. a system with <100 routes**

* **A system where routes have thousands of instructions each vs. a system where
routes have 1-10 instructions**

Relational database  will be pretty slow with a big Graph that's why i think better use the NoSQL databases.

* **A system with millions of simultaneous users vs. <10 simultaneous users**

Scaling can nerfed that problem, we use Docker containers for that or something new, something
serverless for example. With correct architecture we wont have a problem with often change 
number of users count.

* **A system where routes are frequently changed and updated vs. one where routes are permanent once initially devised**

Updates of the Graph it's not a cheap action. Routes should be a permanent, i think better to create new route 
from the update point, then update previous route.

## Here is what I would like to improve in the current implementation or TODO:

* Change sqlite to postgres with postGIS, that's simple to work with geometry and coordinates.
* Settings or Config file should be added or integration with zookeeper.
* Add validation. 
* Web server will be a good additional for that application. 
* Very strange business logic of landmarks, if we mean a real city, we can integrate Google services.
* A good idea would be to add user feedback, providing the opportunity to influence the route as you go.
* Expansion of instruction dialect, integration with third-party services, public API and other.