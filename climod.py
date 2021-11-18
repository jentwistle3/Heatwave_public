"""
This script parses the University of Nebraska High Plains RCC CLIMOD and scrapes temperature data for a list of locations

"""
from selenium import webdriver
from selenium import common
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep
import sys
from sys import exc_info
import csv

def init_webdriver(a_url, page_title):
    a_driver = webdriver.Chrome()
    a_driver.get(a_url)
    try:
        WebDriverWait(a_driver, 10).until(EC.title_contains(page_title))
        print(a_driver.title)
    except TimeoutException:
        print("Page timed out")
        a_driver.close()
        quit()
    sleep(1)
    return a_driver

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


weather_url = "http://climod.unl.edu/"
first_page_title = "High Plains Regional Climate Center - CLIMOD"
filename = "CLIMOD"
start_date = "1917-01-01"
end_date = "2019-12-31"
tempregion = ["Houston, TX", "new york", "elmira", "jefferson city", "columbus oh"] #this will be a list
file_list = ["HoustonTX", "NYCentralPark", "Elmira", "JeffersonCity", "ColumbusOH"]
station = ["/html/body/div[2]/div[2]/div[3]/div/div[2]/fieldset/select/option[text()='HOUSTON WB CITY']",\
           "/html/body/div[2]/div[2]/div[3]/div/div[2]/fieldset/select/option[text()='NY CITY CENTRAL PARK']",\
           "/html/body/div[2]/div[2]/div[3]/div/div[2]/fieldset/select/option[text()='ELMIRA']",\
           "/html/body/div[2]/div[2]/div[3]/div/div[2]/fieldset/select/option[text()='JEFFERSON CITY WTR PL']",\
           "/html/body/div[2]/div[2]/div[3]/div/div[2]/fieldset/select/option[18]"]
location_index = 4

if __name__ == "__main__":
    
# scrape the main page and get the historical weather table
# find the links to the daily summaries
  #  print(datetime.now().strftime("%H:%M:%S"))
 #   sys.stdout = open(f'{filename}analysis.txt', 'w') #put the error info into a text file for reference
    print(f"{filename} Daily Temperature Records")
    print(datetime.now().strftime("%H:%M:%S"))
    links_list = []
    driver = init_webdriver(weather_url, first_page_title)
    product_selector = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/table[1]/tbody/tr[4]/td')
    product_selector.click()
    sleep(.5)
    
    csvselector = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/fieldset/input[2]')
    csvselector.click()
    sleep(.5)
    
    start_date_field = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/fieldset[1]/input')
    start_date_field.clear()
    sleep(.5)
    start_date_field.send_keys(start_date)
    sleep(.5)
    
    end_date_field = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/fieldset[2]/input')
    end_date_field.clear()
    sleep(.5)
    end_date_field.send_keys(end_date)
    sleep(.5)
    
    #turn off the fields which are default on which we don't want
    precip_cb = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[6]/td[2]/input')
    sleep(.5)
    precip_cb.click()
    sleep(.5)
    
    snowfall_cb = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[7]/td[2]/input')
    sleep(.5)
    snowfall_cb.click()
    sleep(.5)
    
    snowdepth_cb = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[8]/td[2]/input')
    sleep(.5)
    snowdepth_cb.click()    
    
    stationarea = driver.find_element_by_xpath('/html/body/div[2]/div[2]/h3[3]/span')
    sleep(.5)
    stationarea.click()
    sleep(.5)
    
    #enter the region
    #loop through the list of regions and sites requesting data for each 
    #and storing as a csv

    region = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div/div[2]/div/input')
    sleep(.5)
    region.clear()
    region.send_keys(tempregion[location_index])
    sleep(.5)
    
    search_button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div/div[2]/div/div')
    sleep(.5)
    search_button.click()
    sleep(4)
    
    driver.find_element_by_xpath(station[location_index]).click()
    sleep(.5)
    
    go_button = driver.find_element_by_xpath('/html/body/div[2]/div[3]/button[1]')
    sleep(.5)
    go_button.click()
    sleep(60)
    
    data_block0 = driver.find_element_by_id('results_area')
    data_block1 = driver.find_element_by_tag_name('pre')
    data_set = (data_block1.text).split("\n") # get rows of text

    driver.close()

    print(data_set.pop(0))
    data_set.pop(0)
    data_set.pop(0)
    total_count = len(data_set)
    bad_high_count = 0
    bad_low_count = 0
    printed = False
    new_rows = [row.split(",") for row in data_set]
    for index in range(0, total_count):
#        print(new_rows[index])
        new_rows[index][1] = new_rows[index][1].lstrip()
        new_rows[index][2] = new_rows[index][2].lstrip()
#        print(new_rows[index])
        try:
            x = float(new_rows[index][1])
        except:
                bad_high_count += 1
                print(new_rows[index])
                printed = True
        try:
            y = float(new_rows[index][2])
        except:
                bad_low_count += 1
                if not printed:
                    print(new_rows[index])
        printed = False    
  
    bh_pct = round((bad_high_count/total_count)*100, 2)
    bl_pct = round((bad_low_count/total_count)*100, 2)
    print(f"looked at all {total_count} rows, bad highs = {bad_high_count} {bh_pct}% bad lows = {bad_low_count} {bl_pct}%")

    with open(f"{file_list[location_index]}.csv", 'w', newline="\n") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(new_rows)
        csv_file.close()
    print(f'finished at {datetime.now().strftime("%H:%M:%S")}')
#    sys.stdout.close()    

    
 