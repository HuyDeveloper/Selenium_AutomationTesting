from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


# Khởi tạo trình điều khiển Firefox
driver = webdriver.Firefox()

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
data_path = './dataAddVacancies.csv'

# Đọc file CSV và tạo DataFrame
df = pd.read_csv(data_path)
for index, row in df.iterrows():
    driver.get("http://localhost/orangehrm-4.5/orangehrm-4.5/symfony/web/index.php/recruitment/addJobVacancy")
    driver.implicitly_wait(10)
    
    # job_title = driver.find_element(By.XPATH, '//*[@id="addJobVacancy_jobTitle"]')
    vacancy_name = driver.find_element(By.XPATH, '//*[@id="addJobVacancy_name"]')
    hiring_manager = driver.find_element(By.XPATH, '//*[@id="addJobVacancy_hiringManager"]')
    number_of_positions = driver.find_element(By.XPATH, '//*[@id="addJobVacancy_noOfPositions"]')   
    

    if(pd.isna(row['Job Title']) != True):
        Select(driver.find_element(By.XPATH, '//*[@id="addJobVacancy_jobTitle"]')).select_by_visible_text(row['Job Title'])
    vacancy_name.send_keys(row['Vacancy Name'])
    hiring_manager.send_keys(row['Hiring Manager'])
    if(pd.isna(row['Number of Positions']) != True):
        number_of_positions.send_keys(row['Number of Positions'])
    
    
    submit_btn = driver.find_element(By.XPATH, '//*[@id="btnSave"]')
    submit_btn.click()
    
    time.sleep(3)
    
    html_content = driver.page_source
    

    if "<h1>Attachments</h1>" in html_content :
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