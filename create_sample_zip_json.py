import json
import datetime

zipcodes = ['22222', '46038']

base = datetime.date(2014, 12, 31)
numdays = 2000
datelist = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
datelist = [ date.strftime('%m/%d/%Y') for date in datelist]

##Creating a List

unique_id = 0
dict_output = []

for zip in zipcodes:
    for date in datelist:
        next_dict = {}
        next_dict['id'] = unique_id
        unique_id += 1
        next_dict['date'] = date
        next_dict['zip'] = zip
        dict_output.append(next_dict)

with open('sample_zip.json', "w") as f:
        json.dump(dict_output, f)
