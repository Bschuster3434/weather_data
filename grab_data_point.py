import sqlite3
import requests
import json
import sys
import os
import time

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

def get_key():
    """Get the api key. Add local key path"""
    path = r'C:\Users\Bschuster\Desktop\api_key.txt'
    with open(path, 'rb') as f:
        key = f.read()
    return key

def build_url_path(api_values):
    """Builds the path for the weathersource api"""
    api_dict = {}
    api_dict['_id'] = api_values['_id']
    api_dict['postal_code_eq'] = str(api_values['zip'])
    raw_date = time.strptime(api_values['date'], '%m/%d/%Y')
    api_dict['iso_date'] = time.strftime("%Y-%m-%dT%H:%M:%S", raw_date)
    api_dict['country_eq'] = 'US'
    key = get_key()
    api_path = 'https://api.weathersource.com'
    api_path += '/v1/' + key + '/history_by_postal_code.json?'
    api_path += 'period=day&postal_code_eq=' + api_dict['postal_code_eq']
    api_path += '&country_eq=' + api_dict['country_eq']
    api_path += '&timestamp_eq=' + api_dict['iso_date']
    api_path += '&&fields=postal_code,country,timestamp,tempMax,tempAvg,tempMin,precip,snowfall,windSpdMax,windSpdAvg,windSpdMin,cldCvrMax,cldCvrAvg,cldCvrMin,dewPtMax,dewPtAvg,dewPtMin,feelsLikeMax,feelsLikeAvg,feelsLikeMin,relHumMax,relHumAvg,relHumMin,sfcPresMax,sfcPresAvg,sfcPresMin,spcHumMax,spcHumAvg,spcHumMin,wetBulbMax,wetBulbAvg,wetBulbMin'
    api_dict['url'] = api_path
    return api_dict

def contact_api(api_dict):
    """Go out to the api and return the JSON Values """

    url = api_dict['url']
    r = requests.get(url)
    json_response = r.json()[0]
    json_response['status'] = r.status_code
    json_response['_id'] = api_dict['_id']
    return json_response

def update_weatherData(api_values, db = 'weather.db'):
    """Insert API Values"""
    statement = """
    INSERT INTO weatherData (
    id
    ,timestamp
    ,tempMax
    ,tempAvg
    ,tempMin
    ,precip
    ,snowfall
    ,windSpdMax
    ,windSpdAvg
    ,windSpdMin
    ,cldCvrMax
    ,cldCvrAvg
    ,cldCvrMin
    ,dewPtMax
    ,dewPtAvg
    ,dewPtMin
    ,feelsLikeMax
    ,feelsLikeAvg
    ,feelsLikeMin
    ,relHumMax
    ,relHumAvg
    ,relHumMin
    ,sfcPresMax
    ,sfcPresAvg
    ,sfcPresMin
    ,spcHumMax
    ,spcHumAvg
    ,spcHumMin
    ,wetBulbMax
    ,wetBulbAvg
    ,wetBulbMin
    )
    VALUES
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    value_list = [api_values['_id'], api_values['timestamp'], api_values['tempMax'], api_values['tempAvg'], api_values['tempMin'], api_values['precip'], api_values['snowfall'], api_values['windSpdMax'], api_values['windSpdAvg'], api_values['windSpdMin'], api_values['cldCvrMax'], api_values['cldCvrAvg'], api_values['cldCvrMin'], api_values['dewPtMax'], api_values['dewPtAvg'], api_values['dewPtMin'], api_values['feelsLikeMax'], api_values['feelsLikeAvg'], api_values['feelsLikeMin'], api_values['relHumMax'], api_values['relHumAvg'], api_values['relHumMin'], api_values['sfcPresMax'], api_values['sfcPresAvg'], api_values['sfcPresMin'], api_values['spcHumMax'], api_values['spcHumAvg'], api_values['spcHumMin'], api_values['wetBulbMax'], api_values['wetBulbAvg'], api_values['wetBulbMin']]

    c = sqlite3.connect(db)
    c.execute(statement, value_list)
    c.commit()
    c.close()
    return 1

def update_tracker(api_values, db = 'weather.db', table ='tracker'):
    """Update Tracker with 1 for complete"""

    statement = "UPDATE tracker set complete = 1 WHERE _id = " + str(api_values['_id'])
    c = sqlite3.connect(db)
    c.execute(statement)
    c.commit()
    c.close()
    return 1

def main():
    requestsLeft = open_requestsLeft()
    if requestsLeft == 0:
        sys.exit() #Exit if no requests left for day

    #Else, increment file donw by one and continue
    minus_one_requestsLeft(requestsLeft)

    #Grab the next tracker record
    next_values = grab_next_tracker_record()

    ##table structure: _id, zip, date, complete
    #Build the path
    api_dict = build_url_path(next_values)

    #Run the path to get a list of values
    api_values = contact_api(api_dict)

    #Update weatherData
    #Update tracker



###For testing purposes
def test():
    ##Testing Open Requests
    with open('test_request_value.txt', 'wb') as f:
        f.write('100')

    assert open_requestsLeft('test_request_value.txt') == str(100)
    minus_one_requestsLeft(99, requestFile = 'test_request_value.txt')
    assert open_requestsLeft('test_request_value.txt') == str(98)
    os.remove('test_request_value.txt')

    ##Testing DB Reads
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

    #Testing api url build
    test_values = {'_id': 1, 'zip': 22222, 'date' : '1/1/2012'}
    assert build_url_path(test_values)['iso_date'] == '2012-01-01T00:00:00'

    #Test returning path
    test_values_1 = {'_id': 1, 'zip': 22222, 'date': '1/1/2014'}
    test_api_dict = build_url_path(test_values_1)
    #with open('testurl.txt', 'w') as f:
    #    f.write(test_api_dict['url'])
    test_api_return = contact_api(test_api_dict)
    assert test_api_return['status'] == 200
    assert test_api_return['cldCvrMin'] == 1
    assert test_api_return['relHumMin'] == 47.1
    assert test_api_return['sfcPresMin'] == 1021.9
    assert test_api_return['_id'] == 1

    #Test Api Update Sequence
        ##Testing DB Reads
    c = sqlite3.connect('testdb.db')

    create_tracker = """
