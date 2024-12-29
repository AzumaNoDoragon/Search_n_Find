from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime
import mysql.connector, time, pyautogui as py, requests
from connect import *

def botTelegram():
    token = configToken
    chat_id = configChatId
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "O validador TERMINOU!!!"
    }
    requests.post(url, data=payload)

with open ("config.txt", "r", encoding='utf-8') as conf:
    set = conf.readlines()
    configTermo = set[0].strip()
    selecionado = set[1].strip()
    configBusca = set[2].strip()
    configToken = set[3].strip()
    configChatId = set[4].strip()
    
idbd = 1
validacao = 0
contagem = 0
verificados = 0

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        color_scheme='dark',
        viewport={'width': 1280, 'height': 600}
    )
    testando = "Não"
    page = context.new_page()

    while testando == "Não":
        page.goto("https://web.whatsapp.com")
        time.sleep(30)
        testando = py.confirm(text='Foi Conectado?', title='Conexão', buttons=['Sim', 'Não'])

    conexao = connect()
    cursor = conexao.cursor()

    while int(idbd) != int(validacao):
        conexao, cursor = reconectar(conexao, cursor)
        verificados+=1
        nome = ''
        telefone = ''

        comandoUser = f"SELECT COUNT(id) FROM resultados WHERE id>0"
        cursor.execute(comandoUser)
        records = cursor.fetchall()
        for row in records:
            validacao = row[0]
        try:
            comandoUser = f'SELECT `id`, `nome`, `telefone` FROM `resultados` WHERE `status` IS NULL LIMIT 1'
            cursor.execute(comandoUser)
        except:
            conexao, cursor = reconectar(conexao, cursor)
            comandoUser = f'SELECT `id`, `nome`, `telefone` FROM `resultados` WHERE `status` IS NULL LIMIT 1'
            cursor.execute(comandoUser)
        records = cursor.fetchall()
        if not records:
            botTelegram()
            break
        else:
            for row in records:
                idbd = row[0]
                nome = row[1]
                telefone = row[2]
        if not telefone or not str(telefone).isnumeric():
            comando_sql = f'UPDATE `resultados` SET `status`="0" WHERE id={idbd}'
            cursor.execute(comando_sql)
            conexao.commit()
            contagem+=1
            continue
        link = "https://web.whatsapp.com/send?phone="+str(telefone)
        try:
            page.goto(link)
            page.wait_for_selector("xpath=//html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button", timeout=10000)
            page.locator("xpath=//html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button").click()
            comando_sql = f'UPDATE `resultados` SET `status`="0" WHERE id={idbd}'
            cursor.execute(comando_sql)
            conexao.commit()
            contagem += 1
        except:
            comando_sql = f'UPDATE `resultados` SET `status`="1" WHERE id={idbd}'
            cursor.execute(comando_sql)
            conexao.commit()
        try:
            time.sleep(5)
            page.locator("xpath=//html/body/div[1]/div/div/div[4]/header/div[1]/div").click()
            conexao, cursor = reconectar(conexao, cursor)
            atualizar = f'UPDATE `resultados` SET `status`="1" WHERE id={idbd}'
            cursor.execute(atualizar)
            conexao.commit()
        except:
            conexao, cursor = reconectar(conexao, cursor)
            atualizar = f'UPDATE `resultados` SET `status`="0" WHERE id={idbd}'
            cursor.execute(atualizar)
            conexao.commit()
    cursor.close()
    conexao.close()
    page.close()