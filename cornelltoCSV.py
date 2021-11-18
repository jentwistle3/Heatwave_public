"""
This script parses cornell university historical weather data and saves it in a CSV
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

filename = "cornellu"

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

cornell_weather_url = "http://weather.nysaes.cals.cornell.edu/history/"
first_page_title = "NYSAES Monthly Weather Summaries"

if __name__ == "__main__":
    
# scrape the main page and get the historical weather table
# find the links to the daily summaries
    print(datetime.now().strftime("%H:%M:%S"))
    links_list = []
    driver = init_webdriver(cornell_weather_url, first_page_title)
    w_table = driver.find_element_by_xpath('//*[@id="CS_Element_content"]/table')
    for table_row in w_table.find_elements_by_css_selector('tr'):
        for datelink in table_row.find_elements_by_css_selector('td'):
            try:
                link_var = datelink.find_element_by_css_selector('a')
                links_list.append(link_var.get_attribute('href'))
            except:
                pass
    daily_rows = []
    new_rows = []
    #go through the list of year - links and get each daily page
    for link in links_list:
        driver.get(link)
        sleep(1)
        print(driver.title)
        data_set_element = driver.find_element_by_tag_name("pre")
        data_set = data_set_element.text
        start_of_data = find_nth(data_set, "AA", 2)
        yearly_temps = data_set[start_of_data+36:] #skip the header
        daily_rows = yearly_temps.split("\n") #split out each day
        # it turns out that there are duplicate days in the data - looks like a 
        # keying mistake as the temps are different - so let's run through and
        # clean this up. 
        # format each day into date as yyyy-mm-dd, high, low
        # note there is a bunch of other data we're tossing
        last_day = ""

        for day in daily_rows:
            day_data = day.split(" ")
            if last_day == day_data[2]:
                print(f"Fixing duplicate day {day_data}")
                day_data[2] = str(int(day_data[2])+1)
            last_day = day_data[2]          
            day_date = f"{day_data[0]}-{day_data[1].zfill(2)}-{day_data[2].zfill(2)}"
            day_high = day_data[3]
            day_low = day_data[4]
            if day_high == "NA":
                continue
            else:
                db_data = (day_date, day_high, day_low)     
            new_rows.append(db_data)
            
        with open(f"{filename}.csv", 'w', newline="\n") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(new_rows) # <-  need to split the string into a set of values
            csv_file.close()
        print(f'finished at {datetime.now().strftime("%H:%M:%S")}')            

    driver.close()
    print(datetime.now().strftime("%H:%M:%S"))

    
 