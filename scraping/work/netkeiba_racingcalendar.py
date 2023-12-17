# netkeiba(https://www.netkeiba.com/?rf=logo)の開催日程からレース日程を取得する。
# 

import bs4
import traceback
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

### ドライバー準備
def get_driver():
    print("set up driver")
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
                command_executor = 'http://selenium:4444/wd/hub',
                options = options
                )
    print("done set up driver")
    driver.implicitly_wait(3)
    return driver

### 対象ページのソースを取得する
def get_source_from_page(driver, page):
    try:
        # ターゲット
        driver.get(page)
        driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
        page_source = driver.page_source
 
        return page_source
 
    except Exception as e:
 
        print("Exception\n" + traceback.format_exc())
 
        return None

### ソースから必要情報を取得する。
def get_data_from_source(src):
    # スクレイピング。対象URLのソースを取得する。
    print("start get_data_from_source")
    soup = bs4.BeautifulSoup(src, features='html.parser')
 
    try:
        info = []
        table = soup.find(class_="Calendar_Table")
        if table:
            elems = table.find_all("td", class_="RaceCellBox")
            for elem in elems:
                a_tag = elem.find("a")
                if a_tag:
                    href = a_tag.attrs['href']
                    match = re.findall("\/top\/race_list.html\?kaisai_date=(.*)$", href)
                    if len(match) > 0:
                        item_id = match[0]
                        info.append(item_id)
        print("match:{}".format(info))
        return info
 
    except Exception as e:
        print("Exception\n" + traceback.format_exc())
        return None

### main
if __name__ == "__main__":
    ### ブラウザのdriver取得
    driver = get_driver()

    ### 年月list
    list_year_month = []

    ### 年月ごとに取得
    print("start scraping")
    try:
        for year in [2022,2023]:
            for month in range(1, 13):
                print(year, month)

                # 対象ページURL
                page = "https://race.netkeiba.com/top/calendar.html?year=" + str(year) + "&amp;month=" + str(month)
    
                # ページのソース取得
                source = get_source_from_page(driver, page)
                # ソースからデータ抽出
                data = get_data_from_source(source)
                # list 保存
                list_year_month.extend(data)
                break
    except:
        print("ERROR!! driver.quit()")
        driver.quit()    

    ### driver
    driver.quit()

    print(list_year_month)