# Project 1

Web Programming with Python and JavaScript

## journal

### 0.1 running flask
```
DATABASE_URL=postgres://srnwovmyccfpnj:37640f4bf3c4b28f2b3ee99fbbb1d9ffe72cd04a203a8ba98c9ea44520dcf691@ec2-52-6-143-153.compute-1.amazonaws.com:5432/daus1tm2bsv6d2 FLASK_APP=src/application.py FLASK_ENV=development flask run
```
### 1.0 setting up some basic files
- application.py
    > where the application will run
- templates/layout.hmtl
    > layout of the templates
    > template inheritance
- templates/index.html
    > starting/ default page
- templates/login.html
    > page for logging in
- templates/register.html
    > page to register if user doesen't have an account

### 2.0 basic back-end set up
- setting up application.py
    >


## TO DO

* [x] **SET UP A heroku DATABASE**
* [x] **SET UP THE FLASK SERVER CONNECTED TO THE HEROKU DATABASE**
* [x] **BUILD A BASIC PAGE WITH A LOGIN AND AN OPTION TO REGISTER**
* [x] **CREATE A USERS TABLE CONTAINING**
    - [x] **AN id** 
    - [x] **A username** 
    - [x] **A password**
* [x] **BUILD A REGISTRATION PAGE**
* [x] **CREATE A BOOKS TABLE CONTAINING**
    - **[x] AN id**
    - **[x] A TITLE**
    - **[x] THE AUTHOR**
    - **[x] THE PUBLICATION YEAR**
    - **[x] THE ISBN NUMBER**
    - **[x] THE REVIEW COUNT**
    - **[x] THE AVERAGE SCORE**
* [x] **IMPORT books.csv INTO THE DATABASE VIA AN import.py FILE**
* [x] **BUILD A BASE PAGE WITH A NAVBAR CONTAINING A SEARCH PAGE LINK AND A LOGOUT OPTION**
* [x] **BUILD A SEARCH PAGE WHICH SEARCHES BOOKS BY ISBN, AUTHOR NAME, OR TITLE**
* **[x] CREATE A REVIEW TABLE CONTAINING**
    - **[x] AN id**
    - **[x] A SCORE**
    - **[x] A TEXT REVIEW**
    - **[x] A RELATION TO THE USER_ID**
    - **[x] A RELATION TO THE BOOK**
* [x] **BUILD A BOOK PAGE ON WHICH A REVIEW CAN BE SUBMITTED CONTAINING**
    - [x] **A RATING SCALE FROM 1 TO 5**
    - [x] **A TEXT COMPONENT FOR AN OPINION**
    - [x] **USERS SHOULD NOT BE ABLE TO SUBMIT MULTIPLE REVIEWS**
* [x] **THE BOOK PAGE ALSO DISPLAYS THE AVAILABLE AVERAGE RATING AND NUMBER OF RATINGS FROM GOODREADS**
* [ ] **BUILD A ``/api/<isbn>`` WHERE <isbn> IS THE ISBN OF THE BOOK RESULTING IN A JSON WITH**
    - [x] **THE TITLE**
    - [x] **THE AUTHOR**
    - [x] **THE PUBLISHING YEAR**
    - [x] **THE ISBN**
    - [x] **THE REVIEW COUNT**
    - [x] **AND THE AVERAGE SCORE**
* [x] **IF THE ISBN IS NOT IN THE DATABASE, THE PAGE SHOULD SHOW A 404 Error**

### TO USE

* RAW SQL COMMANDS
* ALL ADDITIONAL PYTHON PACKAGES SHOULD BE CONTAINED WITHIN THE requirements.txt FILE

## 
