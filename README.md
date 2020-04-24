# Overview
FamilyFavorites is simple Python program that integrates with PostgreSql to store family favorite meals inluding: name, cost, prep time, and stars.

# Instructions
To run this program:
1) Install Postgre SQL.  When you install, you will prompted for a password.  You will need this
password when you run the SQL Shell and when you the code below.
2) Install psycopg2: `pip install psycopg2`
3) Create a database and table (using the psql - SQL Shell that was installed with postgre) using the 
following commands:

```sql
create database family_favorites;
\c family_favorites
create table meals(ID SERIAL PRIMARY KEY, NAME TEXT NOT NULL, TIME_PREP INT, COST INT, STARS INT NOT NULL);
\d meals
```

# Useful Links
* https://www.postgresql.org
* https://www.tutorialspoint.com/postgresql/
* https://www.psycopg.org/
* https://www.postgresqltutorial.com/postgresql-python/

# Commands
FamilyFavorites has a simple command line interface.  The commands include the following:

* q,\<s|c|t\>,\<h|l\> - query sort (s=stars, c=cost, t=time, h=higher to lower, l=lower to higher
* i,\<name\>,\<stars\>,\<cost\>,\<time\> - insert
* d,\<id\> - delete
* u,\<id\>,\<stars\>,\<cost\>,\<time\> - update
* h - help
* x - exit

The selected query will be remembered until a new query is selected.  The updated list of tasks will be displayed after each command (except the help and exit commands).

Sample table output is shown below:

```
Current query [sort by=Stars , direction=Higher to Lower]
 ID  Stars   Cost   Time  Name
---  -----  -----  -----  --------------------
  1      5     19     60  Spaghetti
  2      5     20     30  Train Sandwiches
  3      4     18     60  Beef Stew
```