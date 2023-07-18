from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
import time
import os

url = "https://epgp.inflibnet.ac.in/Home/ViewSubject?catid=0d/1X9CWmyPf9Hgtlh1uyw=="
driver = webdriver.Chrome()
driver.get(url)

select = Select(driver.find_element(by=By.ID, value="Paper"))

not_downloaded = []

for i, j in zip(range(0,len(select.options)), select.options):
    if i == 0:
        continue
    
    select.select_by_index(i)
    time.sleep(5)
    select2 = Select(driver.find_element(by=By.ID, value="Module"))
    print("Created Folder: ", select.options[i].text)

    if not os.path.exists(select.options[i].text):
        os.mkdir(select.options[i].text)

    for k, l in zip(range(0,len(select2.options)), select2.options):
        if k == 0:
            continue

        select2.select_by_index(k)
        time.sleep(5)
        try:
            src = driver.find_element(by=By.ID, value="ifrmet")\
                .find_element(by=By.TAG_NAME, value="iframe")\
                .get_attribute("src")
        except:
            print("Reattempting 1...")
            time.sleep(5)

            try:
                src = driver.find_element(by=By.ID, value="ifrmet")\
                    .find_element(by=By.TAG_NAME, value="iframe")\
                    .get_attribute("src")
            except:
                print("Reattempting 2...")
                time.sleep(5)
                try:
                    src = driver.find_element(by=By.ID, value="ifrmet")\
                        .find_element(by=By.TAG_NAME, value="iframe")\
                        .get_attribute("src")
                except:
                    print("Reattempting 3...")
                    time.sleep(10)
                    try:
                        src = driver.find_element(by=By.ID, value="ifrmet")\
                            .find_element(by=By.TAG_NAME, value="iframe")\
                            .get_attribute("src")
                    except:
                        print("Reattempting 4...")
                        time.sleep(10)
                        try:
                            src = driver.find_element(by=By.ID, value="ifrmet")\
                                .find_element(by=By.TAG_NAME, value="iframe")\
                                .get_attribute("src")
                        except:
                            print(f"Could not Download: \t{select2.options[k].text}\n\t\t{src}\n")
                            not_downloaded.append((select.options[i].text, select2.options[k].text))
                            continue
                    
        print(f"Downloading:\t{select2.options[k].text}\n\t\t{src}\n")

        file = requests.get(src)
        name = select2.options[k].text
        
        with open(f"./{select.options[i].text}/{name}.pdf", "wb") as f:
            f.write(file.content)

driver.quit()

with open("not_downloaded.txt", "w") as f:
    for i in not_downloaded:
        f.write(f"{i[0]}\t{i[1]}\n")