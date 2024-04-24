import csv
import time
import re
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Read addresses from csv
addresses = []
with open('TestFile.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        addresses.extend(row)

options = Options()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

driver.get("https://www.greatschools.org/")

# Initialize empty lists to store data
elementary_schools = []
elementary_ratings = []
middle_schools = []
middle_ratings = []
high_schools = []
high_ratings = []

for address in addresses:
    input_element = driver.find_element(By.ID, "where-js")
    input_element.clear()

    # Type the address character by character
    for char in address:
        input_element.send_keys(char)
        time.sleep(0.1)  # Adjust timing if needed

    time.sleep(5)  # Adjust timing if needed

    # Now, you can proceed with clicking on the primary details or any other actions
    list_element = driver.find_element(
        By.CLASS_NAME, 'primary-details').click()

    time.sleep(3)  # Adjust timing if needed

    # Find and click on the search button if necessary
    search_element = driver.find_element(
        By.CLASS_NAME, 'search_container_icon_image')
    search_element.click()

    time.sleep(5)  # Adjust timing if needed

    cards = driver.find_elements(By.CLASS_NAME, 'assigned')
    for card in cards:
        # Find only the first assigned school for each type
        if not elementary_schools and not elementary_ratings:
            for school, rating in zip(card.find_elements(By.CLASS_NAME, 'header'), card.find_elements(By.CLASS_NAME, 'gs-rating')):
                elementary_schools.append(school.text)
                # Extract the first number from rating
                rating_number = re.search(r'\d+', rating.text).group()
                elementary_ratings.append(rating_number)
        elif not middle_schools and not middle_ratings:
            for school, rating in zip(card.find_elements(By.CLASS_NAME, 'header'), card.find_elements(By.CLASS_NAME, 'gs-rating')):
                middle_schools.append(school.text)
                # Extract the first number from rating
                rating_number = re.search(r'\d+', rating.text).group()
                middle_ratings.append(rating_number)
        elif not high_schools and not high_ratings:
            for school, rating in zip(card.find_elements(By.CLASS_NAME, 'header'), card.find_elements(By.CLASS_NAME, 'gs-rating')):
                high_schools.append(school.text)
                # Extract the first number from rating
                rating_number = re.search(r'\d+', rating.text).group()
                high_ratings.append(rating_number)
        else:
            break  # Exit the loop if all data has been captured

# Create a DataFrame
data = {
    'Elementary School Name': elementary_schools,
    'Elementary School Rating': elementary_ratings,
    'Middle School Name': middle_schools,
    'Middle School Rating': middle_ratings,
    'High School Name': high_schools,
    'High School Rating': high_ratings
}
print(data)
df = pd.DataFrame(data)
# Export to Excel
df.to_excel('school_data.xlsx', index=False)
