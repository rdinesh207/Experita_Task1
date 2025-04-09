import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# -----------------------
# Setup SQLite Database
# -----------------------
conn = sqlite3.connect("exhibitors.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS exhibitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        contact_person TEXT,
        designation TEXT,
        contact_details TEXT,
        profile TEXT
    )
''')
conn.commit()

# -----------------------
# Setup Selenium in Headless Mode
# -----------------------
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

# Open the main URL that contains the iframe
main_url = "https://startupmahakumbh.org/Exhibitor-Directory.php"
driver.get(main_url)

# Wait until the iframe is present, then switch context
try:
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@src='https://startupmahakumbh.org/exhibitor_directory/exhi_list_pub.php?event_name=sm&event_year=2025']"))
    )
    driver.switch_to.frame(iframe)
except Exception as e:
    print(f"Error locating or switching to iframe: {e}")
    driver.quit()
    exit()

# Wait for the pagination element inside the iframe to be loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "pagination7"))
)

# -----------------------
# Get Total Number of Pages
# -----------------------
file = open("exhibitors.txt", "w", encoding="utf-8")
file.write(driver.page_source)
file.close()
soup = BeautifulSoup(driver.page_source, "html.parser")
pagination_div = soup.find("div", class_="pagination7")
current_page_input = pagination_div.find("input", id="currentPage")
max_page = int(current_page_input["max"])
print(f"Total pages found: {max_page}")

# -----------------------
# Function to Extract Data from a <div class="details">
# -----------------------
def extract_details(details_div):
    # Extract the organization name from the <h2><a> tag
    h2_tag = details_div.find("h2")
    organization_name = ""
    if h2_tag:
        a_tag = h2_tag.find("a")
        organization_name = a_tag.get_text(strip=True) if a_tag else ""
    
    # Initialize variables
    org_name_from_p = ""
    address = ""
    contact_person = ""
    designation = ""
    contact_details = ""
    profile = ""
    
    # Iterate through each paragraph in the details div
    for p in details_div.find_all("p"):
        text = p.get_text(strip=True)
        if "Name of the Organization:" in text:
            org_name_from_p = text.split("Name of the Organization:")[1].strip()
        elif "Address:" in text:
            address = text.split("Address:")[1].strip()
        elif "Contact Person:" in text:
            contact_person = text.split("Contact Person:")[1].strip()
        elif "Designation:" in text:
            designation = text.split("Designation:")[1].strip()
        elif "Contact Details:" in text:
            contact_details = text.split("Contact Details:")[1].strip()
        elif "Profile:" in text:
            profile = text.split("Profile:")[1].strip()
    
    final_name = organization_name if organization_name else org_name_from_p
    return final_name, address, contact_person, designation, contact_details, profile

# -----------------------
# Loop Through All Pages inside the iframe
# -----------------------
for page in range(1, max_page + 1):
    print(f"Processing page {page} ...")
    
    if page > 1:
        # Locate the current page input element and the "Go" button
        current_page_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "currentPage"))
        )
        current_page_input.clear()
        current_page_input.send_keys(str(page))
        
        go_button = driver.find_element(By.XPATH, "//button[@onclick=\"gotoPage('go')\"]")
        go_button.click()
        
        # Wait for the updated page content (this may vary depending on the site)
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element_value((By.ID, "currentPage"), str(page))
        )
        time.sleep(1)  # short pause to ensure complete load

    # Get the current page source and use BeautifulSoup to parse
    soup = BeautifulSoup(driver.page_source, "html.parser")
    details_divs = soup.find_all("div", class_="details")
    
    # Extract details from each div and insert into the database
    for details in details_divs:
        name, address, contact_person, designation, contact_details, profile = extract_details(details)
        
        cursor.execute('''
            INSERT INTO exhibitors (name, address, contact_person, designation, contact_details, profile)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, address, contact_person, designation, contact_details, profile))
        conn.commit()
    
    # For pages which are not the last page, click the "Next" button.
    # try:
    #     WebDriverWait(driver, 100).until(
    #         EC.text_to_be_present_in_element_value((By.ID, "currentPage"), str(page))
    #     )
    # except:
    #     print(f"Timeout waiting for page {page}, attempting fallback.")
    #     # Fallback: Manually clear and type the page number and click "Go"
    current_page_input = driver.find_element(By.ID, "currentPage")
    current_page_input.clear()
    current_page_input.send_keys(str(page))
    go_button = driver.find_element(By.XPATH, "//button[@onclick=\"gotoPage('go')\"]")
    go_button.click()
    # Wait again for the update with a shorter timeout
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_value((By.ID, "currentPage"), str(page))
    )
    time.sleep(1)  # short pause to ensure complete load

# -----------------------
# Cleanup: Close Selenium and SQL Connection
# -----------------------
driver.quit()
conn.close()
print("Data extraction complete and saved to exhibitors.db")
