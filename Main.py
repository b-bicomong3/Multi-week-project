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
        if DATE is None:
            ALERT = f"You didn't add anything >:("
        if getOneDate(DATE) is None:
            createTimes(DATE, TIME_IN, TIME_OUT)
            ALERT = f"Successfully added {DATE} to time tracker! You did it :D"
        else:
            ALERT = f"{DATE} already used! Try again!"
            print("Date already exists")

    return render_template("index.html", alert=ALERT)

@app.route('/seeDateAll')
def seeAll():
    """See all Dates page
    """
    QUERY_TIMES = getAllDates()
    return render_template("seeDateAll.html", times=QUERY_TIMES)

@app.route('/delete/<id>')
def deleteDatePage(id):
    deleteDate(id)
    return redirect('/seeDateAll')

# --- DATA BASE --- #

### --- INPUTS --- ###
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

if __name__ == "__main__":
    if FIRST_RUN:
        createTable()
    app.run(debug=True)