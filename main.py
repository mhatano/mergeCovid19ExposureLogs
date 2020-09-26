import glob
import json
import pandas as pd
import re

# List up all json files under data directory
files = glob.glob("data/*.json")

# Read every json file and merge only unique records into single data
json_new = list()
for file in files:
    json_file = open(file=file, encoding='utf8', mode='r')
    json_contents = json.load(json_file)

    # Original data timestamp contains single-digit month, day and hour,
    # which are totally unsuitable for sorting, fix them
    for entry in json_contents:
        re_timestamp = re.sub('年([1-9])月', '年0\\1月', entry['timestamp'])
        re_timestamp = re.sub('月([1-9])日', '月0\\1日', re_timestamp)
        re_timestamp = re.sub(' ([1-9]):', ' 0\\1:', re_timestamp)
        entry['timestamp'] = re_timestamp
        if json_new.count(entry) == 0:
            json_new.append(entry)


# Sort by timestamp
json_new.sort(key=lambda x: x['timestamp'])

# Convert json data into DataFrame
dataframe = pd.read_json(json.dumps(json_new))

# Save the data into Excel file
dataframe.to_excel('merged.xlsx')
