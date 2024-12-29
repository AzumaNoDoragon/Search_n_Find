# Search_n_Find

**Automatiza a busca e coleta de informações de empresas no Google para cadastro em banco de dados e validação de contatos via WhatsApp Web.**
**Atualização com GUI**
![ScrapingMaps](https://github.com/user-attachments/assets/b8174ba4-df1c-473a-a459-2c0c522b2906)

## Requisitos
- Python instalado
- Um banco de dados MySQL configurado com duas tabelas:
  - **Tabela de Cidades**: Contendo as 5570 cidades do Brasil.
  - **Tabela de Resultados**: Para armazenar as informações coletadas (como nome, telefone e status de validação dos contatos).

## Instruções de Uso

1. **Instalação das Bibliotecas**
   - Execute o script `install_libraries.cmd`. Este script irá instalar as bibliotecas necessárias e perguntará se você deseja iniciar a aplicação.

2. **Início da Aplicação**
   - Após a instalação, você pode iniciar a aplicação executando o script `run_script.vbs`.

## Estrutura do Projeto
O projeto possui três principais scripts e um script de conexão:

   - **validador.py**: Realiza a automação da validação de contatos via WhatsApp Web e atualiza o banco de dados para ter apenas resultados com números de WhatsApp validos.
   - **searchPainel.py**: GUI de configuração do scraping (Front-End do sistema).
   - **searchScript.txt**: Arquivo de busca para o scraping (Back-End do sistema).
      - **connect.py**: Contém a função para estabelecer e reconectar a conexão com o banco de dados MySQL (Todos os scripts dependem dele).

## Funcionalidades do projeto
   - Realiza a busca do termo que você especificar em todas as cidades do Brasil, conforme seu banco de dados, retornando todas as respectivas empresas, com nome, telefone, endereço e todos os dados encontrados.
   - Realiza a separação e selecação de apenas números que possuem whatsapp validos (o sistema não garante que seja o número correto da empresa, apenas os coleta do google).
   - Envio de notificação via Telegram ao final da execução dos scripts ou algum erro.

> **Nota:** O código para a criação das tabelas não está incluído neste repositório para preservar a ética. Certifique-se de configurar o banco de dados conforme necessário.
