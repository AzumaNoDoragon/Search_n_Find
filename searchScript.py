from playwright.sync_api import sync_playwright, expect
from datetime import datetime
import time, re, requests, os
import pyautogui as py
from connect import *

conexao = connect()
cursor = conexao.cursor()
conexao, cursor = reconectar(conexao, cursor)

def botTelegram():
    token = configToken
    chat_id = configChatId
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "A busca que estava sendo realizada ACABOU!!!"
    }
    requests.post(url, data=payload)

with open ("config.txt", "r", encoding='utf-8') as conf:
    set = conf.readlines()
    configTermo = set[0].strip()
    selecionado = set[1].strip()
    configBusca = set[2].strip()
    configToken = set[3].strip()
    configChatId = set[4].strip()

if selecionado == "1":
    comandoUser = f'SELECT COUNT(*) AS total FROM cidades WHERE validacao = 0'
    cursor.execute(comandoUser)
    result = cursor.fetchone()
    busca = "Geral"
    count = result[0]
elif selecionado == "2":
    comandoUser = f'SELECT COUNT(*) AS total FROM cidades WHERE estado = "{configBusca}" And validacao = 0'
    cursor.execute(comandoUser)
    result = cursor.fetchone()
    busca = "Estado"
    count = result[0] 
elif selecionado == "3":
    comandoUser = f'SELECT COUNT(*) AS total FROM cidades WHERE cidade = "{configBusca}"'
    cursor.execute(comandoUser)
    result = cursor.fetchone()
    busca = "Cidade"
    count = result[0] 

