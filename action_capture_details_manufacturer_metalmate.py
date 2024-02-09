import pyautogui
import os
import time
import pyperclip

def main(**kwargs):
    #### 1901000
    #part_number = input("Enter the part number: ")
    """ part numbers        
    """
    #part_numbers = ['1151M390006']
    part_numbers = ['1151M390006','1151M390008','1151M390010','1151M390012','1151M390016','1151M390020','1151M390025','1151M390030','1151M390035','1150M390004','1150M390005','1150M390006','1150M390008','1150M390010','1150M390012','1150M390016','1150M390018','1150M390020','1150M390025','1150M390030','1150M390035','1150M390040','1150M390045','1150M390050','1150M390060','Z0322M39','0412T39','']




    for part_number in part_numbers:
        part_number = str(part_number)
        grab_part_info(part_number)



def grab_part_info(part_number):
    #delay_long = 5
    delay_long = 2

    #delay_short = 2
    delay_short = 1

    file_output = "output_manufacturer_metalmate.csv"


    webpage_start = "https://www.harclob2b.com/"

    position_search_box = [500,190]
    position_part_first = [600,495]
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
        time.sleep(10)
        return
    else:
        pass
        
        detail_names = []
        detail_names.append("part_number_manufacturer_metalmate")
        detail_names.append("webpage_manufacturer_metalmate")
        detail_names.append("name_manufacturer_metalmate")
        detail_names.append("box_size_manufacturer_metalmate")
        detail_names.append("box_of_box_size_manufacturer_metalmate")
        detail_names.append("commonity_code")
        detail_names.append("barcode_manufacturer_metalmate")
        details = {}

        # part number
        details["part_number_manufcturer_metalmate"] = part_number

        

        

        matches = []
        match = {"name":"name_manufacturer_metalmate","line_after":"Back to overview"}        
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
                if match["line_after"] in lines[i]:
                    details[match["name"]] = lines[i+1].replace("\n","").replace("\r","")
                    break
    
    
        # web address
        print("Grabbing web address")
        pyautogui.click(position_address_bar,interval=5)
        time.sleep(delay_long)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(delay_long)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(delay_long)
        web_address = pyperclip.paste()        
        details["webpage_manufacturer_metalmate"] = web_address

        #add to csv
        print("Writing to csv")
        if not os.path.exists(file_output):
            with open(file_output, 'w') as file:
                line = ""
                for detail_name in detail_names:
                    line += f"{detail_name},"                
                file.write(f"{line}\n")
        with open(file_output, 'a') as file:
            #use get and default to none
            for detail_name in detail_names:
                detail = details.get(detail_name,"none")
                file.write(f"{detail},")
            file.write("\n")
            
            
            









if __name__ == "__main__":
    kwargs = {}
    main(**kwargs)