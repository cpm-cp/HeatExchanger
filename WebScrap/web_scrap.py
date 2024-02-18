from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from WebScrap.WebDriverPath import WebDriverPath, PATH # Personal path
from bs4 import BeautifulSoup
import numpy as np
from time import sleep

def get_driver() -> webdriver.Edge:
    driver_path = WebDriverPath
    service = Service(executable_path=driver_path)
    driver_options = webdriver.EdgeOptions()
    driver = webdriver.Edge(service=service, options=driver_options)
    return driver

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

def get_water_thermophysic_info(low_temperature: float, high_temperature: float) -> np.ndarray:

    # Path route
    path = PATH
    driver = None

    try:
        driver = get_driver()
        
        driver.get(path) # Init the web page.

        filled_parameters(driver=driver, low_temperature=low_temperature, high_temperature=high_temperature)

        css_selector = 'table.small'
        try:
            WebDriverWait(driver, 20).until(
            lambda d: len(d.find_element(By.CSS_SELECTOR, css_selector).find_elements(By.TAG_NAME, "tr")) >= 2
            )
            # Ahora usamos BeautifulSoup para parsear la página
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find('table', class_='small')
            rows = table.find_all('tr', {'align': 'right'})
            
            if rows and len(rows) > 1:
                data_row = rows[1].find_all('td')
                values = np.array([float(data_row[i].text) for i in [2, 3, 11, 12]])
                return values
            else:
                print('Values or table not found.')
                return np.array([0.0, 0.0, 0.0, 0.0]) 
        except TimeoutException:
            print(f'Time out for select the selector: {css_selector}')
    finally:
        if driver:
            sleep(2)  # Just to make sure everything loads properly.
            driver.quit()