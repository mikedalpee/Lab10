import psycopg2
from urllib.parse import urlparse, uses_netloc

############################################################
# This module allows easy use of .ini files
# for configuration data.  You should import this into 
# your own (user interactive) program too.
import configparser
############################################################

############################################################
# We can load the ini file, and find the postgres_connection
# to use.
config = configparser.ConfigParser()
config.read('config.ini')
connection_string = config['database']['postgres_connection']
############################################################

uses_netloc.append("postgres")

##############################################################################
# Now use the connection string found in the ini file to construct the url used
# to connect to the database.
url = urlparse(connection_string)
##############################################################################

def insert_customer(cursor, name):
    ############################################################################################
    # Note that the second parameter is a tuple - and in Python, if you have a tuple with just
    # one item, you need to use a trailing comma - so Python knows its a tuple and not just
    # a value surrounded by parenthesis.  One of the few very unintuitive parts of the Python syntax!
    ############################################################################################
    cursor.execute("insert into Customers (name) values (%s) returning id", (name, ))
    created_id = cursor.fetchone()[0]
    return created_id

def insert_manufacturer(cursor, name):
    cursor.execute("insert into Manufacturers (name) values (%s) returning id", (name, ))
    created_id = cursor.fetchone()[0]
    return created_id

def insert_machine(cursor, model):
    cursor.execute("insert into Machines (modelNumber) values (%s) returning serialNumber", (model, ))
    created_id = cursor.fetchone()[0]
    return created_id

def insert_order(cursor, customer, machine):
    cursor.execute("insert into Orders (customerId, serialNumber) values (%s, %s) returning number", (customer, machine))
    created_id = cursor.fetchone()[0]
    return created_id

def insert_model(cursor, number, speed, ram, hd, price, manufacturerId):
    cursor.execute("insert into Models (id, speed, ram, hd, price, manufacturerId) values (%s, %s, %s, %s, %s, %s) returning id", (number, speed, ram, hd, price, manufacturerId))
    created_id = cursor.fetchone()[0]
    return created_id

with psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port) as conn:
    with conn.cursor() as cursor:
        #cursor.execute('drop table Orders; drop table Customers; drop table machines; drop table models; drop table manufacturers;')
        cursor.execute('create table Orders (number serial NOT NULL PRIMARY KEY, customerId int, serialNumber int)')
        cursor.execute('create table Customers (id serial NOT NULL PRIMARY KEY, name text)')
        cursor.execute('create table Machines (serialNumber serial NOT NULL PRIMARY KEY, modelNumber int)')
        cursor.execute('create table Models (id int NOT NULL PRIMARY KEY, speed real, ram int, hd int, price real, manufacturerId int)')
        cursor.execute('create table Manufacturers (id serial NOT NULL PRIMARY KEY, name text)')

        customers = []
        customers.append(insert_customer(cursor, "Kasandra Cryer"))
        customers.append(insert_customer(cursor, 'Ferne Linebarger'))
        customers.append(insert_customer(cursor, 'Britany Manges'))
        customers.append(insert_customer(cursor, 'Alma Secrist'))
        customers.append(insert_customer(cursor, 'Sanda Archer'))
        customers.append(insert_customer(cursor, 'Michal Verona'))
        customers.append(insert_customer(cursor, 'Yuki Maio'))
        customers.append(insert_customer(cursor, 'Nichole Chiles'))
        customers.append(insert_customer(cursor, 'Margy Avis'))
        customers.append(insert_customer(cursor, 'Elana Shahid'))
        customers.append(insert_customer(cursor, 'Marvella Searcy'))

        apple = insert_manufacturer(cursor, 'apple')
        dell = insert_manufacturer(cursor, 'dell')

        insert_model(cursor, 1002, 2.1, 512, 250, 995, apple)
        insert_model(cursor, 1003, 1.42, 512, 80, 478, dell)
        insert_model(cursor, 1004, 2.8, 1024, 250, 649, dell)
        insert_model(cursor, 1005, 3.2, 512, 250, 630, dell)
        insert_model(cursor, 1006, 3.2, 1024, 320, 1049, apple)
        insert_model(cursor, 1007, 2.2, 1024, 200, 510, dell)
        insert_model(cursor, 1008, 2.2, 2048, 250, 770, dell)
        insert_model(cursor, 1009, 2, 1024, 250, 650, dell)
        insert_model(cursor, 1010, 2.8, 2048, 300, 770, dell)
        insert_model(cursor, 1011, 2.86, 2048, 160, 959, dell)
        insert_model(cursor, 1012, 2.8, 1024, 160, 649, dell)

        machines = []
        for model in range(1002, 1013):
            for machine in range(3):
                machines.append(insert_machine(cursor, model))


        for customer in customers:
            for machine in machines:
                # sort of a nonsense way to decide whether this customer bought this machines... but 
                # this will do for fake data!
                if customer*4 % machine == 3 or customer *2 % 3 == 2:
                    insert_order(cursor, customer, machine)
        


        

print('Your database is populated, your do not need to re-run this unless you remove/edit your data and want to reset the database. ')

        
