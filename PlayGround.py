import os
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from random import randint
wait = randint(1,6)

# Function to download PDF files from a webpage
def download_pdf_files(url, download_dir):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links on the page
        links = soup.find_all('a')

        # Filter out links that point to PDF files
        pdf_links = [link.get('href') for link in links if link.get('href') and link.get('href').endswith('.pdf')]

        # Download each PDF file
        for pdf_link in pdf_links:
            # Construct the absolute URL if it's a relative URL
            pdf_url = urljoin(url, pdf_link)

            # Extract the filename from the URL
            filename = os.path.basename(pdf_url)

            # Check if the filename starts with "0971_"
            if filename.startswith('0971_'):
                print(f"Skipped: {filename}")
                continue

            # Download the PDF file
            with open(os.path.join(download_dir, filename), 'wb') as f:
                pdf_response = requests.get(pdf_url)
                f.write(pdf_response.content)

            print(f"Downloaded: {filename}")

            # Wait for 15 seconds
            time.sleep(wait)

    else:
        print("Failed to fetch the webpage.")

# Example usage:
url = 'https://www.savemyexams.com/igcse/chemistry/cie/-/pages/past-papers/'  # Replace with the URL of the webpage containing PDF files
download_dir = 'E:\Python_Scrapping\pdf_basement'    # Directory where PDF files will be saved

# Create the download directory if it doesn't exist
os.makedirs(download_dir, exist_ok=True)

# Call the function to download PDF files from the webpage
download_pdf_files(url, download_dir)
