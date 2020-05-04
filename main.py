import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

import time
# chrome driver download it first.


def read_creds(folder_path):
	username = ""
	password = ""
	with open(folder_path, "r") as f:
		lines = f.readlines()
		username = lines[0]
		password = lines[1]

	return username, password

def login(driver, username, password):
	delay = 3
	driver.get('https://timesheet.ultimatix.net/timesheet/Login/bridge')
	driver.refresh()
	driver.refresh()
	print("Login process initiating...")
	#Find the username field
	username_element = driver.find_element_by_xpath("//input[@id='form1']")
	#fill the username
	username_element.send_keys(username)
	print("Filling Username...")
	#Submit username
	driver.find_element_by_xpath("//button[@id='proceed-button']").click()
	driver.implicitly_wait(10)
	
	# Active the password element
	driver.find_element_by_xpath("//*[@id='password-btn']").click()
	
	#Fill the Password
	print("Bypassing the passsword wait...")
	driver.execute_script("passwordValue()"	)
	username_element = driver.find_element_by_xpath("//input[@id='password-login']")
	#fill the password
	print("Filling Password...")
	username_element.send_keys(password)
	#Submit the password
	driver.implicitly_wait(10)
	print("Submitting the form...")
	driver.find_element_by_xpath("//*[@id='form-submit']").click()

def remove_shit(driver):
	wait = WebDriverWait(driver, 100)
	time.sleep(3)
	element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ultimatixAlertPopUp"]/div[4]/input')))
	print("Removing the ultimatix popup...")
	driver.find_element_by_xpath('//*[@id="ultimatixAlertPopUp"]/div[4]/input').click()
	
	time.sleep(3)
	#This is for debug for the first date of the month.
	driver.find_element_by_xpath("//a[contains(text(),'Change')]").click()
	#update the location
	time.sleep(5)
	print("Filling the location part1...")
	element_ = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='branch_lookup']/div[4]/div[1]/div[3]/table/tbody/tr[1]/td[2]/span/select")))
	element=driver.find_element_by_xpath("//*[@id='branch_lookup']/div[4]/div[1]/div[3]/table/tbody/tr[1]/td[2]/span/select")
	element.click()
	all_options = element.find_elements_by_tag_name("option")
	for option in all_options:
	    if  option.get_attribute("value") == "9999999999":
	    	# print("option: ", option)
	    	option.click()
	        break

	print("Filling the location part2...")
	#update the second location
	time.sleep(2)
	element=driver.find_element_by_xpath("//*[@id='branch_lookup']/div[4]/div[1]/div[3]/table/tbody/tr[3]/td[2]/span/select")
	element.click()
	for option in element.find_elements_by_tag_name('option'):
	    if option.text == '324186':
	        option.click() 
	        break
	
	#update 

	print("Updating useless form...")
	wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='branch_lookup']/div[6]/span[1]/button")))
	driver.find_element_by_xpath("//*[@id='branch_lookup']/div[6]/span[1]/button").click()

def copy_efforts(driver):
	wait = WebDriverWait(driver, 100)
	#Go to previous month..
	time.sleep(2)
	print("Switching to previous month...")
	wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layout_pageContent']/div/div/div[5]/div[1]/div[1]/div[1]")))
	element = driver.find_element_by_xpath("//*[@id='layout_pageContent']/div/div/div[5]/div[1]/div[1]/div[1]")
	element.click()
	time.sleep(2)
	#remove alert of prevvious date freeze.
	print("Accepting the alert for date freeze...")
	Alert(driver).accept()
	time.sleep(3)
	#remove ultimatix popup
	print("Removing the ultimatix popup...")
	driver.find_element_by_xpath('//*[@id="ultimatixAlertPopUp"]/div[4]/input').click()
	
	
	#select date with 9 hours.
	required_date = ""
	print("Selecting the right date to copy efforts...")
	all_dates = driver.find_elements_by_class_name("pastEffort")
	for date in all_dates:
		if date.get_property('innerText') == "9":
			required_date = date
	
	required_date.click()
	time.sleep(3)
	Alert(driver).accept()

	#Select the copy this effort to current month
	time.sleep(1)
	print("Copying efforts to current month option...")
	element = driver.find_element_by_xpath("//*[@id='copyDiv']/div[3]/span/input").click()
	#Submit 
	print("Submitting the form...")
	element = driver.find_element_by_xpath("//*[@id='layout_pageContent']/div/div/div[5]/div[2]/div[3]/div[8]/span[1]/input").click()
	Alert(driver).accept()
	#remove ultimatix popup
	time.sleep(3)
	print("Removing the ultimatix popup...")
	driver.find_element_by_xpath('//*[@id="ultimatixAlertPopUp"]/div[4]/input').click()
	time.sleep(2)
	#Go again to current month 
	print("Switching back to current month...")
	driver.find_element_by_xpath('//*[@id="nextMonthNormal"]').click()
	time.sleep(3)
	print("Accepting the alert for advance filling of timesheet...")
	Alert(driver).accept()
	#remove ultimatix popup
	time.sleep(3)
	print("Removing the ultimatix popup...")
	driver.find_element_by_xpath('//*[@id="ultimatixAlertPopUp"]/div[4]/input').click()




if __name__=="__main__":
	CHROMEDRIVER_PATH = './chromedriver'
	WINDOW_SIZE = "960,1080"
	chrome_options = Options()
	# chrome_options.add_argument("--headless")
	chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
	# chrome_options.add_argument('--no-sandbox')

	# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:4756")
	driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
							chrome_options=chrome_options
							)

	username, password = read_creds("creds.txt")
	# Step 1: open timsheet link in incognito and fill the signin form to login
	login(driver, username, password)
	# Step 2: fill that shitty form for location etc
	remove_shit(driver)
	#Step 3 Go to previous month select pastEffort class with innerText == 9 and copy efforts.
	copy_efforts(driver)
	#Step 4 end it
	print("Closing browser...")
	driver.close()