import atexit
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, ElementClickInterceptedException
import subprocess
from datetime import datetime
import clipboard
import keyboard
from courtinfo import *
from notifypy import Notify
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

print("시작시간",datetime.now())

dayName = ['mondays','tuesdays','wednesdays','thursdays','fridays','saturdays','sundays']
thisNow = datetime.now() #지금 날짜정보
thisMonth = thisNow.month #이번달을 숫자로표현
nextMonthCalculated = thisNow + relativedelta(months=1) # 오늘 기준 1달뒤 날짜정보 
nextMonth = thisMonth +1
thisYear = thisNow.year # 현재 년정보
nextYear = thisYear +1
thisMonthLast = datetime(thisYear,thisMonth,1) + relativedelta(months=1) - timedelta(seconds=1) #이번달 마지막 날 11시 59분 59초

targetMonth = None

# 25일 이전에는 이번달만 검색
if thisNow.day < 25:
    targetMonth = thisMonth
# 25일 20시 이후 부터는 다음달 검색
elif thisNow.day == 25:
    if thisNow.hour < 20:
        targetMonth == thisMonth
    else:
        targetMonth == nextMonth    
elif thisNow.day > 25:    
    targetMonth = nextMonth

days = {1:["월",None],2:["화",None],3:["수",None],4:["목",None],5:["금",None],6:["토",None],7:["일",None]}
timeDicWeekdays = {1: ["06",None], 2: ["08",None], 3: ["10", None], 4: ["12",None], 5:["14",None], 6:["16",None],7:["18",None],8:["20",None]}
timeDicWeekend = {1: ["06",None], 2: ["08",None], 3: ["10", None], 4: ["12",None], 5:["14",None], 6:["16",None],7:["18",None],8:["20",None]}
timeDic = {1: ["06",None], 2: ["08",None], 3: ["10", None], 4: ["12",None], 5:["14",None], 6:["16",None],7:["18",None],8:["20",None]}
timeValueList = list(timeDic.values())
timeDicValue = []


for i in range(0,len(timeValueList)):
    timeDicValue.append(timeValueList[i][0])
    
# while targetTime not in timeDicValue:
#     print('')
#     targetTimeNum = int(input("몇 시를 예약하시기 원하십니까?\n 원하시는 시간을 써주세요\n 1. 6시\n 2. 8시\n 3. 10시\n 4. 12시\n 5. 14시\n 6. 16시\n 7. 18시\n 8. 20시\n"))
#     targetTime = timeDic[targetTimeNum]
# print(targetTime,"시를 예약합니다.")

# Checker = False
# userCheck = None
# address = input("어느시, 어느구, 어떤 동에 거주하시나요? ex 고양시, 일산서구, 주엽동\n")
# while Checker == False:
#     print(address,"으로 입력합니다. 이대로 진행할까요?")
    
#     while userCheck not in [1,2]:
#         userCheck = int(input("1. 예, 2: 아니요\n 숫자 1 또는 2를 입력하세요.\n"))
#         if userCheck == 1:
#             Checker = True
#         elif userCheck == 2:
#             address = input("어느시, 어느구, 어떤 동에 거주하시나요? ex 고양시, 일산서구, 주엽동\n")
#             userCheck = None
notification = Notify()
notification.title = "고양시 테니스 코트 검색"


def seleniumChrome():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"]) #usb 에러 메세지 해결
    # options.add_argument('headless') # 창 실행하지 않고 프로그램 진행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def executeChrome():
    # 크롬실행
    try:
        subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome_debug_temp"') # 디버거 크롬 구동 
    except:
        subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome_debug_temp"') # 디버거 크롬 구동

def debuggerChrome():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") #디버거모드
    options.add_argument('window-size=1024,860') #윈도우 사이즈
    options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) #크롬버전에 따라 driver 설치
    wait = WebDriverWait(driver, 600) #최대10분 대기
    return driver, wait

