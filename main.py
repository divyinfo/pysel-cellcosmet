import re
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def download_image(url, dirname, filename):
    response = requests.get(url, stream=True)
    save_image_to_file(response, dirname, filename)
    del response

def save_image_to_file(image, dirname, filename):
    with open('{dirname}/{filename}'.format(dirname=dirname, filename=filename), 'wb') as f:
        shutil.copyfileobj(image.raw, f)

def main():

    driver = webdriver.Chrome()
    driver.maximize_window()

    for page in range(20):
        page += 1
        driver.get("https://www.cellcosmet-cellmen.com/qsPortal/Ajax/get.asp?Ajax=getnode&NoLimitPage=1&N=282&tag=16&tag=33&page=" + str(page))

        # elem = driver.find_elements(By.CSS_SELECTOR, '.tplEcom.tplSearchEcom')
        imgs = driver.find_elements(By.CSS_SELECTOR, '.tplEcom.tplSearchEcom .list-item.ECArt.grid-item .list-item-image')
        for img in imgs:
            style = img.get_attribute('style')
            r = re.search(r'url\([\'\"](.*\/(.*\.(?:jpg|jpeg|png)))[\'\"]\)', style)
            if r and r.groups():
                url = r.groups()[0]
                filename = r.groups()[1]
                
                url = 'https://www.cellcosmet-cellmen.com' + url
                with open('results.txt', 'a+') as f:
                    f.write(url + '\n')

                download_image(url, 'detail', filename)

                filename = 'zoom' + filename.strip('detail')
                url = 'https://www.cellcosmet-cellmen.com/data/dataimages/upload/thumbnails/' + filename
                with open('zooms.txt', 'a+') as f:
                    f.write(url + '\n')
                download_image(url, 'zoom', filename)

    driver.close()

if __name__ == "__main__":
    main()