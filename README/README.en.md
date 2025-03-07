# Search_n_Find

**Automates the search and collection of company information on Google for database registration and contact validation via WhatsApp Web.**

# **Updated with GUI.**

![ScrapingMaps](https://github.com/user-attachments/assets/b8174ba4-df1c-473a-a459-2c0c522b2906)

## Requirements
- Python installed
- A MySQL database configured with two tables:
  - **Cities Table**: Containing the 5,570 cities of Brazil.
  - **Results Table**: To store the collected information (such as name, phone number, and validation status of the contacts).

## Usage Instructions

1. **Install the Libraries**
   - Run the `install_libraries.cmd` script. This script will install the necessary libraries and ask if you want to start the application.

2. **Start the Application**
   - After installation, you can start the application by running the `run_script.vbs` script.

3. **Configure DB Connection**
   - Place your credentials in `connect.py`:
     - (host=' ', user=' ', password=' ', database=' ', port=' ')
   - Create the tables as specified in the code.

## Project Structure
The project has three main scripts and one connection script:

   - **validador.py**: Automates the validation of contacts via WhatsApp Web and updates the database to only include valid WhatsApp numbers.
   - **searchPainel.py**: GUI for configuring the scraping (Front-End of the system).
   - **searchScript.txt**: Search file for the scraping (Back-End of the system).
      - **connect.py**: Contains the function to establish and reconnect the connection to the MySQL database (All scripts depend on it).

## Project Features
   - Searches the term you specify in all cities of Brazil, according to your database, returning all respective companies, with name, phone, address, and all found data.
   - Filters and selects only numbers with valid WhatsApp (the system doesn't guarantee that it's the correct company number, it just collects them from Google).
   - Sends a notification via Telegram at the end of the script execution or if any errors occur.

> **Note:** The code for creating the tables is not included in this repository for ethical reasons. Make sure to configure the database as needed.

## License
This portfolio is licensed under the [MIT License](LICENSE).
