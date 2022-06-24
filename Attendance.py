# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


class Attendance:

    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get("https://company-name.stohrm.com/")
        self.user_id='######'
        self.password='#######'
        self.fill_last_month = True
        self.staleElement = True

    def setSleep(self,seconds=1):
        sleep(seconds)

    def login(self):
        self.driver.find_element(By.ID,"userid").send_keys(self.user_id)
        self.driver.find_element(By.NAME,"logsubmit").click()
        self.driver.find_element(By.ID,"password").send_keys(self.password)
        self.driver.find_element(By.NAME,"logsubmit").click()
        self.setSleep(2)
        """un comment this if you are redirect to already login session issue page
        """
        #self.driver.find_element(By.NAME,"submit").click()
        self.setSleep(2)

    def vaccineModal(self):
        vaccine_modal = self.driver.find_element(By.ID,"vaccine_declare")
        vaccine_modal.find_element(By.CSS_SELECTOR,"button.close").click()

    def findMainMenu(self):
        self.main_menu = self.driver.find_element(By.ID,"main-menu")
        self.setSleep(2)

    def GotoAttendance(self):
        self.findMainMenu()
        submenus = self.main_menu.find_elements_by_xpath(".//*")
        for li in submenus:
            if li.text == 'Time & attendance':
                li.click()
                break
        self.main_menu.find_element(By.CSS_SELECTOR,'li.root-level.has-sub.opened>ul>li:nth-child(2)').click()
    
    def findCal(self):
        self.findMainMenu()
        self.calendar = self.driver.find_element(By.ID, 'cal')

    def GotoPreviousMonth(self):
        self.findCal()
        prev_month = self.calendar.find_elements_by_xpath(".//a[@class='ajax_link_cal']")
        print(prev_month)
        prev_month[0].click()
        self.setSleep()

    def GotoCurrentMonth(self):
        self.findCal()
        prev_month = self.calendar.find_elements_by_xpath(".//a[@class='ajax_link_cal']")
        print(prev_month)
        prev_month[1].click()
        self.setSleep()
    
    def findAbsentCount(self):
        self.setSleep()
        self.findCal()
        totals_rows = self.calendar.find_elements_by_xpath(".//td[@class='absent_class_emp']")
        self.count = len(totals_rows)
        self.staleElement = True
        self.setSleep()
        return totals_rows

    def fillModal(self):
        self.setSleep()
        self.driver.find_element(By.ID,'form_modal_box').find_element_by_link_text('here').click()
        self.setSleep()
        self.driver.find_element(By.ID,'form_modal_box').find_element_by_id('login').click()
        self.driver.find_element(By.CSS_SELECTOR, 'div.time-picker>ul>li:nth-child(127)').click() #10.30 AM
        self.driver.find_element(By.ID,'form_modal_box').find_element_by_id('logout').click()
        self.driver.find_element(By.XPATH, ('(//div[@class="time-picker"])[2]')).find_element_by_css_selector('ul>li:nth-child(235)').click() #7.30 PM
        self.driver.find_element(By.ID,'attendance_drpdwn').click()
        self.driver.find_element(By.ID,'attendance_codeSelectBoxItOptions').find_element_by_css_selector('li:nth-child(2)').click()
        self.driver.find_element(By.ID,'remarksSelectBoxItContainer').click()
        self.driver.find_element(By.ID,'remarksSelectBoxItOptions').find_element_by_css_selector('li:nth-child(4)').click()
        self.driver.find_element(By.NAME,'other_remark').send_keys("work from home")
        self.driver.find_element(By.ID,'submit_att').click()
        self.setSleep()
        self.driver.find_element(By.ID,'cnfbox_modal_ok').click()
        sleep(5)

    def stopLastMonthCheck(self):
        self.fill_last_month = False

    def MarkLastMonth(self):
        totals_rows=[]
        i=1
        self.count=1
        while self.staleElement and i <= self.count:
            if self.fill_last_month:
                self.GotoPreviousMonth()
            totals_rows = self.findAbsentCount()
            if totals_rows:
                totals_rows[0].click()
                self.fillModal()
            i = i  + 1
    
    def MarkCurrentMonth(self):
        totals_rows=[]
        i=1
        self.GotoCurrentMonth()
        self.count = 1
        while self.staleElement and i <= self.count:
            totals_rows = self.findAbsentCount()
            if totals_rows:
                totals_rows[0].click()
                self.fillModal()
            i = i  + 1

        
    
    def markAttendance(self):
        self.MarkLastMonth()
        self.MarkCurrentMonth()
        
    def closeDriver(self):
        self.driver.close()


def main():
    attedanceObj = Attendance()
    attedanceObj.login()
    attedanceObj.GotoAttendance()
    attedanceObj.markAttendance()
    attedanceObj.closeDriver()

if __name__ == "__main__":
    main()


