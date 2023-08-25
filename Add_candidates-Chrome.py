from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Khởi tạo trình điều khiển Chrome
driver = webdriver.Chrome()

# Mở trang web
driver.get('http://localhost/orangehrm-4.5/orangehrm-4.5/symfony/web/index.php/auth/login')

# Tìm phần tử đăng nhập và nhập thông tin đăng nhập
username_input = driver.find_element(By.XPATH, '//*[@id="txtUsername"]')
password_input = driver.find_element(By.XPATH, '//*[@id="txtPassword"]')

username_input.send_keys('Admin')
password_input.send_keys('Quochuy12@')

# Submit form đăng nhập
login_button = driver.find_element(By.XPATH, '//*[@id="btnLogin"]')
login_button.click()

# Chờ một chút để trang web xử lý đăng nhập
wait = WebDriverWait(driver, 10)

# Kiểm tra xem đăng nhập thành công hay không
if driver.current_url == 'http://localhost/orangehrm-4.5/orangehrm-4.5/symfony/web/index.php/dashboard':
    print('Đăng nhập thành công!')
else:
    print('Đăng nhập thất bại!')

# Đường dẫn đến file CSV
data_path = './dataAddCandidates.csv'

# Đọc file CSV và tạo DataFrame
df = pd.read_csv(data_path)
for index, row in df.iterrows():
    driver.get("http://localhost/orangehrm-4.5/orangehrm-4.5/symfony/web/index.php/recruitment/addCandidate")
    driver.implicitly_wait(10)
    
    first_name = driver.find_element(By.XPATH, '//*[@id="addCandidate_firstName"]')
    middle_name = driver.find_element(By.XPATH, '//*[@id="addCandidate_middleName"]')
    last_name = driver.find_element(By.XPATH, '//*[@id="addCandidate_lastName"]')
    email = driver.find_element(By.XPATH, '//*[@id="addCandidate_email"]')
    contact_no = driver.find_element(By.XPATH, '//*[@id="addCandidate_contactNo"]')
    resume = driver.find_element(By.XPATH, '//*[@id="addCandidate_resume"]')
   
    keywords = driver.find_element(By.XPATH, '//*[@id="addCandidate_keyWords"]')
    comment = driver.find_element(By.XPATH, '//*[@id="addCandidate_comment"]')
    date_of_application = driver.find_element(By.XPATH, '//*[@id="addCandidate_appliedDate"]')
    consent = driver.find_element(By.XPATH, '//*[@id="addCandidate_consentToKeepData"]')
    if(pd.isna(row['First Name']) != True):
        first_name.send_keys(row['First Name'])
    if (pd.isna(row['Middle Name']) != True):
        middle_name.send_keys(row['Middle Name'])
    if(pd.isna(row['Last Name']) != True):
        last_name.send_keys(row['Last Name'])
    if(pd.isna(row['Email']) != True):
        email.send_keys(row['Email'])
    if(pd.isna(row['Contact No']) != True):
        contact_no.send_keys(row['Contact No'])
    #job_vacancy = driver.find_element(By.XPATH, '//*[@id="addCandidate_vacancy"]')
    if(pd.isna(row['Job Vacancy']) != True):
        Select(driver.find_element(By.XPATH, '//*[@id="addCandidate_vacancy"]')).select_by_visible_text(row['Job Vacancy'])
    #vacancy_name.send_keys(row['Vacancy Name'])
    if(pd.isna(row['Resume']) != True):
        resume.send_keys(row['Resume'])
    keywords.send_keys(row['Keywords'])
    comment.send_keys(row['Comment'])
    if(pd.isna(row['Date of Application']) != True):
        date_of_application.send_keys(row['Date of Application'])
    consent.send_keys(row['Consent to keep data'])
    
    wait = WebDriverWait(driver, 10)
    
    submit_btn = driver.find_element(By.XPATH, '//*[@id="btnSave"]')
    submit_btn.click()
    
    time.sleep(2)
    result = driver.page_source
    if "<h1>Candidate's History</h1>" in result:
        print(row['Num'])
        print('Thêm thành công!')
        df.loc[index, 'Ouput'] = 'PASS'
    else:
        print(row['Num'])
        print('Thêm thất bại!')
        df.loc[index, 'Ouput'] = 'FAIL'
print(df)
# Đóng trình duyệt
driver.quit()