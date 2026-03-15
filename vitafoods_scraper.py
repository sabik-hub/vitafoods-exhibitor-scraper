import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def main():
        
    # -------- SETTINGS --------
    URL = "https://exhibitors.vitafoods.eu.com/live/figlobal/event46.jsp?site=47&type=company&eventid=598"

    # -------- START BROWSER --------
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.get(URL)

    # Give manual time to solve Cloudflare if needed
    print("Started browser... sleeping 10 seconds to ensure load/solve captcha.")
    time.sleep(10)



    i = 1
    # -------- CLICK "SHOW MORE RESULTS" UNTIL DONE --------
    print("Starting to load more exhibitors...")
    while True:
        try:
            # Use implicit wait inside loop or check for element
            button = driver.find_element(By.CSS_SELECTOR, ".paging .button")
            if not button.is_displayed():
                # If the button exists but isn't visible, we might be at the end
                break

            driver.execute_script("arguments[0].click();", button)
            print(f"Clicked 'Load More' button {i} time(s)")
            time.sleep(2)
            i += 1
        except (TimeoutException, NoSuchElementException) as e:
            print("No more pagination button found.")
            break

    print("All exhibitors loaded in the browser!")



    # -------- PARSE PAGE --------
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select(".exhibitor")
    print(f"Found {len(cards)} exhibitor profiles!")

    data = []

    for card in cards:
        # Company name
        name_tag = card.select_one("h4")
        name = name_tag.get_text(strip=True).replace("Featured", "") if name_tag else ""

        # Stand
        stand_tag = card.select_one(".stand")
        stand = stand_tag.get_text(strip=True) if stand_tag else ""

        # Country
        country_tag = card.select_one(".country")
        country = country_tag.get_text(strip=True) if country_tag else ""

        # Description
        desc_tag = card.select_one(".additional p")
        description = desc_tag.get_text(" ", strip=True) if desc_tag else ""

        # Profile link
        link_tag = card.select_one(".exhibitorlist-profilelink")
        profile_link = link_tag["href"] if link_tag else ""

        data.append({
            "Company Name": name,
            "Stand": stand,
            "Country": country,
            "Description": description,
            "Profile Link": profile_link
        })

    driver.quit()

    # -------- SAVE TO EXCEL --------
    df = pd.DataFrame(data)
    df.to_excel("vitafoods_exhibitors.xlsx", index=False)

    print("Scraping complete. File saved as vitafoods_exhibitors.xlsx")

if __name__ == "__main__":
    main()
