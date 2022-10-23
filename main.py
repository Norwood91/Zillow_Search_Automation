import time

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

ZILLOW_URL = 'https://www.zillow.com/sacramento-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Sacramento%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.04949868164063%2C%22east%22%3A-120.88220131835938%2C%22south%22%3A38.26142657634144%2C%22north%22%3A38.95466199915111%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20288%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%7D'
GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSf3KE-ELeVcoJ6O3u_tzglmLtociZNpA3pd46-YAJsgJhsc7A/viewform?usp=sf_link'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.37',
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
# ________________________________________________________ BS4 -----------------------------------------------------

res = requests.get(ZILLOW_URL, headers=headers)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
house_prices = soup.findAll(attrs={'data-test': 'property-card-price'})
house_links = soup.findAll(attrs={'data-test': 'property-card-link'})
house_addresses = soup.findAll('address')

prices = []
links = []
addresses = []

for price in house_prices:
    price_text = price.getText().split('/')[0:1]
    price = ''.join(price_text)
    prices.append(price)
prices[3] = '$1,850'

for link in house_links:
    house_link = link.get('href')
    links.append(house_link)
del links[6:8]

new_house_links = []
for house_link in links:
    if house_link not in new_house_links:
        new_house_links.append(house_link)

for address in house_addresses:
    address_text = address.getText()
    addresses.append(address_text)

# ________________________________________________________ SELENIUM ------------------------------------------------

chrome_driver_path = 'C:\Development\chromedriver.exe'
driver = webdriver.Chrome(chrome_driver_path)


for n in range(len(new_house_links)):
    driver.get(GOOGLE_FORM_URL)
    time.sleep(2)
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    url_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    address_input.send_keys(addresses[n])
    price_input.send_keys(prices[n])
    url_input.send_keys(new_house_links[n])
    submit.click()


