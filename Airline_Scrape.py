import csv
from selenium import webdriver
from bs4 import BeautifulSoup

# Function to scrape data from a single page
def scrape_page(url):
    # Use Selenium to open the webpage and get the HTML content after dynamic loading
    driver = webdriver.Chrome()  # You'll need to have the ChromeDriver executable in your path
    driver.get(url)

    # Wait for some time to allow dynamic content to load (you might need to adjust this)
    driver.implicitly_wait(10)

    # Get the page source after dynamic loading
    html_content = driver.page_source

    # Close the Selenium WebDriver
    driver.quit()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all rows with the class "tabcontent2"
    rows = soup.find_all('tr', class_='tabcontent2')

    # Create a list to store the data
    data_list = []

    # Check if any rows are found
    if rows:
        # Iterate through the rows
        for row in rows:
            # Extract relevant information from each cell
            cells = row.find_all('td')
            msn = cells[0].get_text(strip=True)
            aircraft_type = cells[1].get_text(strip=True)
            airline = cells[2].get_text(strip=True)
            first_flight = cells[3].get_text(strip=True)
            registration = cells[4].get_text(strip=True)
            status = cells[5].get_text(strip=True)

            # Append the data to the list
            data_list.append([msn, aircraft_type, airline, first_flight, registration, status])

    return data_list

# Iterate over all 15 pages
all_data = []

#Change the url listing to the correct plane number and auto adjust the page number to the number of pages to the table
for page_number in range(1, 16):
    page_url = f"https://www.airfleets.net/listing/a321-{page_number}-typedesc.htm"
    page_data = scrape_page(page_url)
    all_data.extend(page_data)

# Write the data to a CSV file ADJUST FILE NAME TOO
csv_filename = "airfleets_data_321.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write the header
    csv_writer.writerow(["MSN", "Type", "Airline", "First Flight", "Registration", "Status"])
    
    # Write the data
    csv_writer.writerows(all_data)

print(f"Data has been written to {csv_filename}.")
