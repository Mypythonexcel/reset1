from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
import csv
# Setting up Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.set_capability("goog:loggingPrefs", {"browser": "INFO"})
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Initialize WebDriver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.kayak.co.in/flights/")

# Wait for the input field to load
time.sleep(5)
def click_show_more():
    while True:
        try:
            time.sleep(10)
            # Wait until the button is present and clickable
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ULvh-button"))
            )
            button.click() 
            print("show more button is clicked")
            time.sleep(2)  # Wait for the content to load after clicking
        except Exception as e:
            print("No more results to show or an error occurred:")
            break  


# Locate the destination input field by placeholder 'To?'
try:
    delhi_remove_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@class="c_neb-item-value" and text()="New Delhi (DEL)"]/following-sibling::div//div[@class="c_neb-item-button"]'))
    )
    
    # Click the remove button to clear "New Delhi (DEL)"
    delhi_remove_button.click()
    print("Removed 'New Delhi (DEL)' successfully.")
    time.sleep(2)  # Short pause to let the UI update
    
    # Now interact with the origin input field to add a new city
    origin_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Flight origin input"]'))
    )
    
    # Click the input field to focus on it
    origin_input.click()
    time.sleep(1)
    
    # Input the new origin city, e.g., "Mumbai"
    origin_input.send_keys("Mumbai")
    time.sleep(2)  # Wait for the autocomplete dropdown to appear
    
    # Simulate pressing the Enter key to select the city
    origin_input.send_keys(Keys.RETURN)
    
    print("Successfully selected Mumbai as the new origin!")

    
    print("Successfully selected Mumbai as the origin!")
    

    # Wait until the destination input field is present
    destination_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='To?']"))
    )

    destination_input.click()
    time.sleep(1)  

    destination_input.send_keys("Jaipur")
    time.sleep(5)  # Pause for a moment to let the dropdown load

    # Simulate pressing Enter
    destination_input.send_keys(Keys.RETURN)

    print("Successfully selected Jaipur, Rajasthan, India (JAI) from the dropdown!")
    
    # Wait for the search button to be visible and click it
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='RxNS-button-container']"))
    )
    search_button.click()

    # Wait for results to load
    time.sleep(20)
    # Call the function to click the button
    click_show_more()
    
    flights = driver.find_elements(By.CLASS_NAME, 'hJSA-item')
    flight_data_list=[]
    for flight in flights:
        airline = flight.find_element(By.CLASS_NAME, 'c5iUd-leg-carrier').find_element(By.TAG_NAME, 'img').get_attribute('alt')
        departure_time = flight.find_element(By.XPATH, './/div[contains(@class, "vmXl")][1]/span[1]').text
        arrival_time = flight.find_element(By.XPATH, './/div[contains(@class, "vmXl")][1]/span[3]').text
        start_destination = flight.find_element(By.XPATH, './/div[contains(@class, "c_cgF")][1]/span[1]').text
        end_destination = flight.find_element(By.XPATH, './/div[contains(@class, "c_cgF")][2]/span[1]').text
        duration = flight.find_element(By.XPATH, './/div[contains(@class, "xdW8-mod-full-airport")]/div[contains(@class, "vmXl")]').text
        stops = flight.find_element(By.CLASS_NAME, 'JWEO-stops-text').text
        price = driver.find_element(By.CLASS_NAME, 'f8F1-price-text').text
        # Extracting the economy class
        flight_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, './/a[contains(@class, "Iqt3") and @role="link"]'))
        ).get_attribute('href')

        economy_class = driver.find_element(By.CLASS_NAME, 'DOum-name').get_attribute('title')
        data = {
            "Airline": airline,
            "Departure Time": departure_time,
            "Arrival Time": arrival_time,
            "Start Destination": start_destination,
            "End Destination": end_destination,
            "Duration": duration,
            "Stops": stops,
            "Price": price,
             "flight_link":flight_link,
            "Economy Class": economy_class
            }
        flight_data_list.append(data)

        # Save the flight data to a CSV file
    csv_file_path = 'flight_data.csv'
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()  # Write the header
        for flight_data in flight_data_list:
            writer.writerow(flight_data)

    print(f"Flight data saved to {csv_file_path}")



except Exception as e:
    print(f"An error occurred: {e}")
finally:
    time.sleep(5)  # Allow some time to observe the result before quitting
    driver.quit()
