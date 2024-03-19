"""
Script to scrape data from NPCI website for various products.

This script navigates to the NPCI website, selects different products, years, and months, and retrieves data for each combination.

"""

# Import necessary libraries
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up Firefox WebDriver
from selenium.webdriver.firefox.service import Service
service = Service(executable_path="C:\\Users\\DIGAMBAR\\Desktop\\geckodriver.exe")
options = webdriver.FirefoxOptions()
options.binary_location = r"C:\\Program Files\\Mozilla Firefox\\firefox.exe"
driver = webdriver.Firefox(service=service, options=options)

# Initialize an empty DataFrame to store the retrieved data
full_data = pd.DataFrame()

# Loop through the available products on the NPCI website
for product_range in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
    
    # XPath to select the desired product
    select_product = f'/html/body/section[3]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/select/option[{product_range}]'
    try:
        # Click on the selected product
        driver.find_element(By.XPATH, select_product).click()
    except NoSuchElementException:
        print('No Product Available!')
    
    # Map product range to actual product names
    products_mapping = {
        1: 'UPI',
        2: 'IMPS',
        3: 'NETC',
        4: 'NFS',
        5: 'AePS - BHIM Aadhaar Pay',
        6: 'AePS - Cash Withdrawal',
        7: 'AePS - Funds Transfer',
        8: 'NACH - APBS',
        9: 'NACH - Credit',
        10: 'NACH - Debit',
        11: 'CTS'
    }
    product = products_mapping.get(product_range, 'Unknown')
    
    # Loop through the available years (2021 to 2024) on the NPCI website
    for year_range in range(1, 5):
        print(f'Year range is {year_range}')
        # XPath to select the desired year
        select_year = f'/html/body/section[3]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div[3]/div/select/option[{year_range}]'
        try:
            # Click on the selected year
            driver.find_element(By.XPATH, select_year).click()
        except NoSuchElementException:
            print('No Year Available!')

        # Loop through the available months for the selected year
        for month_range in range(1, 13):
            print(f'Month range is {month_range}')
            # XPath to select the desired month
            select_month = f'/html/body/section[3]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div[4]/div/select/option[{month_range}]'
            try:
                # Click on the selected month
                driver.find_element(By.XPATH, select_month).click()
                time.sleep(2)

                new_data = pd.DataFrame()
                
                # Loop through the available types of data (volumn and value) for each month
                for value_range in range(1, 3):
                    print(f'Value range is {value_range}')
                    select_volume_value = f'/html/body/section[3]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div[5]/div/select/option[{value_range}]'
                    try:
                        driver.find_element(By.XPATH, select_volume_value).click()
                    except NoSuchElementException:
                        print('No Value Available!')

                    # XPath to select the table containing the data
                    x_path = '//*[@id="divDailyProductStatisticsTableBody"]'
                    table = driver.find_element(By.CLASS_NAME, 'table-responsive')

                    # Extract text data from the table and split it into lines
                    data = table.text.split('\n')

                    # Skip the first and last lines as they contain headers and footers
                    data = data[1: len(data) - 1]
                    
                    # Initialize lists to store dates and values
                    dates = []
                    values = []
                    
                    # Parse each line of data
                    for item in data:
                        parts = item.split()
                        # Convert date string to datetime.date object
                        date_format = pd.to_datetime(' '.join(parts[:3])).date()
                        dates.append(date_format)
                        # Extract the numerical value and convert it to float
                        number = parts[3].replace(',', '')
                        values.append(float(number))

                    # Create a data frame for the current type of data (volume or value)
                    if value_range == 1:
                        temp = pd.DataFrame({'Date': dates, 'Volumn': values})
                        # Add the product information to the DataFrame
                        temp['Product'] = product
                        # Concatenate the data frame with the previous data
                        new_data = pd.concat([new_data, temp], axis=0)
                    else:
                        temp = pd.DataFrame({'Date': dates, 'Value': values})
                        # Add the product information to the DataFrame
                        temp['Product'] = product
                        # Merge the DataFrame with the previous data based on the date column
                        new_data = new_data.merge(temp, on='Date', how='left')

                # Concatenate the data frame for the current month with the previous month's data
                full_data = pd.concat([full_data, new_data], axis=0)
                
            except NoSuchElementException:
                print('No Month Available!')
