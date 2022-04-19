# 주의점: 진양밸리는 로딩시간이 좀 늦으므로 time.sleep을 잘 살펴야 한다.

@app.route('/reserve/jinyang')
def jinyang_reserve():
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
    jsLogin = jsRead('jinyang/login.js')
    jsLogin = setParam(dict_param, jsLogin)

    driver.get('https://www.chinyangvalley.co.kr/member/login.asp')
    driver.execute_script(jsLogin)
    time.sleep(0.5)

    # 예약절차 링크로 이동
    print('2.0. reservation javascript call')
    driver.get('https://www.chinyangvalley.co.kr/reservation/reservation2.asp')
    time.sleep(1)

    # 예약 날짜선택
    fulldate = "document.getElementById('%s').click();" % (dict_param['year'] + dict_param['month'] + dict_param['date'])
    driver.execute_script(fulldate)
    time.sleep(1)
    # 파라미터 세팅 및 시간선택
    jscon = jsRead('jinyang/reserve.js')
    jscon = setParam(dict_param, jscon)
    driver.execute_script(jscon)

    '''
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
    '''
    return 'json.dumps(obj)'

@app.route('/search/jinyang')
def jinyang_search():
    # 파라미터
    dict_param = {
        'login_id': request.args.get('login_id'),
        'login_password': request.args.get('login_password'),
    }
    print('1.0. login javascript call')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    jsLogin = jsRead('jinyang/login.js')
    jsLogin = setParam(dict_param, jsLogin)
    
    driver.get('https://www.chinyangvalley.co.kr/member/login.asp')
    driver.execute_script(jsLogin)
    time.sleep(0.5)

    print('2.0. reservation javascript call')
    driver.get('https://www.chinyangvalley.co.kr/reservation/reserCheck.asp')
    time.sleep(0.5)
    
    con = jsRead('jinyang/search.js')
    driver.execute_script(con)
    
    val = driver.execute_script('return elResult.innerHTML')
   
    driver.close()

    return val

@app.route('/cancel/jinyang')
def jinyang_cancel():
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
    
    jsLogin = jsRead('jinyang/login.js')
    jsLogin = setParam(dict_param, jsLogin)
    
    driver.get('https://www.chinyangvalley.co.kr/member/login.asp')
    driver.execute_script(jsLogin)
    time.sleep(0.5)

    print('2.0. reservation javascript call')
    driver.get('https://www.chinyangvalley.co.kr/reservation/reserCheck.asp')
    time.sleep(0.5)
    
    
    # 파라미터 세팅 및 시간선택
    jscon = jsRead('jinyang/cancel.js')
    jscon = setParam(dict_param, jscon)
    print(jscon)
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
        print('false')
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
    time.sleep(0.5)
    # 예약이 취소되었습니다.
    result = alert.text
    alert.accept()
    driver.close()

    if result.index('취소 되었습니다.') == -1:
        obj['isCancelled'] = False
    else:
        obj['isCancelled'] = True

    obj['message'] = result
    
    return json.dumps(obj)
