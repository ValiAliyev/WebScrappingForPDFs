import os
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from random import randint

WAIT_TIME_RANGE = (1, 6)
MIN_FILE_SIZE = 1024  # Minimum file size in bytes

def download_pdf_files(url, download_dir):
    try:
        response = requests.get(url)
        response.raise_for_status()  
    except requests.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.find_all('a')

    pdf_links = [link.get('href') for link in links if link.get('href') and link.get('href').endswith('.pdf')]

    for pdf_link in pdf_links:
        pdf_url = urljoin(url, pdf_link)
        filename = os.path.basename(pdf_url)

        try:
            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()  
            if len(pdf_response.content) < MIN_FILE_SIZE:
                print(f"Skipped: {filename} - File size too small")
                continue

            with open(os.path.join(download_dir, filename), 'wb') as f:
                f.write(pdf_response.content)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")
            continue

        wait_time = randint(*WAIT_TIME_RANGE)
        time.sleep(wait_time)

if __name__ == "__main__":
    url = 'https://www.savemyexams.com/a-level/chemistry/cie/-/pages/past-papers/'  
    download_dir = 'E:\Python_Scrapping\pdf_basement'    

    os.makedirs(download_dir, exist_ok=True)

    download_pdf_files(url, download_dir)
