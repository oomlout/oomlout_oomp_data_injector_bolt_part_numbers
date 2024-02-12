import action_capture_details_manufacturer_metalmate
import action_capture_details_distributor_orbital_fasteners

import os
import csv
import yaml

def main(**kwargs):
    print("working")
    
    harvest = False
    #harvest = True

    #csv_make = False
    csv_make = True

    #load csv_working file
    key_main = "oomp_id"
    kwargs["key_main"] = key_main
    
    kwargs = load_csv_working(**kwargs)

    

    if harvest:        
        #part numbers are loaded into kwargs in kload_csv_working
        action_capture_details_manufacturer_metalmate.main(**kwargs)
        #action_capture_details_distributor_orbital_fasteners.main(**kwargs)
        

    if csv_make:
        make_csv_file(**kwargs)

def load_csv_working(**kwargs):
    key_main = kwargs["key_main"]

    key_distributor_orbital_fasteners = "part_number_distributor_orbital_fasteners"
    kwargs["key_distributor_orbital_fasteners"] = key_distributor_orbital_fasteners
    
    key_manufacturer_metalmate = "part_number_manufacturer_metalmate"
    kwargs["key_manufacturer_metalmate"] = key_manufacturer_metalmate
    
    data_file_csv_working_oomp_id = {}
    kwargs["data_file_csv_working_oomp_id"] = data_file_csv_working_oomp_id
    
    data_file_csv_working_part_number_distributor_orbital_fasteners = {} 
    kwargs["data_file_csv_working_part_number_distributor_orbital_fasteners"] = data_file_csv_working_part_number_distributor_orbital_fasteners
    
    data_file_csv_working_part_number_manufacturer_metalmate = {}
    kwargs["data_file_csv_working_part_number_manufacturer_metalmate"] = data_file_csv_working_part_number_manufacturer_metalmate
    
    file_csv_working = "working.csv"    
    kwargs["file_csv_working"] = file_csv_working

    with open(file_csv_working, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row[key_main]
            data_file_csv_working_oomp_id[key] = row
            key = row.get(key_distributor_orbital_fasteners)
            if key != "":
                data_file_csv_working_part_number_distributor_orbital_fasteners[key] = row
            key = row.get(key_manufacturer_metalmate,"")
            if key != "":
                data_file_csv_working_part_number_manufacturer_metalmate[key] = row
    
    # add the part_number data to kwargs
    part_numbers_distributor_orbital_fasteners = data_file_csv_working_part_number_distributor_orbital_fasteners.keys()
    kwargs["part_numbers_distributor_orbital_fasteners"] = part_numbers_distributor_orbital_fasteners
    
    part_numbers_manufacturer_metalmate = data_file_csv_working_part_number_manufacturer_metalmate.keys()
    kwargs["part_numbers_manufacturer_metalmate"] = part_numbers_manufacturer_metalmate

    return kwargs

def make_csv_file(**kwargs):
    
    key_main = kwargs["key_main"]
    key_distributor_orbital_fasteners = kwargs["key_distributor_orbital_fasteners"]
    key_manufacturer_metalmate = kwargs["key_manufacturer_metalmate"]

    #load file_csv_working
    data_file_csv_working_oomp_id = kwargs["data_file_csv_working_oomp_id"]
    data_file_csv_working_part_number_distributor_orbital_fasteners = kwargs["data_file_csv_working_part_number_distributor_orbital_fasteners"]
    data_file_csv_working_part_number_manufacturer_metalmate = kwargs["data_file_csv_working_part_number_manufacturer_metalmate"]
    
            

            



    #load output_files
    file_csv_output_distributor_orbital_fastener = "output_distributor_orbital_fasteners.csv"
    file_csv_output_manufacturer_metalmate = "output_manufacturer_metalmate.csv"
    
    #load working.csv key pairs into data_output
    data_output = {}
    for row_id in data_file_csv_working_oomp_id:
        row = data_file_csv_working_oomp_id[row_id]
        data_output[row[key_main]] = row

    #add items
    items = []
    items.append({"file":file_csv_output_distributor_orbital_fastener,"key_dist_manu":key_distributor_orbital_fasteners, "data":data_file_csv_working_part_number_distributor_orbital_fasteners})
    items.append({"file":file_csv_output_manufacturer_metalmate,"key_dist_manu":key_manufacturer_metalmate, "data":data_file_csv_working_part_number_manufacturer_metalmate})
    
    oomp_ids = data_output.keys()
    

    for item in items:
        file = item["file"]
        key_dist_manu = item["key_dist_manu"]
        data = item["data"]
        #load the distributor or manufacturer file into a dict
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)            
            data_current_file = {}
            for row in reader:
                key = row[key_dist_manu]
                data_current_file[key] = row

        #iterate through oomp_ids
        for oomp_id in oomp_ids:
            part_number_test = data_output[oomp_id].get(key_dist_manu,"")
            if part_number_test != "":
                if part_number_test in data_current_file:
                    row = data_current_file[part_number_test]
                    for key in row:
                        data_output[oomp_id][key] = row[key]
                else:
                    print(f"part number {part_number_test} not found in {file}")
                

    #calculate price
    data_output = calculate_price(data_output)


    # sanitize
    data_output = sanitize_data(data_output)   

    # dump
    dump_data(data_output)


def calculate_price(data_output):
    print("calculating price")
    for row_id in data_output:
        row = data_output[row_id]
        distributor_current = row.get("distributor_current","internal")
        quantity_current = row.get("quantity_current","1")

        quantity_breaks = ["1","100","200","1000","10000"]
        
        for quantity_break in quantity_breaks:
            key_source = f"price_{quantity_break}_distributor_{distributor_current}"
            key_destination = f"price_{quantity_break}"
            if key_source in row:
                row[key_destination] = row[key_source]
            else:
                row[key_destination] = "missing_value"
        
        current_price_string = "price_current"
        key_source = f"price_{quantity_current}"
        if key_source in row:
            row[current_price_string] = row[key_source]
        else:
            row[current_price_string] = "missing_value"

    return data_output

def dump_data(data_output):
    print("dumping data")
    #make directories if they dno't exist
    file_output_yaml = "data/oomlout_oomp_data_injector_bolt_part_numbers/working.yaml"
    os.makedirs(os.path.dirname(file_output_yaml), exist_ok=True)    
    with open(file_output_yaml, 'w') as file:
        yaml.dump(data_output, file)

    #make directories if they dno't exist
    file_csv_output = "data/oomlout_oomp_data_injector_bolt_part_numbers/working.csv"
    os.makedirs(os.path.dirname(file_csv_output), exist_ok=True) 
    keys = []
    for row_id in data_output:
        for key in data_output[row_id]:
            if key not in keys:
                keys.append(key)   
    with open(file_csv_output, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for row_id in data_output:
            writer.writerow(data_output[row_id])

def sanitize_data(data_output):
    print("sanitizing data")
    #sanitize data_output
    remove_keys = []
    remove_keys.append("'? '")
    remove_keys.append("': '")
    remove_keys.append("")
    for row_id in data_output:
        row = data_output[row_id]
        for key in list(row.keys()):
            if key in remove_keys:
                del row[key]
            if "working_" in key:
                del row[key]

    #remove all none, "", and "none" values
    remove_values = ["none","", None]
    for row_id in data_output:
        row = data_output[row_id]
        for key in list(row.keys()):
            if row[key] in remove_values:
                del row[key]
    
    return data_output

if __name__ == "__main__":
    kwargs = {}
    main(**kwargs)