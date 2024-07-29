from playwright.sync_api import sync_playwright, expect
import mysql.connector, time, re
import pyautogui as py

with sync_playwright() as p:
  termo = py.prompt(text='Digite o termo de pesquisa', title='Inicialização' , default='Mecanica')
  id = 1
  while id <= 5570:
    conexao = mysql.connector.connect(host='', user='', password='', database='')
    cursor = conexao.cursor()
    navegador = p.chromium.launch(headless=False)
    page = navegador.new_page()
    page.goto("https://www.google.com/search?q=mecanica+na+cidade+de+londrina&sca_esv=561755169&tbm=lcl&sxsrf=AB5stBh_wxNhVAqo3uSLB5uCu8ZRGD2WXw:1693522253666&ei=TRnxZLKdKKSK5OUPiLyD6A8&oq=Mecanica+na+cidade+de+lo&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhhNZWNhbmljYSBuYSBjaWRhZGUgZGUgbG8qAggAMgUQIRigATIFECEYoAEyBRAhGKABSMoWULwIWPQJcAB4AJABAJgBqQGgAdMDqgEDMC4zuAEDyAEA-AEBwgIEECMYJ4gGAQ&sclient=gws-wiz-local&pccc=1#rlfi=hd:;si:;mv:[[-23.2562316,-51.122445],[-23.3707438,-51.1885775]];start:20")
    time.sleep(10)
    try:
      comandoUser = f'SELECT `cidade`, `estado`, `id` FROM `cidades{termo}` WHERE validacao=0 LIMIT 1'
      cursor.execute(comandoUser)
    except:
      continue
    records = cursor.fetchall()
    for row in records:
      cidade = row[0]
      estado = row[1]
      id = row[2]
    print(f"Está no id:{id} de 5570 cidades")
    page.locator('//*[@id="APjFqb"]').fill(f'{termo} na cidade de {cidade}, {estado}')
    page.locator('//*[@id="tsf"]/div[1]/div[1]/div[2]/button').click()
    time.sleep(10)
    increment = 2
    inexistente = False
    while inexistente != True:
      conexao = mysql.connector.connect(host='', user='', password='', database='')
      cursor = conexao.cursor()
      try:
        page.locator(f'xpath=//html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{increment}]').click()
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
        seleciona = r'SELECT telefone FROM `' + termo + r'` WHERE telefone="{}"'.format(telefoneCerto)
        cursor.execute(seleciona)
        resultado = cursor.fetchall()
        if len(resultado)!=0:
          print('Numero existente no banco')
        else:
          inserir = f' INSERT INTO `{termo}`(`nome`, `telefone`, `segmento`, `cidade`, `estado`, `enviado`) VALUES ("{nome}", "{telefoneCerto}", "{termo}", "{cidade}", "{estado}", "0")'
          cursor.execute(inserir)
          conexao.commit()
          print(f'\nSubiu para o banco\nNome: {nome}, Telefone: {telefoneCerto}')
      except:
        None
      increment+=2
    time.sleep(5)
    nextInexistente = False
    while nextInexistente != True:
      conexao = mysql.connector.connect(host='', user='', password='', database='')
      cursor = conexao.cursor()
      time.sleep(5)
      inexistente = False
      try:
        page.locator('//*[@id="pnnext"]').click()
      except:
        atualizar = f'UPDATE `cidades{termo}` SET `validacao`=1 WHERE `id`={id}'
        cursor.execute(atualizar)
        conexao.commit()
        break
      increment = 2
      while inexistente != True:
        conexao = mysql.connector.connect(host='', user='', password='', database='')
        cursor = conexao.cursor()
        time.sleep(5)
        try:
          result = page.locator(f'xpath=//html/body/div[4]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{increment}]').click()
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
          seleciona = r'SELECT telefone FROM `' + termo + r'` WHERE telefone="{}"'.format(telefoneCerto)
          cursor.execute(seleciona)
          resultado = cursor.fetchall()
          if len(resultado)!=0:
            print('Numero existente no banco')
          else:
            inserir = f' INSERT INTO `{termo}`(`nome`, `telefone`, `segmento`, `cidade`, `estado`, `enviado`) VALUES ("{nome}", "{telefoneCerto}", "{termo}", "{cidade}", "{estado}", "0")'
            cursor.execute(inserir)
            conexao.commit()
            print(f'\nSubiu para o banco\nNome: {nome}, Telefone: {telefoneCerto}')
        except:
          None
        increment+=2
    page.close()
    navegador.close()
    print("\nUfa, mais uma cidade")