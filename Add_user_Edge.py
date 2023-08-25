from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


# Khởi tạo trình điều khiển Edge
driver = webdriver.Edge()

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
data_path = './dataAddUser.csv'

# Đọc file CSV và tạo DataFrame
df = pd.read_csv(data_path)
for index, row in df.iterrows():
    driver.get("http://localhost/orangehrm-4.5/orangehrm-4.5/symfony/web/index.php/admin/saveSystemUser")
    driver.implicitly_wait(10)
    
    employee_name = driver.find_element(By.XPATH, '//*[@id="systemUser_employeeName_empName"]')
    user_name = driver.find_element(By.XPATH, '//*[@id="systemUser_userName"]')
    password = driver.find_element(By.XPATH, '//*[@id="systemUser_password"]')
    confirm_password = driver.find_element(By.XPATH, '//*[@id="systemUser_confirmPassword"]')

    employee_name.send_keys(row['Employee Name'])
    user_name.send_keys(row['Username'])
    password.send_keys(row['Password'])
    confirm_password.send_keys(row['Confirm Password']) 
    wait = WebDriverWait(driver, 10)
    
    submit_btn = driver.find_element(By.XPATH, '//*[@id="btnSave"]')
    submit_btn.click()
    
    time.sleep(3)

    if driver.current_url == 'http://localhost/orangehrm-4.5/orangehrm-4.5/symfony/web/index.php/admin/viewSystemUsers':
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