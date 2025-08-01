# فرق بین selenium.webdriver باwebdriver_manager
# selenium.webdriver = خودِ ابزار کنترل مرورگر (بدون مدیریت درایور)
# webdriver_manager = ابزار مدیریت و دانلود خودکار درایور برای راحتی و سرعت توسعه

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from make_datafram import category_data
from analyze import export_data
from first_last import find_last_page


# ------------------------
number_page = int(find_last_page())
# number_page = 7
Dataframe_skill = pd.DataFrame(columns=["job_offer"])

options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
#اگر شرط قبل از ۳۰ ثانیه برآورده بشه، بلافاصله ادامه می‌ده (یعنی زودتر از ۳۰ ثانیه هم ممکنه کار تموم بشه).
# اگر بعد از ۳۰ ثانیه شرط برقرار نشه، خطا (TimeoutException) می‌ده و کد متوقف می‌شه
wait = WebDriverWait(driver, 30)
url = "https://jobvision.ir/jobs/keyword/برنامه%20نویس%20python/category/developer"
driver.get(url)
counter = 2
try:
    while counter <= number_page:
        print(counter)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.desktop-job-card")))
        initial_links = driver.find_elements(By.CSS_SELECTOR, "a.desktop-job-card")
        page_links = driver.find_elements(By.CSS_SELECTOR, "a.page-link")
        print("تعداد آگهی‌ها:", len(initial_links))
        for i in range(len(initial_links)):
            try:
                # بعد از back باید لیست رو دوباره بگیریم
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.desktop-job-card")))
                job_links = driver.find_elements(By.CSS_SELECTOR, "a.desktop-job-card")
                # نیاز به استفاده نیست فقط می خوام بدونی
                # for job in job_links:
                #     اینجا متن ها را نشان می دهد
                #     title = job.text
                #     اینجا لینک را نشان می دهد
                #     url = job.get_attribute("href")
                job = job_links[i]
                # execute_scriptکد جاوا اسکریپ رو مستقیما اجرا می کنه
                # کد جاوا اسکریپ ";()arguments[0].scrollIntoView"
                # کدهای جاوا اسکریپ را باید تو "" نوشت
                driver.execute_script("arguments[0].scrollIntoView();", job)
                job.click()
                time.sleep(10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.job-title")))
                title = driver.find_element(By.CSS_SELECTOR, "h1.job-title").text
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, "span.d-flex.bg-white.text-black.border.border-secondary.col.rounded-sm.text-white")
                    list_skill = []
                    parts = ""
                    for ce in range(len(elements)):
                        # جدا کردن بر اساس خط تیره
                        parts = elements[ce].text.split("-")
                        # # حذف فاصله‌های اضافی اطراف هر بخش
                        parts = [part.strip() for part in parts]
                        list_skill.append(parts)
                    Dataframe_skill = category_data(title, list_skill,Dataframe_skill)
                except:
                    text = "(توضیحات یافت نشد)"
            except Exception as e:
                print("خطا در خواندن آگهی")
        for link in page_links:
            if link.text.strip() == str(counter):
                driver.execute_script("arguments[0].scrollIntoView(true);", link)
                time.sleep(5)
                driver.execute_script("arguments[0].click();", link)
                counter = counter + 1
                break
finally:
    # بستن مرورگر
    driver.quit()
export_data(Dataframe_skill)



