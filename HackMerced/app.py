from hmac import trans_36
from pprint import pp
from pydoc import classname
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from pdfminer.high_level import extract_text
import database
import re
import time

def get_tr(soup):
    trs = soup.find_all('tr', class_='datarow')
    return trs

def get_commodity(trs):
    commodities = []
    for tr in trs:
        td_commodity = tr.find('td', class_='commodity')  # Use class_ instead of classname
        if td_commodity:
            commodities.append(td_commodity.text.strip())
    return commodities

def get_planted_acres(trs):
    planted_acres = []
    for tr in trs:
        tds = tr.find_all('td', class_ = 'dataitem')
        if tds[0].text.strip() == '':
            planted_acres.append('None')
        else:
            planted_acres.append(tds[0].text.strip())
    return planted_acres

def get_harvested_acres(trs):
    harvested_acres = []
    for tr in trs:
        tds = tr.find_all('td', class_ = 'dataitem')
        if tds[1].text.strip() == '':
            harvested_acres.append('None')
        else:
            harvested_acres.append(tds[1].text.strip())
    return harvested_acres

def get_yield(trs):
    yields = []
    for tr in trs:
        tds = tr.find_all('td', class_ = 'dataitem')
        if tds[2].text.strip() == '':
            yields.append('None')
        else:
            yields.append(tds[2].text.strip())
    return yields

def get_production(trs):
    production = []
    for tr in trs:
        tds = tr.find_all('td', class_ = 'dataitem')
        if tds[3].text.strip() == '':
            production.append('None')
        else:
            production.append(tds[3].text.strip())
    return production

def get_ppu(trs):
    ppu = []
    for tr in trs:
        tds = tr.find_all('td', class_ = 'dataitem')
        if tds[4].text.strip() == '':
            ppu.append('None')
        else:
            ppu.append(tds[4].text.strip())
    return ppu

def get_value_production(trs):
    value = []
    for tr in trs:
        tds = tr.find_all('td', class_ = 'dataitem')
        if tds[5].string is None:
            value.append('None')
        else:
            value.append(tds[5].text.strip())
    return value

def scrapeANDinsert(url, state):
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    commodity = get_commodity(get_tr(soup))
    # print(commodityCA)
    planted_acres = get_planted_acres(get_tr(soup))
    # print(planted_acresCA)
    harvested_acres = get_harvested_acres(get_tr(soup))
    # print(harvested_acresCA)
    yields = get_yield(get_tr(soup))
    # print(yieldCA)
    production = get_production(get_tr(soup))
    # print(productionCA)
    ppu = get_ppu(get_tr(soup))
    # print(ppuCA)
    value = get_value_production(get_tr(soup))
    # print(valueCA)

    database.insert_data(state, commodity, planted_acres, harvested_acres, yields, production, ppu, value)

overviewCA = 'https://www.nass.usda.gov/Quick_Stats/Ag_Overview/stateOverview.php?state=CALIFORNIA'
# scrapeANDinsert(overviewCA, 'CA')
overviewALB = 'https://www.nass.usda.gov/Quick_Stats/Ag_Overview/stateOverview.php?state=ALABAMA'
# scrapeANDinsert(overviewALB, 'ALB')
overviewAL = 'https://www.nass.usda.gov/Quick_Stats/Ag_Overview/stateOverview.php?state=ALASKA'
# scrapeANDinsert(overviewAL, 'AL')
overviewCO = 'https://www.nass.usda.gov/Quick_Stats/Ag_Overview/stateOverview.php?state=COLORADO'
# scrapeANDinsert(overviewCO, 'CO')
overviewCN = 'https://www.nass.usda.gov/Quick_Stats/Ag_Overview/stateOverview.php?state=CONNECTICUT'
# scrapeANDinsert(overviewCN, 'CN')

# profitableCommodityCA, highestValueCA = database.findMostProfitable('CA')
# print(profitableCommodityCA)
# print(highestValueCA)

# test1, test2 = database.findProfitPerAcre('CA', 'TOMATOES')
# print(test1)
# print(test2)



