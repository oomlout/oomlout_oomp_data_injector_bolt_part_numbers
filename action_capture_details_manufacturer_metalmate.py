import pyautogui
import os
import time
import pyperclip
import yaml

def main(**kwargs):
    #### 1901000
    #part_number = input("Enter the part number: ")
    """ part numbers        
    """
    part_numbers_manual = ['1151M390016','1151M390020','1151M390025']
    #part_numbers_manual = ['1151M390006','1151M390008','1151M390010','1151M390012','1151M390016','1151M390020','1151M390025','1151M390030','1151M390035','1150M390004','1150M390005','1150M390006','1150M390008','1150M390010','1150M390012','1150M390016','1150M390018','1150M390020','1150M390025','1150M390030','1150M390035','1150M390040','1150M390045','1150M390050','1150M390060','Z0322M39','0412T39','']
    part_numbers = kwargs.get("part_numbers_manufacturer_metalmate",part_numbers_manual)



    for part_number in part_numbers:
        part_number = str(part_number)
        grab_page_info(part_number)


    file_output = "output_manufacturer_metalmate.csv"
    #delete if it exists
    if os.path.exists(file_output):
        os.remove(file_output)

    for part_number in part_numbers:
        part_number = str(part_number)
        grab_part_info(part_number)


def grab_page_info(part_number, overwrite = False):
    delay_long = 5
    #delay_long = 2

    delay_short = 2
    #delay_short = 1

    directory_output = "temporary/manufacturer_metalmate"
    file_name = f"{directory_output}/{part_number}.yaml"
    
    file_output = "output_manufacturer_metalmate.csv"

    if not os.path.exists(file_name):


        webpage_start = "https://www.harclob2b.com/"

        position_search_box = [600,191]
        position_part_first = [713,570]
        #position_part_first = [713,499]
        position_address_bar = [218,64]
            #open browser
        print("Opening browser")
        os.system(f"start chrome {webpage_start}")
        time.sleep(delay_long)


        #click search box
        print("Clicking search box")
        pyautogui.click(position_search_box,interval=5)
        time.sleep(delay_long)

        #type in and search
        print("Typing in part number")
        pyautogui.typewrite(part_number)
        time.sleep(delay_long)
        pyautogui.press('enter')
        time.sleep(delay_long)

        #click on part
        print("Clicking on part")
        pyautogui.click(position_part_first,interval=5)
        time.sleep(delay_long)

        #select all
        print("copying page")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(2)
        page = pyperclip.paste()

        

        #test if part number is in page

        lines = page.split("\n")
        part_number_test = ""
        for line in lines:
            #is the line after "search"
            for i in range(len(lines)):
                if "Item No." in lines[i]:
                    part_number_test = lines[i].replace("Item No.","").replace("\n","").replace("\r","").strip()
                    break
        if part_number != part_number_test:
            #input 10 second timeout
            print(f"Part number {part_number} not found")        
            data = {}
            data["part_number"] = part_number
            data["page"] = page
            data["error"] = "part number not found"
            #time.sleep(10)
            #dump[ yaml
            if not os.path.exists(directory_output):
                os.makedirs(directory_output)
            with open(file_name, 'w') as file:
                yaml.dump(data, file)   

        else:
            pass
            
            data = {}
            data["part_number"] = part_number
            data["page"] = page

            # web address
            print("Grabbing web address")
            pyautogui.click(position_address_bar,interval=5)
            time.sleep(delay_long)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(delay_long)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(delay_long)
            web_address = pyperclip.paste()        

            data["web_address"] = web_address

            #write to file
            print("Writing to file")
            if not os.path.exists(directory_output):
                os.makedirs(directory_output)

            
            with open(file_name, 'w') as file:
                yaml.dump(data, file)
        #send ctrl w to close tab
        pyautogui.hotkey('ctrl', 'w')        

                
                
                


def grab_part_info(part_number):
    delay_long = 5
    #delay_long = 2

    delay_short = 2
    #delay_short = 1

    file_output = "output_manufacturer_metalmate.csv"

    directory_output = "temporary/manufacturer_metalmate"
    file_name = f"{directory_output}/{part_number}.yaml"
    file_name_part_error = f"{directory_output}/part_error.yaml"
    
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        error = data.get("error","")
        if error == "":

            #test if part number is in page
            page = data["page"]

            lines = page.split("\n")
            part_number_test = ""
            for line in lines:
                #is the line after "search"
                for i in range(len(lines)):
                    if "Item No." in lines[i]:
                        part_number_test = lines[i].replace("Item No.","").replace("\n","").replace("\r","").strip()
                        break
            if part_number != part_number_test:
                #input 10 second timeout
                print(f"Part number {part_number} not found")        
                #add to error file
                if not os.path.exists(file_name_part_error):
                    with open(file_name_part_error, 'w') as file:
                        file.write(f"{part_number}\n")
                else:
                    with open(file_name_part_error, 'a') as file:
                        file.write(f"{part_number}\n")
                return
            else:
                pass
                
                detail_names = []
                detail_names.append("part_number_manufacturer_metalmate")
                detail_names.append("link_manufacturer_metalmate")
                detail_names.append("name_manufacturer_metalmate")
                detail_names.append("box_size_manufacturer_metalmate")
                detail_names.append("box_of_box_size_manufacturer_metalmate")
                detail_names.append("commonity_code")
                detail_names.append("barcode_manufacturer_metalmate")
                details = {}

                # part number
                details["part_number_manufacturer_metalmate"] = part_number

                

                

                matches = []
                match = {"name":"name_manufacturer_metalmate","line_after":["Back to overview","Expand: Catalogue"]}        
                matches.append(match)
                match = {"name":"box_size_manufacturer_metalmate","line_after":"Box Quantity"}
                matches.append(match)
                match = {"name":"box_of_box_size_manufacturer_metalmate","line_after":"Sales Outer Qty."}
                matches.append(match)
                match = {"name":"commonity_code","line_after":"Commodity Code"}
                matches.append(match)
                match = {"name":"barcode_manufacturer_metalmate","line_after":"Barcode"}
                matches.append(match)
                
                for match in matches:
                    for i in range(len(lines)):
                        line_afters = match["line_after"]
                        #if not an array make it one
                        if type(line_afters) != list:
                            line_afters = [line_afters]
                        for line_after in line_afters:
                            if line_after in lines[i]:
                                details[match["name"]] = lines[i+1].replace("\n","").replace("\r","")
                                break
            
            
                web_address = data["web_address"]
                details["link_manufacturer_metalmate"] = web_address

                #add to csv
                print("Writing to csv")
                line = ""
                if not os.path.exists(file_output):
                    with open(file_output, 'w') as file:                
                        for detail_name in detail_names:
                            line += f"{detail_name},"                
                        file.write(f"{line}\n")
                
                with open(file_output, 'a') as file:
                    #use get and default to none
                    line = ""
                    for detail_name in detail_names:
                        detail = details.get(detail_name,"none")
                        line += f"{detail},"
                    file.write(f"{line}\n")
                    print(f"details: {line}")
                    
                    
                    









if __name__ == "__main__":
    kwargs = {}
    main(**kwargs)