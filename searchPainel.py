from connect import *
import tkinter as tk, requests
from tkinter import font, OptionMenu
import subprocess, threading, os

conexao = connect()
cursor = conexao.cursor()
conexao, cursor = reconectar(conexao, cursor)
global configTermo
global configBusca
global configTelegram
global selecionado
configTermo = ""
selecionado = ""
configBusca = ""
configTelegram = []

def run_script():   
    janela.quit()
    subprocess.Popen(["cmd", "/c", "runhiddenScript.cmd"])

def configurar():
    global configTermo
    global configBusca
    global configTelegram
    global selecionado
    conexao = connect()
    cursor = conexao.cursor()
    conexao, cursor = reconectar(conexao, cursor)
    configTermo = caixa_termo.get("1.0", "end-1c")
    atualizar = f"UPDATE `cidades` SET `validacao`= 0 WHERE 1"
    cursor.execute(atualizar)
    conexao.commit()
    with open ("config.txt", "w", encoding='utf-8') as conf:
        conf.write(f"{configTermo}\n{selecionado}\n{configBusca}\n{configTelegram[0]}\n{configTelegram[1]}")
    time.sleep(5)
    thread = threading.Thread(target=run_script)
    thread.start()

def iniciar():
    thread = threading.Thread(target=run_script)
    thread.start()

def botTelegram():
    global configTelegram
    token = caixa_tok.get("1.0", "end-1c").strip()  # Obtém o token da caixa de texto
    chat_id = caixa_id.get("1.0", "end-1c").strip()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "Teste de bot...\nFuncionando!"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:  # Verifica se o status code da resposta é 200 (OK)
        configTelegram = [token, chat_id]
        return configTelegram
    else:
        return None

def atualizar_busca_selecionada(*args):
    global busca_selecionada
    global configBusca
    configBusca = busca_selecionada.get()
    
def carregar_estados(cursor):
    cursor.execute("SELECT DISTINCT estado FROM cidades")  # Ajuste a query de acordo com a sua tabela de estados
    return [estado[0] for estado in cursor.fetchall()]

def carregar_cidades(cursor):
    cursor.execute("SELECT cidade FROM cidades ORDER BY cidade")  # Ajuste a query de acordo com a sua tabela de estados
    return [cidades[0] for cidades in cursor.fetchall()]

if os.path.exists("config.txt"):
    with open ("config.txt", "r", encoding='utf-8') as conf:
        set = conf.readlines()
        configTermo = set[0].strip()
        selecionado = set[1].strip()
        configBusca = set[2].strip()
        configToken = set[3].strip()
        configChatId = set[4].strip()

def selecionar_opcao():
    global containerStatus
    global busca_selecionada
    global configBusca
    global selecionado
    
    selecionado = opcao.get()
    
    containerStatus.destroy()
    containerStatus = tk.Frame(container_Metodo, borderwidth=1, relief="groove")
    containerStatus.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    if selecionado == 1:
        labelMetodo = tk.Label(containerStatus, text="Brasil:")
        labelMetodo.grid(row=0, column=0, padx=10, pady=0)
        caixaMetodo = tk.Text(containerStatus, height=1, width=43)
        caixaMetodo.insert(tk.END, "Todas as 5595 cidades do país.")
        caixaMetodo.configure(state="disabled")
        caixaMetodo.grid(row=0, column=1, padx=10, pady=10)
        configBusca = "Todas"
    elif selecionado == 2:
        labelbusca = tk.Label(containerStatus, text="Estado:")
        labelbusca.grid(row=0, column=0, padx=10, pady=0)

        # Obter os estados do banco de dados
        busca = carregar_estados(cursor)

        # Criar um OptionMenu para os estados
        busca_selecionada = tk.StringVar(containerStatus)
        busca_selecionada.set("Selecione um estado")  # Valor padrão

        busca_selecionada.trace_add("write", atualizar_busca_selecionada)
        menu_busca = OptionMenu(containerStatus, busca_selecionada, *busca)
        menu_busca.grid(row=0, column=1, padx=10, pady=10)
    elif selecionado == 3:
        labelbusca = tk.Label(containerStatus, text="Cidade:")
        labelbusca.grid(row=0, column=0, padx=10, pady=0)

        # Obter as cidades do banco de dados
        busca = carregar_cidades(cursor)

        # Declarar a variável global busca_selecionado
        busca_selecionada = tk.StringVar(containerStatus)
        busca_selecionada.set("Selecione a cidade")  # Valor padrão

        # Adicionar o trace para a função
        busca_selecionada.trace_add("write", atualizar_busca_selecionada)

        menu_busca = tk.OptionMenu(containerStatus, busca_selecionada, *busca)
        menu_busca.grid(row=0, column=1, padx=10, pady=10)

