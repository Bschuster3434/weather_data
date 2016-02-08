import sqlite3
import requests
import json
import sys
import os

##The Organization of the program
#Check if You have any requests left
#If you, subtract by 1 from that file, write and continue
#open connection to tracker and grab one file where the data has not been scrapper
#incorporate data into a request
#execute the request
#parse the json and insert into the weatherData table data
#update the record to know it's completed
#close the connection

def open_requestsLeft(requestFile = 'requestsLeft.txt'):
    with open(requestFile, 'rb') as f:
        requestsLeft = f.read()
        return requestsLeft

def minus_one_requestsLeft(current_value, requestFile = 'requestsLeft.txt'):
    with open(requestFile, 'wb') as f:
        f.write(str(int(current_value) - 1))

def grab_next_tracker_record(db = 'weather.db', table ='tracker'):
    #Run a script to grab the most recent db

    statement = 'SELECT * FROM ' + table + " where complete = 0 LIMIT 1"

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    record = [row for row in conn.execute(statement)][0]
    conn.close()
    return record


def build_url_path(api_values):
    """Builds the path for the weathersource api"""

    

def main():
    requestsLeft = open_requestsLeft()
    if requestLeft == 0:
        sys.exit() #Exit if no requests left for day

    #Else, increment file donw by one and continue
    minus_one_requestsLeft(requestsLeft)

    #Grab the next tracker record
    next_values = grab_next_tracker_record()

    ##table structure: _id, zip, date, complete
    #Build the path



###For testing purposes
def test():
    with open('test_request_value.txt', 'wb') as f:
        f.write('100')

    assert open_requestsLeft('test_request_value.txt') == str(100)
    minus_one_requestsLeft(99, requestFile = 'test_request_value.txt')
    assert open_requestsLeft('test_request_value.txt') == str(98)
    os.remove('test_request_value.txt')

    c = sqlite3.connect('testdb.db')
    try:
        c.execute('create table test (id, complete)')
    except:
        cont = 1
    c.commit()
    c.execute('insert into test values (7, 0)')
    c.commit()
    c.execute("insert into test values (3, 1)")

    assert grab_next_tracker_record(db = 'testdb.db', table ='test')['id'] == 7
    c.close()
    os.remove('testdb.db')

    print 'Tests Passed'

test()
