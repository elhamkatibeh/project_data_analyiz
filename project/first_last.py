
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
def find_last_page():
    options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    #اگر شرط قبل از ۳۰ ثانیه برآورده بشه، بلافاصله ادامه می‌ده (یعنی زودتر از ۳۰ ثانیه هم ممکنه کار تموم بشه).
    # اگر بعد از ۳۰ ثانیه شرط برقرار نشه، خطا (TimeoutException) می‌ده و کد متوقف می‌شه
    wait = WebDriverWait(driver, 30)

    url = "https://jobvision.ir/jobs/keyword/برنامه%20نویس%20python/category/developer"
    driver.get(url)

    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.desktop-job-card")))
        initial_links = driver.find_elements(By.CSS_SELECTOR, "a.desktop-job-card")
        page_link = driver.find_elements(By.CSS_SELECTOR, ".page-link")
        # for i in range(len(page_link)):
        #     text = page_link[i].text
        driver.execute_script("arguments[0].scrollIntoView();",page_link[-1])
        page_link[-1].click()
        page_link_end = driver.find_elements(By.CSS_SELECTOR, ".page-link")
        for j in range(len(page_link_end)):
            if page_link_end[j].text != "":
                last_number_page = page_link_end[j].text
    except:
        text = "(توضیحات یافت نشد)"
    driver.quit()
    return last_number_page