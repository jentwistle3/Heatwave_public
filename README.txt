README file for NY Heatwave Analysis

Overview
Python scripts are used to pull the data from the source sites and save locally in a CSV file.
The two sites used are:
    1 - High Plains Regional Climate Center: High Plains Regional Climate Center - CLIMOD (unl.edu)  at the University of Nebraska Lincoln. This site has a good data set for New York’s Central Park. 
    2 - Cornell University:  weather.nysaes.cals.cornell.edu/history/ has records taken at their experimental farm outside of Geneva, NY. 


To analyze the data I used python 3 scripts inside a Jypiter notebook running in Anaconda. Anaconda is a Python distribution and application 
dashboard which gives you both Python and Jypiter, as well as other interesting tools, in one download.

Anaconda can be obtained here: https://docs.anaconda.com/anaconda/navigator/

I used Pandas for most of the analysis. Pandas is a powerful Python tool for data manipulation and analysis. 
I used Matplotlib for the charts. Matplotlib https://matplotlib.org/ is a comprehensive library for creating data visualizations in Python. 

Matplotlib and Pandas must be installed once you have Anaconda running. Instructions to do this 
can be found here:

Pandas: https://docs.anaconda.com/anaconda/navigator/tutorials/pandas/
Matplotlib: https://anaconda.org/conda-forge/matplotlib

The data pulling scripts use Selenium, a test automation library, to scrape the temperature data
from these sites. 

Selenium is here: https://www.selenium.dev/
Selenium packages for Anaconda can be found here: https://anaconda.org/conda-forge/selenium

Selenium in turn uses an internet browser, the "driver", to access the web site.
I used chromedriver which can be obtained here: https://chromedriver.chromium.org/downloads

The total list of libraries used is:
selenium webdriver
selenium common
selenium.common.exceptions TimeoutException
selenium.webdriver.support.ui WebDriverWait, expected_conditions
selenium.webdriver.common.by By
datetime datetime
time sleep
sys
sys exc_info
csv

With the exception of Selenium, chromedriver, matplotlib and pandas these are all standard Python 3 libraries.

The process is:
Install Anaconda
Install chromedriver
Install Pandas
Install Matplotlib

To pull the data:
configure climod.py
           climod.py is designed to pull from any of the climod data sets. Using Selenium it steps through the climod GUI menus
           setting search parameters and ultimately requesting a data set over a date range.  I experimented pulling data from 
           a half dozen climod locations: Houston, NY Central Park, Elmira NY, Jefferson City, MO, and Columbus OH.
           Ultimately I only used the data from NY Central Park for this analysis.
           To configure climod.py to pull the data from NY Central Park set the "location_index" variable equal to 1
           
           Alternatively you can skip this step and use the data file in this repository: NYCentralPark.csv. NB this file starts in 1/1/1900 and 
           runs to 7/31/2020, the analyis process will drop the 2020 data in order to align all years.

start_date = "1900-01-01"
end_date = "2019-12-31"
tempregion = ["Houston, TX", "new york", "elmira", "jefferson city", "columbus oh"] #this will be a list
file_list = ["HoustonTX", "NYCentralPark", "Elmira", "JeffersonCity", "ColumbusOH"]
station = ["/html/body/div[2]/div[2]/div[3]/div/div[2]/fieldset/select/option[text()='HOUSTON WB CITY']",\
           "/html/body/div[2]/div[2]/div[3]/div/div[2]/fieldset/select/option[text()='NY CITY CENTRAL PARK']",\
           "/html/body/div[2]/div[2]/div[3]/div/div[2]/fieldset/select/option[text()='ELMIRA']",\
           "/html/body/div[2]/div[2]/div[3]/div/div[2]/fieldset/select/option[text()='JEFFERSON CITY WTR PL']",\
           "/html/body/div[2]/div[2]/div[3]/div/div[2]/fieldset/select/option[18]"]
location_index = 1

Run climod.py if desired

Run cornelltoCSV.py This will pull the data from the Cornell CALS website. You can also skip this step and use the data file 
in this repository: cornellu.csv

Once you have the data in the form of the two .CSV files NYCentralPark.csv and cornellu.csv you can run the analysis.

Start Anaconda
Start Jypiter from the Anaconda menu
Open CornellU.ipynb. This is a Jypiter notebook containing the python scripts which perform the calculations and generate the plots.
Run each cell sequentially top to bottom.
Once you've run the Cornell notebook, repeat the process with NYCentralPark.ipynb.
At this point you'll have access to all the data and all the charts via the Jypiter notebooks and the files saved on your hard drive.

Have fun.
John


