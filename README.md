# 💰 FinancialApp

O **FinancialApp** é uma aplicação web em **Python + Flask** para gerenciamento financeiro integrada ao **Google Drive** e **Google Sheets**.  

A aplicação cria automaticamente uma pasta no Google Drive chamada **FinanceApp**, com planilhas para cartões, controle de gastos e despesas parceladas.  

O objetivo é simplificar o gerenciamento financeiro com base em planilhas acessíveis pela nuvem.

---

## 🚀 Funcionalidades

- Autenticação via **OAuth 2.0** do Google.  
- Criação automática da pasta **FinanceApp** no Drive.  
- Criação/uso das planilhas:  
  - **Cards** → Cadastro de cartões.  
  - **Control** → Controle de gastos.  
  - **Parcelados** → Despesas parceladas.  
- Estrutura inicial com colunas já configuradas.  
- API em **Flask** para interagir com os dados.

---

## 📦 Pré-requisitos

- Conta Google com acesso ao **Google Drive** e **Google Sheets**.  
- **Python 3.10+** instalado na máquina.  

> ⚠️ Não é necessário instalar manualmente dependências: o próprio `run.py` cria o ambiente virtual e instala tudo automaticamente.

---

## 🔑 Criando Credenciais OAuth no Google Cloud

1. Acesse o **[Google Cloud Console](https://console.cloud.google.com/)**.  
2. Crie um **novo projeto** (ou selecione um já existente).  
3. Ative as APIs necessárias:  
   - **Google Drive API**  
   - **Google Sheets API**  
4. Vá em **APIs e Serviços > Credenciais**.  
5. Clique em **Criar credenciais > ID do cliente OAuth**.  
6. Tipo de aplicativo: **Aplicativo para computador**.  
7. Após criar, clique em **Download JSON**.  
8. Renomeie o arquivo para **`oauth_credentials.json`** e coloque na **raiz do projeto**.

> ⚠️ Este arquivo contém informações sensíveis, **não compartilhe**.

---

## ▶️ Executando a aplicação

1. Baixe/clonar o repositório:

```bash
git clone https://github.com/Rafael-Kohn/financial-app.git
cd financial-app
```

2. Coloque o arquivo **`oauth_credentials.json`** dentro da pasta do projeto.  

3. Execute:

```bash
python run.py
```

4. No primeiro uso, será exibido um link para autenticação:

```
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth...
```

Abra no navegador, autorize o acesso e copie o código.  
Um arquivo **`token.pickle`** será salvo localmente para não precisar repetir a autenticação.

---

## 🌐 Acessando

Por padrão, a aplicação roda em:

```
http://0.0.0.0:5000
```

Você pode alterar o host e a porta ao iniciar, o `run.py` perguntará:

```
Digite o IP ou enter para default (0.0.0.0):
Digite a porta ou enter para default (5000):
Ativar debug? (s/n) [s]:
```

---

## 🗂 Estrutura do Projeto

```
financial-app/
│── app/
│   ├── __init__.py      # Criação da instância Flask
│   ├── routes.py        # Rotas da aplicação
│── setup_drive.py       # Classe responsável pelo setup no Google Drive
│── config.py            # Configurações
│── run.py               # Inicializa ambiente, dependências e servidor
│── oauth_credentials.json  # (seu arquivo baixado do Google Cloud)
│── token.pickle         # Token salvo após autenticação
```

---

## ⚙️ Como funciona internamente

1. `run.py` cria automaticamente uma **venv** e instala pacotes (`Flask`, `gspread`, `google-api-python-client`, etc).  
2. O usuário autentica via OAuth no Google → gera `token.pickle`.  
3. O **SetupDrive** garante a existência da pasta e planilhas no Drive.  
4. O servidor Flask inicializa e disponibiliza endpoints REST para interagir com os dados.  

---

## 🛠 Futuras melhorias

- CRUD completo para lançamentos.  
- Dashboard com gráficos.  
- Exportação CSV/Excel.  
- Deploy em nuvem. 
- Analise de gastos por IA 

---

## 📄 Licença

Este projeto está sob licença MIT.  
