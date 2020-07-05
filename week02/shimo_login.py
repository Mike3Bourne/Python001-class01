from selenium import webdriver
import time
try:
    browser = webdriver.Chrome()
    browser.get('https://shimo.im/welcome')
    time.sleep(4)
    login_btn = browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
    # btn_login = browser.find_element_by_class_name("login-button btn_hover_style_8")
    login_btn.click()
    time.sleep(2)

    browser.find_element_by_name('mobileOrEmail').send_keys('mobile') # 可输入正确的账号
    time.sleep(1)
    browser.find_element_by_name('password').send_keys('password')  # 输入正确的密码
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button').click()

    cookie = browser.get_cookies()
    print(cookie)
    time.sleep(5)

except Exception as e:
    print(e)
finally:
    browser.close()

