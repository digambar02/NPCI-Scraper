# NPCI Data Scraper

This script is designed to scrape data from the National Payments Corporation of India (NPCI) website for various products. It navigates through different products, years, and months, and retrieves relevant data for each combination.

## Requirements

- Python 3
- Selenium
- Pandas

## Installation

1. Clone the repository:

    git clone https://github.com/digambar02/NPCI_Scraper.git

2. Install the required dependencies:
   
    pip install -r requirements.txt

4. Download the appropriate WebDriver for Firefox. You can download the geckodriver from [here](https://github.com/mozilla/geckodriver/releases) and place it in the repository folder.

## Usage

1. Run the script:

    npci_scraper.py

2. The script will navigate to the NPCI website, select different products, years, and months, and retrieve data for each combination.

3. The scraped data will be stored in a DataFrame and saved to a CSV file.

## Contributors

- [Digambar Dagade](https://github.com/digambar02)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
