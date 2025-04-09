# Exhibitor Directory Scraper and Viewer

This project consists of two main components:

1. **scraper.py:** A Python script that uses Selenium (with BeautifulSoup) to extract exhibitor data from the website and store it in an SQLite database.
2. **app.py:** A Flask application that retrieves the data from the SQLite database and displays it in a professional, searchable, and sortable web interface.
3. **requirements.txt:** A list of the Python dependencies required to run the project.

## Project Overview

### Scraper (`scraper.py`)
- **Purpose:** Extracts data from the [Exhibitor Directory](https://startupmahakumbh.org/Exhibitor-Directory.php) using headless Selenium and BeautifulSoup.
- **Functionality:**  
  - Loads the main page and switches to the target iframe.
  - Navigates through paginated pages using a combination of "Next" buttons and manual page number entry (with a fallback if timeouts occur).
  - Extracts details (Name, Address, Contact Person, Designation, Contact Details, Profile) from HTML elements.
  - Inserts the extracted data into an SQLite database (`exhibitors.db`).
- **Usage:**  
  Run the scraper from the command line:
  ```bash
  python scraper.py
  ```

### Flask Application (`app.py`)
- **Purpose:** Provides a web interface to view the exhibitor data stored in the SQLite database.
- **Features:**  
  - Retrieves all records from the `exhibitors` table.
  - Displays the data in a professional web interface using Bootstrap and DataTables.
  - Supports sorting and filtering for easy lookup.
- **Usage:**  
  Start the Flask app from the command line:
  ```bash
  python app.py
  ```
  Then open your browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to view the directory.

### Python Dependencies (`requirements.txt`)
The following dependencies are required:
- Flask
- selenium
- beautifulsoup4
- lxml

Install them using pip:
```bash
pip install -r requirements.txt
```

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/rdinesh207/Experita_Task1.git
   cd Experita_Task1
   ```

2. **Create a Virtual Environment (optional, recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Scraper**
   ```bash
   python scraper.py
   ```
   This will create/update the `exhibitors.db` file with the scraped data.

5. **Run the Flask Application**
   ```bash
   python app.py
   ```
   Open your browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to view the data.

## Notes

- **Web Driver:** Make sure you have the appropriate Chrome WebDriver installed and available in your PATH. The version should match your installed Chrome browser.
- **Database:** Running `scraper.py` will overwrite previous data in `exhibitors.db`. Ensure that you have backups if necessary.
- **Error Handling:** The scraper includes a fallback mechanism if the pagination fails to update. Check the console output for any error messages.

## Acknowledgements

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [DataTables](https://datatables.net/)
