# 💰 FlowCapital — Credit Score com Open Finance

## 📌 Visão Geral

O **FlowCapital** é uma plataforma de análise de crédito baseada em Open Finance, desenvolvida para oferecer um score mais justo e acessível, especialmente para pessoas sem histórico bancário tradicional.

A solução permite que usuários compartilhem seus dados financeiros com consentimento, possibilitando uma análise mais precisa do seu comportamento financeiro.

---

## 🎯 Problema

Muitos brasileiros, principalmente trabalhadores informais e autônomos, têm dificuldade em conseguir crédito por não possuírem histórico bancário suficiente ou score adequado nos modelos tradicionais.

---

## 🚀 Solução

O FlowCapital utiliza dados financeiros alternativos, como fluxo de caixa, frequência de renda e padrão de gastos, para gerar um score de crédito mais inclusivo e realista.

---

## 👥 Público-alvo

* Trabalhadores autônomos
* Freelancers
* Pequenos empreendedores
* Pessoas sem histórico de crédito

---

## ⚙️ Funcionalidades

* Cadastro e autenticação de usuários
* Integração simulada com Open Finance
* Cálculo de score de crédito
* Dashboard financeiro
* Simulador de crédito
* Recomendações personalizadas

---

## 🧠 Modelo de Score

O score é calculado com base nos seguintes critérios:

* Estabilidade de renda (40%)
* Controle de gastos (30%)
* Frequência de entradas (20%)
* Saldo médio (10%)

Fórmula:

Score = (0.4 × renda) + (0.3 × gastos) + (0.2 × frequência) + (0.1 × saldo)

---

## 🏗️ Arquitetura

### Frontend

* Quasar Framework (Vue.js)
* HTML
* CSS
* JavaScript

### Backend

* Django (Python)

### Banco de Dados

* PostgreSQL / SQLite

---

## ☁️ Deploy

A aplicação foi implantada utilizando serviços da AWS, garantindo escalabilidade, disponibilidade e confiabilidade.

### 🌐 Infraestrutura

* **Frontend (Quasar)**: hospedado via AWS S3 + CloudFront
* **Backend (Django)**: hospedado em AWS EC2
* **Banco de Dados**: AWS RDS (PostgreSQL)

### 🔧 Serviços AWS utilizados

* EC2 (servidor da aplicação)
* S3 (armazenamento de arquivos e frontend)
* CloudFront (CDN para distribuição)
* RDS (banco de dados gerenciado)

---

### 🚀 Acesso ao sistema

* URL: https://seu-projeto.aws.com

*(substituir pela URL real do projeto)*

---

## 🔐 Segurança

* Autenticação de usuários
* Proteção de dados sensíveis
* Consentimento do usuário para compartilhamento de dados

---

## 🛠️ Tecnologias Utilizadas

* Python
* Django
* JavaScript
* Quasar Framework
* HTML
* CSS

---

## ⚠️ Limitações

* Integração com Open Finance é simulada
* Sistema simplificado para fins acadêmicos
* Modelo de score pode ser aprimorado

---

## 🔮 Melhorias Futuras

* Integração com APIs reais de Open Finance
* Implementação de Machine Learning
* Aplicativo mobile
* Sistema de notificações

---

## ▶️ Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/flowcapital-credit-score.git
```

---

### 2. Backend (Django)

```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

---

### 3. Frontend (Quasar)

```bash
cd frontend
npm install
quasar dev
```

---

## 👨‍💻 Equipe

* Nome 1
* Nome 2
* Nome 3

---

## 📄 Licença

Projeto desenvolvido para o Hackathon Semana Ubíqua.
