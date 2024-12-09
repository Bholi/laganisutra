from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service
from subindices.models import SubIndices
import datetime

class Command(BaseCommand):
    help = 'Scrape Sub Indices data and save it to the database'

    def handle(self, *args, **kwargs):
        # Set up the WebDriver
        service = Service('/opt/homebrew/bin/chromedriver')  # Adjust the path to your chromedriver
        driver = webdriver.Chrome(service=service)

        try:
            # Open the website
            driver.get("https://nepalstock.com/")

            # Wait for the page to load
            wait = WebDriverWait(driver, 15)

            # Click on the menu icon
            menu_icon = wait.until(EC.element_to_be_clickable((By.ID, "index__more")))
            menu_icon.click()

            # Wait and click on the "Sub Indices" tab
            sub_indices_tab = wait.until(EC.element_to_be_clickable((By.ID, "subindex-tab")))
            sub_indices_tab.click()
            time.sleep(5)

            # Wait for the table rows to load
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#subindex table.table tbody tr")))

            # Find the table rows
            table = driver.find_element(By.CSS_SELECTOR, "#subindex table.table")
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

            # Extract the table data
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                if columns and len(columns) == 4:
                    symbol = columns[0].text.strip()
                    current = columns[1].text.strip()
                    change = float(columns[2].text.strip()) if columns[2].text.strip() else None
                    percent_change = float(columns[3].text.strip().replace('%', '')) if columns[3].text.strip() else None

                    # Save to the database
                    SubIndices.objects.update_or_create(
                        indices=symbol,
                        date=datetime.date.today(),
                        defaults={
                            'current': current,
                            'change': change,
                            'percent_change': percent_change,
                        }
                    )

            self.stdout.write(self.style.SUCCESS('Successfully scraped and saved data to the database.'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error occurred: {e}'))

        finally:
            # Close the WebDriver
            driver.quit()
