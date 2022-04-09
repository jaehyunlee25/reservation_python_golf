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
import re

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

print('step 3 - flask')
app = Flask(__name__)
CORS(app)

@app.route('/hello')
def hello():
    return 'hello, world!!'

@app.route('/island_reserve')
def island_reserve():
    # 파라미터
    dict_param = {
        'year': request.args.get('year'),
        'month': request.args.get('month'),
        'date': request.args.get('date'),
        'course': request.args.get('course'),
        'time': request.args.get('time'),
    }

    # 크롬 탭 열기
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # 로그인 하기
    jsLogin = jsRead('island/island_login.js')
    driver.get('https://www.islandresort.co.kr/html/member/Login.asp')
    driver.implicitly_wait(3)
    driver.execute_script(jsLogin)
    driver.implicitly_wait(3)

    # 예약절차 링크로 이동
    print('2.0. reservation javascript call')
    driver.get('https://www.islandresort.co.kr/html/reserve/reserve01.asp')
    driver.implicitly_wait(3)

    # 참고자료
    dict_course = {'EAST': 1, 'SOUTH': 2, 'WEST':3}
    
    # 예약 날짜선택
    driver.execute_script("Date_Click('%s','%s','%s');" % (dict_param['year'], dict_param['month'], dict_param['date']))
    # 파라미터 세팅 및 시간선택
    jscon = jsRead('island/island_reserve.js')
    jscon = setParam(dict_param, jscon)
    driver.execute_script(jscon)

    REPORT = 'true'
    try:
        REPORT = driver.execute_script('return REPORT.value')
    except:
        print('normal')

    # 리턴 객체
    obj = {
        'process': 'okay',
    }

    if REPORT == 'false':
        obj['process'] = 'error'
        obj['message'] = 'no such Tee'
        obj['isReserved'] = False
        return json.dumps(obj)

    # 예약인원 선택
    driver.execute_script("document.getElementsByClassName('res_select_typeA')[0].value=3")
    # 위임여부 선택
    driver.execute_script("document.getElementsByClassName('res_select_typeA')[1].value=1")
    # 예약실행
    driver.execute_script("document.getElementsByClassName('type1')[0].click()")

    # alert 처리
    alert = WebDriverWait(driver, 10).until(expected_conditions.alert_is_present())
    # 예약을 하겠습니까?
    alert.accept()   
    # 예약 성공 혹은 예약 오류 메시지
    result = alert.text    
    alert.accept()
    driver.close()    

    if result.index('예약이 정상적으로 처리되었습니다.') == -1:
        obj['isReserved'] = False
    else:
        obj['isReserved'] = True

    obj['message'] = result

    return json.dumps(obj)

@app.route('/island_search')
def island_search():
    print('1.0. login javascript call')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    lcon = jsRead('island/island_login.js')

    driver.get('https://www.islandresort.co.kr/html/member/Login.asp')
    driver.implicitly_wait(3)
    driver.execute_script(lcon)
    driver.implicitly_wait(3)

    print('2.0. reservation javascript call')
    driver.get('https://www.islandresort.co.kr/html/reserve/reserve02.asp')
    
    con = jsRead('island/island_search.js')
    driver.execute_script(con)
    
    val = driver.execute_script('return elResult.innerHTML')
    driver.implicitly_wait(3)

    driver.close()

    return val

@app.route('/island_cancel')
def island_cancel():
    print('1.0. login javascript call')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    lcon = jsRead('island/island_login.js')
    
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

def setParam(dict, jsStr):
    for key, value in dict.items():
        jsStr = re.sub('\$\{' + key + '\}', value, jsStr)
    return jsStr
def jsRead(file):
    l = open(file, 'r')
    lcon = l.read()
    l.close()
    return lcon

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)