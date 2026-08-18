from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://www.pdvlink.com.br/suporte/Help_Desk/index.asp")

driver.find_element(By.XPATH, '//*[@id="txtUsuario"]').send_keys("erik.sales ")
driver.find_element(By.XPATH, '//*[@id="txtSenha"]').send_keys("")
driver.find_element(By.XPATH, '//*[@id="btnSubmit"]').click()
print ("Login feito com sucesso")

wait = WebDriverWait(driver, 10) 
element = wait.until(
    EC.presence_of_element_located((By.ID, '/html/body/div[3]')))

processo = set()
dados_completos = []





print("Relatório gerado com sucesso")
driver.quit()
