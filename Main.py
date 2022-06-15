#Main.py
'''
Title:
Author: Beatrix Bicomong
Date: May 26, 2022
'''

import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect

# --- GLOBAL VARIABLES --- #
DB_NAME = "dataTable.db"
FIRST_RUN = True
if (Path.cwd() / DB_NAME).exists():
    FIRST_RUN = False

# --- FLASK --- #
app = Flask(__name__)

# --- WEBPAGES

@app.route('/', methods=['GET', 'POST'])
def index():
    """Homepage of website
    """
    ALERT = ""
    if request.form:
        DATE = request.form.get("date")
        TIME_IN = request.form.get("time_in")
        TIME_OUT = request.form.get("time_out")
        if DATE == "":
            ALERT = f"You didn't add anything >:("
            return render_template("index.html", alert=ALERT)
        if getOneDate(DATE) is None:
            createTimes(DATE, TIME_IN, TIME_OUT)
            ALERT = f"Successfully added {DATE} to time tracker! You did it :D"
        else:
            ALERT = f"{DATE} already used! Try again!"
            print("Date already exists")

    return render_template("index.html", alert=ALERT)

@app.route('/addAll', methods=['GET', 'POST'])
def addAll():
    """Calculates the total hours from the database

    Returns:
        int: Total amount of hours
    """
    DATA = getAllDates()
    ALERT = ""
    RESULT = addAll(DATA)

    if RESULT == 0:
        ALERT = f"There is no added data to calculate."        
    else:
        ALERT = f"You have an overall total of {RESULT} hours."

    return render_template("index.html", alert=ALERT)

@app.route('/search', methods=['POST'])
def search():
    """searches for the timestamp within the database

    Returns:
        str: Date
    """
    if request.form:
        SEARCH = request.form.get("searching")
        if getOneDate(SEARCH) is None:
            return redirect("/seeDateAll")
        else:
            TIME_IN, TIME_OUT = getTime(SEARCH)
            return render_template("search.html", variable1=TIME_IN, variable2=TIME_OUT, variable=SEARCH)      

@app.route('/seeDateAll', methods=['GET', 'POST'])
def seeAll():
    """See all Dates page
    """
    QUERY_TIMES = getAllDates()

    return render_template("seeDateAll.html", times=QUERY_TIMES)

@app.route('/delete/<id>')
def deleteDatePage(id):
    """Deletes the data from the database

    Args:
        id (str): The id of the timestamp

    Returns:
        redirect: Redirects the page
    """
    deleteDate(id)
    return redirect('/seeDateAll')

### --- INPUTS --- ###
# --- DATA BASE --- #
def createTimes(DATE, TIME_I, TIME_O):
    """Creates a section to add to the database

    Args:
        DATE (str): Date
        TIME_I (str): Starting time
        TIME_O (str): Ending time
    """
    global DB_NAME

    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute('''
            INSERT INTO
                times
            VALUES(
                ?, ?, ?
            )
    ;''', [DATE, TIME_I, TIME_O])

    CONNECTION.commit()
    CONNECTION.close()

### --- PROCRESSING --- ###
def createTable():
    """Creates the database table on first run
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute('''
            CREATE TABLE
                times(
                    date TEXT PRIMARY KEY NOT NULL,
                    time_in TEXT,
                    time_out TEXT
                )
    ;''')

    CONNECTION.commit()
    CONNECTION.close()

def deleteDate(DATE):
    """Deletes a contact

    Args:
        DATE (str): primary key
    """
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute('''
        DELETE FROM
            times
        WHERE
            date = ?
    ;''',[DATE])
    CONNECTION.commit()
    CONNECTION.close()

def addAll(DATA):
    """Adds data together

    Returns:
        int: Total Amount
    """

    NUM_1 = []
    NUM_2 = []
    LIST_A = []
    LIST_B = []
    TOTAL_LIST = []
    TOTAL = 0
    
    for i in range(len(DATA)):
        NUM_1.append(DATA[i][1])
        VALUE_1_RAW = NUM_1.pop(0)
        VALUE_1 = VALUE_1_RAW.split(":")
        A_1 = VALUE_1.pop(0)
        A_1 = int(A_1)
        A_1 = A_1 * 60
        A_2 = VALUE_1.pop(0)
        A_2 = int(A_2)
        A = A_1 + A_2
        LIST_A.append(A)
        NUM_2.append(DATA[i][2])
        VALUE_2_RAW = NUM_2.pop(0)
        VALUE_2 = VALUE_2_RAW.split(":")
        B_1 = VALUE_2.pop(0)
        B_1 = int(B_1)
        B_1 = B_1 * 60
        B_2 = VALUE_2.pop(0)
        B_2 = int(B_2)
        B = B_1 + B_2
        LIST_B.append(B)
    
    for i in range(len(LIST_A)):
        SUB = LIST_B[i] - LIST_A[i]
        DIV = SUB / 60
        TOTAL_LIST.append(DIV)

    for i in range(len(TOTAL_LIST)):
        RESULT = TOTAL_LIST.pop(0)
        if RESULT < 0: 
            RESULT = RESULT * -1
        TOTAL = TOTAL + RESULT
        TOTAL = round(TOTAL, 2) 
        
    return TOTAL

### --- OUTPUTS --- ###
def getOneDate(DATE):
    """Query and return a single date from the database

    Args:
        DATE (str): 
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    TIME = CURSOR.execute('''
            SELECT
                *
            FROM
                times
            WHERE
                date = ?
    ;''', [DATE]).fetchone()
    CONNECTION.close()
    return TIME

def getAllDates():
    """Returns every row in the timetable database

    Returns:
        TIME (list):
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    TIMES = CURSOR.execute('''
            SELECT
                *
            FROM
                times
            ORDER BY
                date
    ;''').fetchall()
    CONNECTION.close()
    return TIMES

def getTime(TIME):
    """Query and returns the time in and out from the database

    Args:
        TIME (str): ID

    Returns:
        int: Times in and out
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    R_TIME_IN = CURSOR.execute('''
            SELECT
                time_in
            FROM
                times
            WHERE
                date = ?
    ;''', [TIME]).fetchone()

    R_TIME_OUT = CURSOR.execute('''
            SELECT
                time_out
            FROM
                times
            WHERE
                date = ?
    ;''', [TIME]).fetchone()

    L_TIME_IN = list(R_TIME_IN)
    L_TIME_OUT = list(R_TIME_OUT)

    TIME_IN = L_TIME_IN.pop(0)
    TIME_OUT = L_TIME_OUT.pop(0)

    return TIME_IN, TIME_OUT


if __name__ == "__main__":
    if FIRST_RUN:
        createTable()
    app.run(debug=True)