CREATE TABLE tracker
(_id INTEGER PRIMARY KEY AUTOINCREMENT
,zip TEXT
,date TEXT
,complete INTEGER
)
    """

    try:
        c.execute(create_tracker)
    except:
        cont = 1
    c.commit()

    create_weatherData = """
CREATE TABLE weatherData
(
 id INTEGER PRIMARY KEY
,timestamp text
,tempMax real
,tempAvg real
,tempMin real
,precip real
,precipConf real
,snowfall real
,snowfallConf real
,windSpdMax real
,windSpdAvg real
,windSpdMin real
,cldCvrMax real
,cldCvrAvg real
,cldCvrMin real
,dewPtMax real
,dewPtAvg real
,dewPtMin real
,feelsLikeMax real
,feelsLikeAvg real
,feelsLikeMin real
,relHumMax real
,relHumAvg real
,relHumMin real
,sfcPresMax real
,sfcPresAvg real
,sfcPresMin real
,spcHumMax real
,spcHumAvg real
,spcHumMin real
,wetBulbMax real
,wetBulbAvg real
,wetBulbMin real
)
    """
    try:
        c.execute(create_weatherData)
    except:
        cont = 1
    c.commit()

    c.execute("INSERT INTO tracker VALUES(NULL, 22222, '1/1/2014', 0)")
    c.commit()
    #c.execute("INSERT INTO tracker VALUES(2, 12345, '1/1/2014', 0)")
    #c.commit()
    c.close()

    next_test_values = grab_next_tracker_record(db = 'testdb.db', table ='tracker')
    assert next_test_values['_id'] == 1
    api_test_dict = build_url_path(next_test_values)
    assert api_test_dict['_id'] == 1
    api_test_values = contact_api(api_test_dict)
    assert api_test_values['_id'] == 1

    #Where we're writing the logic to update the db
    #Update weatherData
    assert update_weatherData(api_test_values, db = 'testdb.db') == 1

    c = sqlite3.connect('testdb.db')
    c.row_factory = sqlite3.Row
    test_api_return = [row for row in c.execute('SELECT * From weatherData')][0]
    assert test_api_return['cldCvrMin'] == 1
    assert test_api_return['relHumMin'] == 47.1
    assert test_api_return['sfcPresMin'] == 1021.9
    assert test_api_return['id'] == 1 ###This is the only id that does not need the '_' at the beginning
    c.close()

    #Update Tracker
    assert update_tracker(api_test_values, db = 'testdb.db') == 1
    statement = "SELECT _id from tracker where complete = 1"
    conn = sqlite3.connect('testdb.db')
    conn.row_factory = sqlite3.Row
    record = [row for row in conn.execute(statement)][0]['_id']
    conn.close()
    assert record == 1




    os.remove('testdb.db')


    print 'KEY:'
    print get_key()
    print 'Tests Passed'

#test()
if __name__ == "__main__":
    main()
