import psycopg2

"""
This program uses postgre sql to manage a list of favorite family meals.  To use this program, you 
need to do the following:

1) Install Postgre SQL.  When you install, you will prompted for a password.  You will need this
password when you run the SQL Shell and when you the code below.
2) Install psycopg2: pip install psycopg2
3) Create a database and table (using the psql - SQL Shell that was installed with postgre) using the 
following commands:

create database family_favorites;
\c family_favorites
create table meals(ID SERIAL PRIMARY KEY, NAME TEXT NOT NULL, TIME_PREP INT, COST INT, STARS INT NOT NULL);
\d meals

Useful Links:
https://www.postgresql.org
https://www.tutorialspoint.com/postgresql/
https://www.psycopg.org/
https://www.postgresqltutorial.com/postgresql-python/
"""

MEALS_SORT_STARS=4
MEALS_SORT_COST=3
MEALS_SORT_TIME_PREP=2
HIGHER_TO_LOWER=True
LOWER_TO_HIGHER=False

def connect(user_password):
    """
    Connect to the family_favorites database running on your computer using the provided password
    If it fails to connect, an error will be printed and connection returned will be None.
    """
    db_connection = None
    try:
        print("Connecting to family_favorites database...")
        # Connect to the database
        db_connection = psycopg2.connect(host="localhost",database="family_favorites", user="postgres", password=user_password)
        print("Connected!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return db_connection
        
def get_meals(db_connectionm, sort_col, higher_to_lower):
    """
    Get all the meals from the family_favorites database and return as a list of tuples.
    The query is done based on the sort column (which will always also include the name)
    and the direction to sort.  

    The content in the tuples is as follows:
    [0] => id
    [1] => name
    [2] => time_prep
    [3] => cost
    [4] => stars
    """
    if db_connection is None:       
        return
    # Obtain a cursor to allow operations on the database
    db_cursor = db_connection.cursor()

    # Define the command and execute it
    if direction == HIGHER_TO_LOWER:
        dir_cmd = "DESC"
    else:
        dir_cmd = "ASC"    
    if sort_by == MEALS_SORT_COST:
        sort_by_col = "cost "+dir_cmd+", name ASC"
    elif sort_by == MEALS_SORT_STARS:
        sort_by_col = "stars "+dir_cmd+", name ASC"
    elif sort_by == MEALS_SORT_TIME_PREP:
        sort_by_col = "time_prep "+dir_cmd+", name ASC"
    else:
        sort_by_col = "name ASC"

    command = "SELECT * FROM MEALS ORDER BY " + sort_by_col
    db_cursor.execute(command)

    # Get all the results and return them
    results = db_cursor.fetchall()
    db_cursor.close()
    return results

def add_meal(db_connection, name, time_prep, cost, stars):
    """
    Insert a new meal into the meals table.
    """
    if db_connection is None:       
        return
    # Obtain a cursor to allow operations on the database
    db_cursor = db_connection.cursor()

    # Define the command and execute it
    command = "INSERT INTO meals (name, time_prep, cost, stars) values (%s, %s, %s, %s)"
    values = (name, time_prep, cost, stars)
    db_cursor.execute(command, values)
    db_connection.commit()
    db_cursor.close()

def delete_meal(db_connection, meal):
    """
    Delete the meal based on the id (which is in meal[0])
    """
    if db_connection is None:
        return
    # Obtain a cursor to allow operations on the database        
    db_cursor = db_connection.cursor()

    # Define the command and execute it
    command = "DELETE FROM meals WHERE ID = %s"
    values = (meal[0],)
    db_cursor.execute(command, values)
    db_connection.commit()
    db_cursor.close() 

def update_meal(db_connection, meal, new_time_prep, new_cost, new_stars):
    """
    Update the time prep, cost, and stars for the meal based on the id (whih is in meal[0])
    """
    print(meal)
    if db_connection is None:
        return
    # Obtain a cursor to allow operations on the database        
    db_cursor = db_connection.cursor()

    # Define the command and execute it
    command = "UPDATE meals SET time_prep = %s, cost = %s, stars = %s WHERE ID = %s"    
    values = (new_time_prep, new_cost, new_stars, meal[0])
    db_cursor.execute(command, values)
    db_connection.commit()
    db_cursor.close() 

def disconnect(db_connection):
    """
    Close the connection to the database.
    """
    if db_connection is not None:
        db_connection.close()
        print('Database connection closed.')

def display_meals(meals):
    """
    Display a formated list of meals.
    """
    print("{:>3}  {:>5}  {:>5}  {:>5}  {}".format("ID", "Stars", "Cost", "Time", "Name"))
    print("{:>3}  {:>5}  {:>5}  {:>5}  {}".format("-"*3, "-"*5, "-"*5, "-"*5, "-"*20))
    table_id = 1
    # The id shown in the table is based on the location in the sorted list
    for meal in meals:
        print("{:>3}  {:>5}  {:>5}  {:>5}  {}".format(table_id, meal[4], meal[3], meal[2], meal[1]))
        table_id += 1

def convert_sort_by(sort_by):
    """
    Provide a string mapping for the SORT constants
    """
    if sort_by == MEALS_SORT_COST:
        return "Cost"
    if sort_by == MEALS_SORT_STARS:
        return "Stars"
    if sort_by == MEALS_SORT_TIME_PREP:
        return "Time"
    return "None"

def convert_direction(direction):
    """
    Provide a string mapping for the direction constants
    """
    if direction == HIGHER_TO_LOWER:
        return "Higher to Lower"
    return "Lower to Higher"


# Main Program
user_password = input("Enter password for user [postgres]: ")
db_connection = connect(user_password)
if db_connection is None:
    exit_program = True
else:
    exit_program = False
# Start the program by showing open tasks in all categories
sort_by = MEALS_SORT_STARS
direction = HIGHER_TO_LOWER
# When redisplay is True, then the updated table will display
# after the command is processed.
redisplay = True
while not exit_program:
    try:
        print()
        # Redisplay the updated table
        if redisplay:
            print("Current query [sort by={} , direction={}]".format(convert_sort_by(sort_by), convert_direction(direction)))
            meals = get_meals(db_connection, sort_by, direction)
            display_meals(meals)
            print()
        else:
            redisplay = True
        # Get the command from the user and split up by commas
        command = input("> ")
        params = command.split(",")
        # Perform the action based on the first parameter
        if params[0] == "h" and len(params) == 1:
            print("q,<s|c|t>,<h|l> - query sort (s=stars, c=cost, t=time, h=higher to lower, l=lower to higher")
            print("i,<name>,<stars>,<cost>,<time> - insert")
            print("d,<id> - delete")
            print("u,<id>,<stars>,<cost>,<time> - update")
            print("h - help")
            print("x - exit")
            redisplay = False
        elif params[0] == "q" and len(params) == 3:
            # Determine the status and category parameters
            if params[1] == "s":
                sort_by = MEALS_SORT_STARS
            elif params[1] == "c":
                sort_by = MEALS_SORT_COST
            else:
                sort_by = MEALS_SORT_TIME_PREP
            if params[2] == "h":
                direction = HIGHER_TO_LOWER
            else:
                direction = LOWER_TO_HIGHER
        elif params[0] == "i" and len(params) == 5:
            add_meal(db_connection, params[1], params[4], params[3], params[2])
        elif params[0] == "d" and len(params) == 2:
            # Need to be careful about converting id to 0 based index
            delete_meal(db_connection, meals[int(params[1])-1])
        elif params[0] == "u" and len(params) == 5:
            # Need to be careful about converting id to 0 based index
            update_meal(db_connection, meals[int(params[1])-1], params[4], params[3], params[2])
        elif params[0] == "x" and len(params) == 1:
            exit_program = True
        else:
            print("Invalid command.")
    except IndexError:
        # If number conversions or invalid ID's occur, then catch them 
        # to prevent the program from exiting.
        print("Invalid command.")
