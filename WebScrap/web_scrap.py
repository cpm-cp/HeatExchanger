from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from WebScrap.WebDriverPath import WebDriverPath, PATH # Personal path
from bs4 import BeautifulSoup
import numpy as np

def find_and_send_keys(driver, locator, value):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, locator))
        )
        element.clear()
        element.send_keys(str(value))
    except TimeoutException:
        print(f'Element with name: {locator} not found at time.')
    except NoSuchElementException:
        print(f'No element found with name: {locator}')

def filled_parameters(driver: webdriver.Edge, low_temperature: float, high_temperature:float):

    find_and_send_keys(driver, 'TLow', low_temperature)    # Low temperature
    find_and_send_keys(driver, 'THigh', high_temperature)  # High temperature
    find_and_send_keys(driver, 'P', 1.0)                   # Pressure (constant)
    find_and_send_keys(driver, 'TInc', 1)                  # Increment
    
    # Submit
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @value="Press for Data"]'))
        )
        submit_button.click()
    except TimeoutException:
        print('Button not found at time.')

def get_water_thermophysic_info(mean_Temperature:int) -> np.ndarray:
    # Path route
    path = PATH
    driver = None

    low_temperature = high_temperature = mean_Temperature

    try:
        driver = webdriver.Edge()
        
        driver.get(path) # Init the web page.

        filled_parameters(driver=driver, low_temperature=low_temperature, high_temperature=high_temperature)

        tag_name_table = 'tbody'
        tag_name_tr = 'tr'
        try:
            WebDriverWait(driver, 10).until(
            lambda d: len(d.find_element(By.TAG_NAME, tag_name_table).find_elements(By.TAG_NAME, tag_name_tr)) == 2
            )
            # Parse the web page with bs4
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find(tag_name_table)
            rows = table.find_all(tag_name_tr)
            
            if rows and len(rows) == 2:
                data_row = rows[1].find_all('td', {'align': 'right'})
                values = np.array([float(data_row[i].text) for i in [2, 8, 11, 12]])
                return values
            else:
                print('Values or table not found.')
                return np.array([0.0, 0.0, 0.0, 0.0]) 
        except TimeoutException:
            print(f'Time out for find the tags: {tag_name_table} and {tag_name_tr}')
    finally:
        if driver:
            driver.quit()