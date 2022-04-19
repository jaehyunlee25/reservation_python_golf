@app.route('/reserve/island')
def island_reserve():
    # 파라미터
    dict_param = {
        'login_id': request.args.get('login_id'),
        'login_password': request.args.get('login_password'),
        'year': request.args.get('year'),
        'month': request.args.get('month'),
        'date': request.args.get('date'),
        'course': request.args.get('course'),
        'time': request.args.get('time'),
    }

    # 크롬 탭 열기
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # 로그인 하기
    jsLogin = jsRead('island/login.js')
    jsLogin = setParam(dict_param, jsLogin)

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
    jscon = jsRead('island/reserve.js')
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

@app.route('/search/island')
def island_search():
    # 파라미터
    dict_param = {
        'login_id': request.args.get('login_id'),
        'login_password': request.args.get('login_password'),
    }
    print('1.0. login javascript call')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    jsLogin = jsRead('island/login.js')
    jsLogin = setParam(dict_param, jsLogin)

    driver.get('https://www.islandresort.co.kr/html/member/Login.asp')
    driver.implicitly_wait(3)
    driver.execute_script(jsLogin)
    driver.implicitly_wait(3)

    print('2.0. reservation javascript call')
    driver.get('https://www.islandresort.co.kr/html/reserve/reserve02.asp')
    
    con = jsRead('island/search.js')
    driver.execute_script(con)
    
    val = driver.execute_script('return elResult.innerHTML')
    driver.implicitly_wait(3)

    driver.close()

    return val

@app.route('/cancel/island')
def island_cancel():
    # 파라미터
    dict_param = {
        'login_id': request.args.get('login_id'),
        'login_password': request.args.get('login_password'),
        'year': request.args.get('year'),
        'month': request.args.get('month'),
        'date': request.args.get('date'),
        'course': request.args.get('course'),
        'time': request.args.get('time'),
    }

    print('1.0. login javascript call')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    jsLogin = jsRead('island/login.js')
    jsLogin = setParam(dict_param, jsLogin)
    
    driver.get('https://www.islandresort.co.kr/html/member/Login.asp')
    driver.implicitly_wait(3)
    driver.execute_script(jsLogin)
    driver.implicitly_wait(3)

    print('2.0. reservation javascript call')
    driver.get('https://www.islandresort.co.kr/html/reserve/reserve02.asp')
    driver.implicitly_wait(3)

    # 참고자료
    dict_course = {'EAST': 1, 'SOUTH': 2, 'WEST':3}
    # 파라미터 세팅 및 시간선택
    jscon = jsRead('island/cancel.js')
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
        obj['message'] = 'no such Reservation'
        obj['isCancelled'] = False
        return json.dumps(obj)

    # 취소실행
    driver.execute_script("document.getElementById('SEL_BUTTON').click()")
    # alert 처리
    alert = WebDriverWait(driver, 10).until(expected_conditions.alert_is_present())
    print(alert.text)
    
    # 예약을 취소 하시겠습니까?
    alert.accept()
    # 예약이 취소되었습니다.
    alert.accept()
    driver.close()

    obj['message'] = '예약이 취소되었습니다.'

    return json.dumps(obj)
