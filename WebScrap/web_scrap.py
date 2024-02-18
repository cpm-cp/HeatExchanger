from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from WebScrap.WebDriverPath import WebDriverPath # Personal path
from bs4 import BeautifulSoup
import numpy as np
from time import sleep

def find_and_send_keys(driver, locator, value):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, locator))
        )
        element.clear()
        element.send_keys(str(value))
    except TimeoutException:
        print(f'Element with name: {locator} not found at time.')


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

def get_water_thermophysic_info(low_temperature: float, high_temperature: float) -> np.ndarray:

    # My personal WebDriver path (Edge)
    driver_path = WebDriverPath

    # Path route
    PATH = 'https://webbook.nist.gov/cgi/fluid.cgi?ID=C7732185&TUnit=K&PUnit=atm&DUnit=kg%2Fm3&HUnit=kJ%2Fmol&WUnit=m%2Fs&VisUnit=Pa*s&STUnit=N%2Fm&Type=IsoBar&RefState=DEF&Action=Page'

    # WebDriver instance (Edge)
    service = Service(executable_path=driver_path)

    driver = None
    try:
        # Instance, Edge browser.
        driver = webdriver.Edge(service=service)
        
        # Init the web page.
        driver.get(PATH)

        filled_parameters(driver=driver, low_temperature=low_temperature, high_temperature=high_temperature)

    
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, 'tbody'))
            )
        except TimeoutException:
            print('The result table failed to load in time.')
            return np.array([0.0, 0.0, 0.0, 0.0])  # Maintain consistent return type

        # Extract page source and parse it
        page_src = driver.page_source
        soup = BeautifulSoup(page_src, 'html.parser')

        try:
            rows = soup.find_all('tr', {'align': 'right'})
            if rows and len(rows) > 1:
                data_row = rows[1].find_all('td')  # Assuming you're interested in the second row of data
                
                # Debugging: print the text of each data cell
                print("Extracted data:", [td.text for td in data_row])
                
                values = np.array([float(data_row[i].text) for i in [2, 3, 11, 12]])
                return values
            else:
                print('Values or table not found.')
                return np.array([0.0, 0.0, 0.0, 0.0])
        except ValueError as e:
            print(f"Error converting data to float: {e}")
            return np.array([0.0, 0.0, 0.0, 0.0])
    finally:
        if driver:
            sleep(2)  # Just to make sure everything loads properly.
            driver.quit()