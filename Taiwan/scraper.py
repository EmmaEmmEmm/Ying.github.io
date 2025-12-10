# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_latest_power_lottery():
    try:
        # Selenium 設定
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 台灣彩券官網
        driver.get("https://www.taiwanlottery.com/")
        time.sleep(1)   # 讓 JavaScript 載入

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        # 找到威力彩開獎區
        result_blocks = soup.find_all("div", class_="result-balls")
        if not result_blocks:
            return {"error": "找不到開獎資訊"}

        # 威力彩通常在第一個區塊
        power_lottery_block = result_blocks[1]

        balls = power_lottery_block.find_all("div", class_="ball")

        if len(balls) < 7:
            return {"error": "威力彩球數異常"}

        # 前 6 顆區域 (大小順序)
        main_numbers = [b.text for b in balls[:6]]

        # 第二區 (特別號)
        special_number = balls[6].text

        return {
            "main": main_numbers,
            "special": special_number
        }

    except Exception as e:
        return {"error": str(e)}
