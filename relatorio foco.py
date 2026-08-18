from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

options = Options()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

driver.get("https://www.pdvlink.com.br/suporte/Help_Desk/index.asp")
driver.find_element(By.ID, "txtUsuario").send_keys("erik.sales")
driver.find_element(By.ID, "txtSenha").send_keys("")
driver.find_element(By.ID, "btnSubmit").click()
time.sleep(2)

mapa_criticidade = {
    "Crítico": 1,
    "Alto": 2,
    "Intermediário": 3,
    "Baixo": 4
}

tickets = []
index = 1

while True:
    try:
        ticket_div = driver.find_element(By.XPATH, f"/html/body/div[3]/a[{index}]")
        numero = ticket_div.find_element(By.XPATH, f"./div[2]").text.strip()
        nome = ticket_div.find_element(By.XPATH, f"./div[3]").text.strip()
        data_criacao_raw = ticket_div.find_element(By.XPATH, f"./div[5]").text.strip()
        criticidade_raw = ticket_div.find_element(By.XPATH, f"./div[9]").text.strip()
        criticidade = mapa_criticidade.get(criticidade_raw, 0)

        
        if " - " in data_criacao_raw:
            responsavel, data_criacao = data_criacao_raw.split(" - ")
        else:
            responsavel, data_criacao = "DESCONHECIDO", data_criacao_raw

       
        link = ticket_div.get_attribute("href")
        ticket_id = link.split("id=")[-1]

        
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(f"https://www.pdvlink.com.br/suporte/Help_Desk/chamados_detalhes.asp?id={ticket_id}")
        time.sleep(1.5)

       
        try:
            data_ultima_interacao = driver.find_element(By.XPATH, "/html/body/form[7]/table[1]/tbody/tr[3]/td").text.strip()
        except:
            data_ultima_interacao = "N/A"

        try:
            texto_ultima_interacao = driver.find_element(By.XPATH, "/html/body/form[7]/table[1]/tbody/tr[4]/td[2]").text.strip()
        except:
            texto_ultima_interacao = "N/A"

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

      
        tickets.append({
            "Nome do Ticket": f"{numero} - {nome}",
            "Responsável": responsavel.strip(),
            "Data Vencimento": data_criacao.strip(),
            "Prioridade": criticidade,
            "Data Última Interação": data_ultima_interacao,
            "Descrição": texto_ultima_interacao
        })

        index += 1
    except:
        break  

driver.quit()


df = pd.DataFrame(tickets)


def formatar_data(data_str):
    try:
        return pd.to_datetime(data_str, dayfirst=True).strftime("%d/%m/%Y %H:%M")
    except:
        return data_str


caminho_excel = "C:\\Users\\SUPORTE DEV\\Documents\\PROJETOS\\CLICK\\ chamados.xlsx"
df.to_excel(caminho_excel, index=False)