janela = tk.Tk()
janela.title("Scrapping Maps")

# Configuração da janela
largura = 500
altura = 500
posicao_x = (janela.winfo_screenwidth() // 2) - (largura // 2)
posicao_y = (janela.winfo_screenheight() // 2) - (altura // 2)
janela.geometry(f"{largura}x{altura}+{posicao_x}+{posicao_y}")
janela.resizable(False, False)

# Configuração da fonte
fonte_padrao = font.nametofont("TkDefaultFont")
fonte_padrao.configure(size=12, family="Arial")  # Define o tamanho e a família da fonte padrão

# Configuração dos containers
container_Busca = tk.Frame(janela, borderwidth=1, relief="groove")
container_Busca.pack(padx=10, pady=5)
container_Metodo = tk.Frame(janela, borderwidth=1, relief="groove")
container_Metodo.pack(padx=10, pady=5)
container_Bot = tk.Frame(janela, borderwidth=1, relief="groove")
container_Bot.pack(padx=10, pady=5)

# Configuração do primeiro container
label_Busca = tk.Label(container_Busca, text="Bot de Busca", font=("Arial", 15))
label_Busca.grid(row=0, column=0, padx=0, pady=5)
label_termo = tk.Label(container_Busca, text="Termo de busca:")
label_termo.grid(row=1, column=0, padx=10, pady=0)
caixa_termo = tk.Text(container_Busca, height=1, width=38)
caixa_termo.insert("1.0", configTermo)
caixa_termo.grid(row=1, column=1, padx=10, pady=10)
configTermo = caixa_termo

# Configuração do segundo container
opcao = tk.IntVar(value=0) 
label_Busca = tk.Label(container_Metodo, text="Método de Busca", font=("Arial", 15))
label_Busca.grid(row=0, column=0, padx=5, pady=5)

opcao1 = tk.Radiobutton(container_Metodo, text="Todo o Brasil", variable=opcao, value=1, command=selecionar_opcao)
opcao1.grid(row=3, column=0, padx=5, pady=5)
opcao2 = tk.Radiobutton(container_Metodo, text="Escolher Estado", variable=opcao, value=2, command=selecionar_opcao)
opcao2.grid(row=3, column=1, padx=5, pady=5)
opcao3 = tk.Radiobutton(container_Metodo, text="Escolher Cidade", variable=opcao, value=3, command=selecionar_opcao)
opcao3.grid(row=3, column=2, padx=5, pady=5)
containerStatus = tk.Frame(container_Metodo, borderwidth=1, relief="groove")
containerStatus.grid(row=4, column=0, columnspan=3, padx=10, pady=5)
labelMetodo = tk.Label(containerStatus, text="Selecione uma Opção")
labelMetodo.grid(row=0, column=0, padx=10, pady=0)

# Configuração do terceiro container
label_bot = tk.Label(container_Bot, text="Bot Telegram", font=("Arial", 15))
label_bot.grid(row=2, column=0, padx=0, pady=5)
label_tok = tk.Label(container_Bot, text="Token:")
label_tok.grid(row=3, column=0, padx=10, pady=0)
caixa_tok = tk.Text(container_Bot, height=1, width=36)
caixa_tok.grid(row=3, column=1, padx=10, pady=10)
caixa_tok.insert("1.0", configToken)

label_id = tk.Label(container_Bot, text="chat_id:")
label_id.grid(row=4, column=0, padx=10, pady=0)
caixa_id = tk.Text(container_Bot, height=1, width=36)
caixa_id.grid(row=4, column=1, padx=10, pady=10)
caixa_id.insert("1.0", configChatId)

buttonTeste = tk.Button(container_Bot, text="Teste", command=botTelegram)
buttonTeste.grid(row=5, column=1, padx=10, pady=10)

# Configuração botão salvar
buttonSalvar = tk.Button(janela, text="Salvar e Iniciar", command=configurar)
buttonSalvar.pack(padx=50, pady=0)
buttonIniciar = tk.Button(janela, text="Iniciar", command=iniciar)
buttonIniciar.pack(padx=120, pady=0)

janela.mainloop()