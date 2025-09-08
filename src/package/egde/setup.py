from selenium import webdriver
from selenium.webdriver.common.by import By

# 将驱动程序和当前脚本放在同一个文件夹也可以
# driver = webdriver.Chrome(r'D:/uusama/tools/chromedriver.exe')
driver = webdriver.Edge()      # Edge浏览器
driver.implicitly_wait(30)
driver.get('https://lbs.amap.com/api/webservice/guide/api-advanced/search')  # 打开指定路径的页面

def querySelector(selectors):
    return driver.find_element(By.CSS_SELECTOR,selectors)
def querySelectors(selectors):
    return driver.find_elements(By.CSS_SELECTOR,selectors)
    
def input_item():
    atomic = querySelectors('.table-container')
    input_item = atomic[2].find_elements(By.CSS_SELECTOR,'input')
    run_button = atomic[2].find_element(By.CSS_SELECTOR,'.run')
    input0 = input_item[0]
    input1 = input_item[1]
    input2 = input_item[2]
    input3 = input_item[3]
    input1.clear()
    # input1.send_keys('')
    input2.clear()
    input2.send_keys('200000')
    run_button.click()

    pass
    
# input_item()
if input('1'):
    driver.quit()