with sync_playwright() as p:
    termo = configTermo
    id = 1
    conexao = connect()
    cursor = conexao.cursor()
    while count != 0:
        conexao, cursor = reconectar(conexao, cursor)
        navegador = p.chromium.launch(headless=False)
        page = navegador.new_page()
        page.goto("https://www.google.com/search?q=mecanica+na+cidade+de+londrina&sca_esv=561755169&tbm=lcl&sxsrf=AB5stBh_wxNhVAqo3uSLB5uCu8ZRGD2WXw:1693522253666&ei=TRnxZLKdKKSK5OUPiLyD6A8&oq=Mecanica+na+cidade+de+lo&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhhNZWNhbmljYSBuYSBjaWRhZGUgZGUgbG8qAggAMgUQIRigATIFECEYoAEyBRAhGKABSMoWULwIWPQJcAB4AJABAJgBqQGgAdMDqgEDMC4zuAEDyAEA-AEBwgIEECMYJ4gGAQ&sclient=gws-wiz-local&pccc=1#rlfi=hd:;si:;mv:[[-23.2562316,-51.122445],[-23.3707438,-51.1885775]];start:20")
        time.sleep(10)
        if selecionado == "1":
            comandoUser = f'SELECT `cidade`, `estado`, `id` FROM `cidades` WHERE validacao=0 LIMIT 1'
        elif selecionado == "2":
            comandoUser = f'SELECT `cidade`, `estado`, `id` FROM `cidades` WHERE validacao=0 and estado = "{configBusca}" LIMIT 1'
        elif selecionado == "3":
            comandoUser = f'SELECT `cidade`, `estado`, `id` FROM `cidades` WHERE validacao=0 and cidade = "{configBusca}" LIMIT 1'
        cursor.execute(comandoUser)
        records = cursor.fetchall()
        for row in records:
            cidade = row[0]
            estado = row[1]
            id = row[2]

        page.locator('//*[@id="APjFqb"]').fill(f'{termo} na cidade de {cidade}, {estado}')
        page.locator('//*[@id="tsf"]/div[1]/div[1]/div[2]/button').click()
        time.sleep(10)
        increment = 2
        inexistente = False
        while inexistente != True:
            conexao, cursor = reconectar(conexao, cursor)
            result = None
            div = str(increment)
            try:
                barraPesquisa = page.locator('//*[@id="APjFqb"]').text_content()
                pesquisa = (f'{termo} na cidade de {cidade}, {estado}')
                if barraPesquisa != pesquisa:
                    page.go_back()
                    time.sleep(5)
            except:
                pass
            try:
                page.locator(f'xpath=//html/body/div[2]/div/div[8]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{div}]').click()
                time.sleep(5)
                result = page.locator(f'xpath=//html/body/div[2]/div/div[8]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/g-flippy-carousel').all_inner_texts()
            except:
                inexistente = True
            time.sleep(10)
            try:
                divisao = str(result).split("Telefone: ", 1)
                telefone = divisao[1]
                telefoneCerto = str("55" + telefone[:15].replace("(", "").replace(")", "").replace(" ", "").replace("-", "").replace("\\", "").replace("n", ""))
                nome = page.locator('xpath=//html/body/div[2]/div/div[8]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[2]/div/div[1]').text_content()
                seleciona = r'SELECT  id, telefone FROM `resultados` WHERE telefone="{}"'.format(telefoneCerto)
                cursor.execute(seleciona)
                resultado = cursor.fetchall()
                if resultado:
                    idReturn = resultado[0][0]
                    agora = datetime.now()
                    agora_str = agora.strftime('%Y-%m-%d %H:%M:%S')
                    atualizar = f"UPDATE `resultados` SET `dataModificacao`='{agora_str}' WHERE id={idReturn}"
                    cursor.execute(atualizar)
                    conexao.commit()
                else:
                    inserir = f'INSERT INTO `resultados`(`nome`, `telefone`, `segmento`, `cidade`, `estado`, `busca`, `enviado`, `testado`, `dataModificacao`) VALUES ("{nome}", "{telefoneCerto}", "{termo}", "{cidade}", "{estado}", "{busca}", "0", "0", "{agora_str}")'
                    cursor.execute(inserir)
                    conexao.commit()
            except:
                pass
            increment+=2
        time.sleep(5)
        nextInexistente = False
        while nextInexistente != True:
            try:
                barraPesquisa = page.locator('//*[@id="APjFqb"]').text_content()
                pesquisa = (f'{termo} na cidade de {cidade}, {estado}')
                if barraPesquisa != pesquisa:
                    page.go_back()
                    time.sleep(5)
            except:
                pass
            conexao, cursor = reconectar(conexao, cursor)
            time.sleep(5)
            inexistente = False
            try:
                page.locator('//*[@id="pnnext"]').click()
            except:
                atualizar = f'UPDATE `cidades` SET `validacao`=1 WHERE `id`={id}'
                cursor.execute(atualizar)
                conexao.commit()
                break
            increment = 2
            while inexistente != True:
                try:
                    barraPesquisa = page.locator('//*[@id="APjFqb"]').text_content()
                    pesquisa = (f'{termo} na cidade de {cidade}, {estado}')
                    if barraPesquisa != pesquisa:
                        page.go_back()
                        time.sleep(5)
                except:
                    pass
                conexao, cursor = reconectar(conexao, cursor)
                cursor = conexao.cursor()
                result = None
                time.sleep(5)
                div = str(increment)
                try:
                    page.locator(f'xpath=//html/body/div[2]/div/div[8]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{div}]').click()
                    time.sleep(5)
                    result = page.locator(f'xpath=//html/body/div[4]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]').all_inner_texts()
                except:
                    inexistente = True
                    time.sleep(5)
                try:
                    divisao = str(result).split("Telefone: ", 1)
                    telefone = divisao[1]
                    telefoneCerto = str("55" + telefone[:15].replace("(", "").replace(")", "").replace(" ", "").replace("-", "").replace("\\", "").replace("n", ""))
                    nome = page.locator('xpath=//html/body/div[4]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[2]/div/div[1]').text_content()
                    seleciona = r'SELECT  id, telefone FROM `resultados` WHERE telefone="{}"'.format(telefoneCerto)
                    cursor.execute(seleciona)
                    resultado = cursor.fetchall()
                    if resultado:
                        idReturn = resultado[0][0]
                        agora = datetime.now()
                        agora_str = agora.strftime('%Y-%m-%d %H:%M:%S')
                        atualizar = f"UPDATE `resultados` SET `dataModificacao`='{agora_str}' WHERE id={idReturn}"
                        cursor.execute(atualizar)
                        conexao.commit()
                    else:
                        inserir = f' INSERT INTO `resultados`(`nome`, `telefone`, `segmento`, `cidade`, `estado`, `busca`, `dataModificacao`) VALUES ("{nome}", "{telefoneCerto}", "{termo}", "{cidade}", "{estado}", "{busca}", "{agora_str}")'
                        cursor.execute(inserir)
                        conexao.commit()
                except:
                    pass
                increment+=2
        count -= 1
        page.close()
        navegador.close()
        cursor.close()
        conexao.close()
botTelegram()