import csv
import yaml
import os

def main(**kwargs):
    file_input_csv = "working.csv"
    file_output_yaml = "data/output.yaml"

    data = []
    with open(file_input_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    #remove all fileds that start working_
    for i in range(len(data)):
        for key in list(data[i].keys()):
            if key.startswith("working_"):
                del data[i][key]
    
    #rename key oomp_id to id
    for i in range(len(data)):
        data[i]["id"] = data[i]["oomp_id"]
        del data[i]["oomp_id"]

    #make directories if they dno't exist
    os.makedirs(os.path.dirname(file_output_yaml), exist_ok=True)    
    with open(file_output_yaml, 'w') as file:
        yaml.dump(data, file)






if __name__ == "__main__":
    kwargs = {}
    main(**kwargs)