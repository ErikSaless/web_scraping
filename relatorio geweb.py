from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
import pandas as pd

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://sistemas.sogamax.com.br/sistema/login.php")
sleep(2)
driver.find_element(By.XPATH, '//*[@id="admLogin"]').send_keys("Erik Sales")
driver.find_element(By.XPATH, '//*[@id="admPasswd"]').send_keys("")
driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/form/button').click()
print("Login feito com sucesso")

sleep(2)
driver.get("https://acesso.geweb.com.br/helpdesk/login/00857492000136/866/ERIKSALES/10501/c3Vwb3J0ZWRldjJAc29nYW1heC5jb20uYnI-/1cls")
sleep(2)

processados = set()
dados_completos = []

while True:
    linhas = driver.find_elements(By.XPATH, '//*[@id="tabletickets"]/tr')

    if not linhas:
        print("Nenhuma linha encontrada.")
        break

    for i in range(len(linhas)):
        linhas = driver.find_elements(By.XPATH, '//*[@id="tabletickets"]/tr')  # Atualiza
        linha = linhas[i]
        celulas = linha.find_elements(By.TAG_NAME, "td")

        if len(celulas) < 7:
            continue

        ticket = celulas[0].text.strip()
        motivo = celulas[1].text.strip()
        data_criacao = celulas[4].text.strip()
        status = celulas[6].text.strip()
    
        if ticket in processados or status.lower() == "concluído":
            continue

        visualizar = celulas[7].find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].click();", visualizar)
        sleep(2)

        try:
            data_ultima_interacao = driver.find_element(By.XPATH, '/html/body/div[4]/table/tbody/tr[1]/td[4]').text.strip()
            ultima_interacao = driver.find_element(By.XPATH, '/html/body/div[4]/table/tbody/tr[1]/td[2]').text.strip()
        except:
            data_ultima_interacao = ''
            ultima_interacao = ''

        dados_completos.append([
            ticket,
            status,
            motivo,
            data_criacao,
            data_ultima_interacao,
            ultima_interacao
        ])

        processados.add(ticket)

        driver.back()
        sleep(2)
    break 

df = pd.DataFrame(dados_completos, columns=[
    'Ticket', 'Status', 'Motivo', 'Data de criação',
    'Data da ultima interação', 'Última interação'
])

data_hoje = datetime.now().strftime('%d-%m-%Y')

nome_arquivo = f"RELATORIO_CHAMADOS_{data_hoje}.xlsx"

caminho = fr"C:\\Users\\SUPORTE DEV\\Documents\\RELATORIO DOS CHAMADOS\\EXCEL\\ROBO GEWEB\\RELATORIO_CHAMADOS_.xlsx"

df.to_excel(caminho, index=False)

print("Relatório gerado com sucesso!")
driver.quit()