def courtSearching():
    driver, wait = seleniumChrome()
    driverCounter = 0
    if targetMonth < 10:
        searchingTargetMonth = "0" + str(targetMonth)
    for i in range(1,7):
        if court[i][1].get()==True: #코트예약 사용자가 하길 원하면
            if driverCounter > 1:
                driver.close()
            driver.get(court[i][2]) #코트예약 url 호출
            driverCounter =+ 1
            for courtNum in range(1,court[i][3]+1): # 코트 갯수만큼 반복
                try:
                    try:
                        courtSelection = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'{0}번 {1}월')]".format(courtNum,targetMonth))))
                        print(courtSelection.text)
                        courtSelection.click()
                    except:
                        courtSelection = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'{0}번 {1}월')]".format(courtNum,searchingTargetMonth))))
                        print(courtSelection.text)
                        courtSelection.click()
                except:
                    try:
                        # 다음페이지에 있는 경우 > 버튼 누르기
                        nextPage = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'/html/body/app/div[2]/div[2]/div/div/div[2]/div[2]/a[2]/i')))
                        nextPage.click()
                        try:
                            courtSelection = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'{0}번 {1}월')]".format(courtNum,targetMonth))))
                            print(courtSelection.text)
                            courtSelection.click()
                        except:
                            courtSelection = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'{0}번 {1}월')]".format(courtNum,searchingTargetMonth))))
                            print(courtSelection.text)
                            courtSelection.click()
                    except:
                        print(searchingTargetMonth)         
                # 달력에 있는 날짜들 가져오기
                day_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"calendar-date")))
                # 일자 별 로직 시행
                for day in day_elements:
                    day_num_element = day.find_element(By.CLASS_NAME,"num")
                    day_num_text = day_num_element.text # 1~31까지 숫자 가져오기
                    sevenDaysNum = date(thisYear,targetMonth,int(day_num_text)).weekday()
                    if days[sevenDaysNum+1][1].get() == False:
                        continue
                    # day 색이 회색 (hex = e4e4e4 / rgba = (228, 228, 228, 1))이 아닐때 로직 시행
                    if day_num_element.value_of_css_property('color') != "rgba(228, 228, 228, 1)":
                        print(day_num_text, "일 확인 중..")
                        # 일자 클릭
                        day.click()
                        # 일자 클릭 후 time list 를 찾는데 시간이 걸리기 때문에 sleep
                        time.sleep(0.5)
                        # 시간 list 추출
                        timesCandicate = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//span[@class="box_info"]')))
                        # 매진정보 list 추출
                        timesAvailable = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//span[@class="box_info"]/following-sibling::span')))
                        # 코트명 + " " + 연도 + "/" + "월" + " 0번 코트" 필요
                        targetName = court[i][0] + "_" + str(thisYear) + "/" + str(targetMonth) + "_{0}번_코트".format(courtNum)
                        for timeCandidate, timeAvailable in zip(timesCandicate,timesAvailable):
                            if days[sevenDaysNum+1][1].get() == True and timeAvailable.text != "매진":
                                # 주말
                                if date(thisYear,targetMonth,int(day_num_text)).weekday() >= 5:
                                    for j in range(1,9):
                                        targetTime = timeDicWeekend[j][0]+":00"
                                        if  targetTime == timeCandidate.text and timeDicWeekend[j][1].get() == True:
                                            messageBody = targetName + day_num_text + "일 " + timeCandidate.text + " 예약가능"
                                            notification.message = messageBody
                                            notification.send()                                  
                                # 주중
                                elif date(thisYear,targetMonth,int(day_num_text)).weekday() < 5:
                                    for k in range(1,9):
                                        targetTime = timeDicWeekdays[k][0]+":00"
                                        if timeDicWeekdays[k][0]+":00" == timeCandidate.text and timeDicWeekdays[k][1].get() == True:
                                            messageBody = targetName + day_num_text + "일 " + timeCandidate.text + " 예약가능"
                                            notification.message = messageBody
                                            notification.send()
                    else:
                        pass
                # 1일부터 말일까지 검색 하면 뒤로 가기 누르기
                driver.back()
    driver.quit()
    notification.message = "코트 검색이 끝났습니다."
    notification.send()

