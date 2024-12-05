import pyautogui
import os
import time
import pyperclip
import yaml
import copy

def main(**kwargs):
    #### 1901000
    #part_number = input("Enter the part number: ")
    """ part numbers        
    """
    part_numbers_manual = []
    #part_numbers_manual = ['1901000','1901010','1901020','1901030','1901040','1901050','1901051','1901052','1901054','1890620','1891000','1891010','1891020','1891030','1891040','1891050','1891052','1891054','1891056','1891057','1891058','1771000','1711000','1731000']
    part_numbers_manual = [ "1771000"]
    
    part_numbers = copy.deepcopy(kwargs.get("part_numbers_distributor_orbital_fasteners",part_numbers_manual))
    
    

    for part_number in part_numbers:
        part_number = str(part_number)
        grab_page_info(part_number) #capture the page
        
    file_output = "output_distributor_orbital_fasteners.csv"
    #delete file_output if it exists
    if os.path.exists(file_output):
        os.remove(file_output)

    for part_number in part_numbers:
        grab_part_info(part_number) #use stored page to capture part info

def grab_page_info(part_number, overwrite = False):
    delay_long = 5
    #delay_long = 2

    delay_short = 2
    #delay_short = 1

    
    
    directory_output = "temporary/distributor_page_orbital_fasteners"
    file_name = f"{directory_output}/{part_number}.yaml"

    if not os.path.exists(file_name) or overwrite:
        print(f"Grabbing page info for {part_number}")

        webpage_start = "https://www.orbitalfasteners.co.uk/"

        position_search_box = [650,188]
        #position_search_box = [619,188]
        position_part_first = [868,637]
        #position_part_first = [868,669]
        position_address_bar = [390,59]

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
        #make upper case    
        page = page.upper()


        #remove all text after "YOU MIGHT ALSO LIKE"
        string_clip_after = "YOU MIGHT ALSO LIKE"
        if string_clip_after in page:
            print(f"Clipping page of '{string_clip_after}'")
            page = page.split(string_clip_after)[0]

        
        data = {}
        data["page"] = page
        

        #grabbing web address
        print("Grabbing web address")
        pyautogui.click(position_address_bar,interval=5)
        time.sleep(delay_long)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(delay_short)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(delay_short)
        web_address = pyperclip.paste()
        #remove trailing ? and everything after it
        if "?" in web_address:
            web_address = web_address.split("?")[0]

        data["web_address"] = web_address
        
        #preess ctrl w to close window
        print("Closing window")
        pyautogui.hotkey('ctrl', 'w')
        
        
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        print(f"Writing to {part_number}")
        with open(file_name, 'w') as file:
            yaml.dump(data, file)
    else:
        print(f"File already exists {part_number}")


def grab_part_info(part_number):
    directory_output = "temporary/distributor_page_orbital_fasteners"
    file_name = f"{directory_output}/{part_number}.yaml"
    with open(file_name, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    delay_long = 5
    #delay_long = 2

    delay_short = 2
    #delay_short = 1

    file_output = "output_distributor_orbital_fasteners.csv"
    
    page = data["page"]
    #make upper case    
    page = page.upper()


    prices = {}
    prices[1] = {}
    prices[1]["start_string"] = ["1 - 199 ","1 - 99 ","1 - 499 ", "1 - 999 ", "1 - 1999 ", "1 - 49 ", "1 - 99 "]
    prices[1]["end_string"] = "INC. VAT"   #prices[1]["end_string"] = " INC. VAT"
    prices[100] = {}
    prices[100]["start_string"] = ["100 - 499 ", "1 - 199 ", "1 - 499 ", "1 - 999 ", "1 - 1999 ", "50 - 249 ", "100 -499 "]
    prices[100]["end_string"] = "INC. VAT" #prices[100]["end_string"] = " INC. VAT"
    prices[200] = {}
    prices[200]["start_string"] = ["200 - 999 ", "100 - 499 ", "1 - 999 ", "1 - 499 ", "1 - 1999 ", "50 - 249 " ]
    prices[200]["end_string"] = "INC. VAT" #prices[200]["end_string"] = " INC. VAT"
    prices[1000] = {}
    prices[1000]["start_string"] = ["1000 - ", "1000+", "500 - 2499 ", "1000 - 4999", "1 - 1999 ", "300+", "800+", "600+"]
    prices[1000]["end_string"] = "INC. VAT"   #prices[1000]["end_string"] = " INC. VAT"
    prices[10000] = {}
    prices[10000]["start_string"] = ["4800+","1000+", "3000+", "5000 - 24999", "5000+", "10000 - 63999", "4000+", "1000 - 8999999", "2400+", "300+", "800+", "2000+", "1600", "6000+", "1200+", "8000+", "9000+", "600+"]
    prices[10000]["end_string"] = "INC. VAT"       #prices[10000]["end_string"] = " INC. VAT"
    

    try:
        print("Clipping Text")
        text_between_start = "Qty	Price per unit	Price per 100 units".upper()
        text_between_end = "Pricing help".upper()
        price_clip = page.split(text_between_start)[1].split(text_between_end)[0]
        price_clip = price_clip.replace("\t"," ")
        price_clip = price_clip.split("\n")
    except:
        print(f"Error clipping text for {part_number}")
        #delay 30 seconds
        time.sleep(30)



    print("Grabbing Prices")
    for qty in prices:
        start_strings = prices[qty]["start_string"]
        #if start_string isn't an array make it one
        if not isinstance(start_strings,list):
            start_strings = [start_strings]
        for start_string in start_strings:
            price = "none"
            if price == "none":
                end_string = prices[qty]["end_string"]
                for line in price_clip:
                    line = line.upper()
                    if start_string in line:
                        price = line.split(start_string)[1].split(end_string)[0]
                        #price is from £ to end
                        price = price.split("£")[1]
                        price = price.replace("£","")
                        price = price.replace(" ","")
                        prices[qty]["price"] = price
                        print(f"    Price for {qty} is {price}")
                        pass
                        break

    pass

    

    web_address = data["web_address"]
    #remove trailing ? and everything after it
    if "?" in web_address:
        web_address = web_address.split("?")[0]

    #add to csv
    print("Writing to csv")
    if not os.path.exists(file_output): ##### always remake file
        with open(file_output, 'w') as file:
            file.write("part_number_distributor_orbital_fasteners,price_1_distributor_orbital_fasteners,price_100_distributor_orbital_fasteners,price_200_distributor_orbital_fasteners,price_1000_distributor_orbital_fasteners,price_10000_distributor_orbital_fasteners,link_distributor_orbital_fasteners\n")
    with open(file_output, 'a') as file:
        #use get and default to none
        price_1 = prices.get(1,{}).get("price","none")
        price_100 = prices.get(100,{}).get("price","none")
        price_200 = prices.get(200,{}).get("price","none")
        price_1000 = prices.get(1000,{}).get("price","none")
        price_10000 = prices.get(10000,{}).get("price","none")

        #if a price is none make it the next price that isn't none
        if price_1000 == "none":
            price_1000 = price_10000
        if price_200 == "none":
            price_200 = price_1000
        if price_100 == "none":
            price_100 = price_200
        if price_1 == "none":
            price_1 = price_100
        

        file.write(f"{part_number},{price_1},{price_100},{price_200},{price_1000},{price_10000},{web_address}\n")
        
    







if __name__ == "__main__":
    kwargs = {}
    main(**kwargs)