from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

from flask import Flask, render_template, send_file
from flask import request
from flask_cors import CORS, cross_origin
import json

print('step 1')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument('disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--disable-dev-shm-usage")

print('step 2')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

print('step 3 - flask')
app = Flask(__name__)
CORS(app)

@app.route('/hello')
def hello():
    return 'hello, world!!'

@app.route('/island')
def island():
    print('1.0. login javascript call')
    l = open('island/island_login.js', 'r')
    lcon = l.read()
    l.close()
    driver.get('https://www.islandresort.co.kr/html/member/Login.asp')
    driver.implicitly_wait(3)
    driver.execute_script(lcon)
    driver.implicitly_wait(3)

    print('2.0. reservation javascript call')
    driver.get('https://www.islandresort.co.kr/html/reserve/reserve01.asp')
    driver.implicitly_wait(3)
    # 날짜선택
    driver.execute_script("Date_Click('2022','04','26');")
    # 코스와 시간선택
    driver.execute_script("Book_time('20220426','3', 'WEST','0600','150000');")
    # 예약인원 선택
    driver.execute_script("document.getElementsByClassName('res_select_typeA')[0].value=3")
    # 위임여부 선택
    driver.execute_script("document.getElementsByClassName('res_select_typeA')[1].value=1")
    # 예약실행
    driver.execute_script("document.getElementsByClassName('type1')[0].click()")
    alert = WebDriverWait(driver, 10).until(expected_conditions.alert_is_present())
    alert.accept()

    return alert.text

@app.route('/island_search')
def island_search():
    print('1.0. login javascript call')
    l = open('island/island_login.js', 'r')
    lcon = l.read()
    l.close()
    driver.get('https://www.islandresort.co.kr/html/member/Login.asp')
    driver.implicitly_wait(3)
    driver.execute_script(lcon)
    driver.implicitly_wait(3)

    print('2.0. reservation javascript call')
    driver.get('https://www.islandresort.co.kr/html/reserve/reserve02.asp')
    
    l = open('island/island.js', 'r')
    con = l.read()
    l.close()
    driver.execute_script(con)
    
    val = driver.execute_script('return elResult.innerHTML')
    driver.implicitly_wait(3)

    return val

@app.route('/island_cancel')
def island_cancel():
    print('1.0. login javascript call')
    l = open('island/island_login.js', 'r')
    lcon = l.read()
    l.close()
    driver.get('https://www.islandresort.co.kr/html/member/Login.asp')
    driver.implicitly_wait(3)
    driver.execute_script(lcon)
    driver.implicitly_wait(3)

    print('2.0. reservation javascript call')
    driver.get('https://www.islandresort.co.kr/html/reserve/reserve02.asp')
    driver.implicitly_wait(3)

    """ result = driver.find_element(By.TAG_NAME, 'body')
    f = open('result.html', 'w')
    f.write(result.get_attribute('innerHTML'))
    f.close() """

    return 'cancelled'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)