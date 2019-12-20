import os
import csv
import json
from collections import OrderedDict

def get_json_files_in_cwd():
    path = os.getcwd()
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))
    return files

def convert(file_name):
    try:
        extension = file_name.split(".")[-1].lower()
        
        f = open(file_name)
        if extension == "json":
            # load json file
            data = json.load(f,object_pairs_hook=OrderedDict)
            print("JSON file loaded")
        else:
            print("unsupported file type ... exiting")
            exit()
    except Exception as e:
        # error loading file
        print("Error loading file ... exiting:",e)
        exit()
    else:
        if extension == "json":
            # get all keys in json objects
            keys = []
            for i in range(0,len(data)):
                for j in data[i]:
                    if j not in keys:
                        keys.append(j)
            
            # map data in each row to key index
            converted = []
            converted.append(keys)

            for i in range(0,len(data)):
                row = []
                for j in range(0,len(keys)):
                    if keys[j] in data[i]:
                        row.append(data[i][keys[j]])
                    else:
                        row.append(None)
                converted.append(row)

        # CREATE OUTPUT FILE
        converted_file_basename = os.path.basename(file_name).split(".")[0]
        converted_file_extension = ".csv"

        if(os.path.isfile(converted_file_basename + converted_file_extension)):
            counter = 1
            while os.path.isfile(converted_file_basename + " (" + str(counter) + ")" + converted_file_extension):
                counter += 1
            converted_file_basename = converted_file_basename + " (" + str(counter) + ")"
        
        try:
            with open(converted_file_basename + converted_file_extension, 'w') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(converted)
        except:
            print("Error creating file ... exiting")
        else:
            print("File created:",converted_file_basename + converted_file_extension)

if __name__ == "__main__":
    files = get_json_files_in_cwd()
    for file_name in files:
        convert(file_name)