def reservHelper(courtValue,timeValue,address):
    executeChrome()
    driver, wait = debuggerChrome()
    targetCourt = eval("targetCourt"+str(courtValue))
    driver.get(targetCourt)    
    while True:    
        try: 
            len(driver.current_url) > 0
            pressedKey = keyboard.read_key()
            match pressedKey:
                case "f8":
                    print("{0}시 선택시도".format(timeDic[timeValue][0]))
                    try: 
                        timeSelection = driver.find_element(By.XPATH,"//span[contains(text(),'{0}:00')]".format(timeDic[timeValue][0]))
                        if timeSelection.value_of_css_property('color') != "rgba(187, 187, 187, 1)":
                            timeSelection.click()
                            nextSelection =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'다음단계')]")))
                            nextSelection.click()
                    except:
                        print("{0}시 선택불가".format(timeDic[timeValue][0]))
                case "f9":
                    print("정보입력")
                    try:
                        # 가격 고르기
                        priceSelection =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/bk-slot-ticket/bk-slot-final/div/div[1]/bk-qty-slot/div/div/div[2]/div/div/a[2]')))
                        priceSelection.click()
                        # 지역주소 넣기
                        addressSelection =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="extra0"]')))
                        addressSelection.click()
                        clipboard.copy(address)
                        # Ctrl + V 하기
                        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                        # 선택해주세요 누르기
                        aggrementSelection1 =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'선택해주세요')]")))
                        aggrementSelection1.click()
                        # time.sleep(1)
                        # 동의합니다. 누르기
                        aggrementSelection2 =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/bk-slot-ticket/bk-slot-final/div/div[2]/div[1]/bk-extra-input/div/div/form/div[2]/div/div/div/div/div[2]/div/ul/li[2]')))
                        aggrementSelection2.click()
                        # 결제화면 넘어가기
                        nextSelection2 =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/bk-slot-ticket/bk-slot-final/div/div[2]/bk-submit/div/button')))
                        nextSelection2.click()
                    except:
                        print("f9 실패")
                case "f10":
                    print("결재하기")
                    try:

                        # 항상 전액사용 체크해제
                        NpayMoney = driver.find_element(By.CLASS_NAME,'Checkout_checkbox-mark__3i-t1')
                        try: 
                            NpayMoney.click()
                        except NoSuchElementException:
                            pass
                        # 일반 결제 누르기
                        generalPayment =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="PAYMENT_WRAP"]/div[1]/div[1]/ul/li[4]/div/span/span')))
                        generalPayment.click()
                        # 나중에 결제하기 누르기
                        payLater =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="PAYMENT_WRAP"]/div[1]/div[1]/ul/li[4]/ul/li[2]/span[1]/span')))
                        payLater.click()
                        # 은행 종류 고르기
                        bankSelectMenu =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="bankCodeList"]/div/div')))
                        bankSelectMenu.click()
                        # 하나은행
                        bankSelect =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="bankCodeList"]/div/div[2]/div/ul/li[6]')))
                        bankSelect.click()
                        
                        # 본인계좌로 환불
                        # accountSelect = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="PAYMENT_WRAP"]/div[1]/div[1]/div[1]/div[2]/div[2]/div/ul/li[1]/span/span')))
                        # accountSelect.click()
                        
                        # 환불정산액 적립
                        refundSelect =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="PAYMENT_WRAP"]/div[1]/div[1]/div[1]/div[2]/div[2]/div/ul/li[2]/span/span')))
                        refundSelect.click()

                        # 현금영수증
                        CashReceipt =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="PAYMENT_WRAP"]/div[1]/div[1]/div[2]/div/ul/li[1]/span/span')))
                        CashReceipt.click()
                        #최종 결제 선택하기
                        finalclick =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,"//button[contains(text(),'주문하기')]")))
                        finalclick.click()
                        reservationVerification =  WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'입금 대기')]")))
                        print("결제완료")
                        driver.get(targetCourt)
                    except:
                        print("f10 실패")
                case "f4":
                    driver.get(targetCourt)
        except NoSuchWindowException:
            break