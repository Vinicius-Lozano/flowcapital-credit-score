# 💰 FlowCapital — Crédito Inteligente com Open Finance

## 📌 Visão Geral

O **FlowCapital** é uma plataforma de análise de crédito que conecta usuários e empresas, utilizando dados financeiros reais para reduzir burocracia e acelerar decisões de crédito.

A proposta é oferecer um **score rápido, acessível e confiável**, facilitando o acesso ao crédito e ajudando empresas a encontrar bons clientes.

---

## 🚨 Problema

O processo tradicional de análise de crédito é:

* burocrático
* demorado
* pouco acessível

Além disso:

* empresas têm dificuldade em avaliar risco com segurança
* instituições têm dificuldade em encontrar bons clientes
* usuários enfrentam barreiras para conseguir crédito

---

## 🎯 Público-alvo

### 🏢 B2B (Empresas)

* empresas que desejam avaliar clientes com mais segurança
* instituições que buscam reduzir risco

### 👤 B2C (Usuários)

* pessoas em busca de crédito rápido
* usuários sem histórico bancário tradicional

---

## 🚀 Solução

O FlowCapital oferece uma plataforma simples e rápida que:

* gera score de crédito instantaneamente
* analisa entradas e despesas do usuário
* reduz burocracia no processo
* compartilha o score com empresas (com consentimento via Open Finance)

---

## 🔥 Diferencial

* ⚡ Resposta rápida
* 🧾 Baixa burocracia
* 🔗 Integração com Open Finance
* 📊 Visualização clara do perfil financeiro

---

## 🔄 Fluxo da Plataforma

1. Usuário acessa a plataforma
2. Obtém seu score de crédito
3. Autoriza o compartilhamento de dados
4. O sistema envia o score para empresas
5. Empresas analisam e retornam propostas
6. Usuário recebe ofertas de crédito

---

## ⚙️ Funcionalidades

* Cadastro e login com CPF
* Validação de CPF e senha segura
* Dashboard com score de crédito
* Análise de entradas e despesas
* Integração com Open Finance (Pluggy)
* Painel administrativo

---

## 🧠 Modelo de Score

### 📥 Dados utilizados

* renda
* despesas
* frequência de entradas
* transações bancárias (Open Finance)

---

### 🧮 Cálculo

O score varia de **0 a 1000**, baseado em uma fórmula que considera a relação entre renda e despesas.

---

### 📊 Classificação

* **Aprovado** → baixo risco
* **Microcrédito** → risco moderado
* **Negado** → alto risco

---

## 🏗️ Arquitetura

![Arquitetura do Sistema](flowcapital_diagrama.png)

---

## 🛠️ Tecnologias Utilizadas

* Django (Python)
* Quasar (Vue.js)
* JavaScript, HTML, CSS
* PostgreSQL
* AWS (EC2, S3, RDS)
* Pluggy (Open Finance)
* Docker

---

## ☁️ Deploy

* EC2 → backend
* S3 → frontend / assets
* CloudFront → distribuição
* RDS → banco de dados

---

## 🐳 Execução com Docker (Recomendado)

```bash
docker-compose up --build
```

👉 Não é necessário subir backend e frontend separadamente.

---

## ▶️ Execução Manual (Opcional)

### Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
quasar dev
```

---

## 📱 Responsividade

A aplicação é responsiva e pode ser utilizada em dispositivos móveis (via build do frontend).

---

## ⚠️ Limitações

* não foi implementado o dashboard para empresas (B2B)
* não foi implementado modelo de IA avançado (apenas fórmula)
* sistema ainda em nível de protótipo

---

## 🔮 Melhorias Futuras

* dashboard para empresas com ranking de clientes
* uso de Machine Learning para score
* sistema de recomendação de crédito
* melhorias na experiência mobile

---

## 💰 Modelo de Negócio

* empresas pagam para acessar e avaliar clientes
* a plataforma recebe comissão sobre créditos aprovados

---

## 📌 Conclusão

O FlowCapital propõe uma forma mais rápida e acessível de análise de crédito, utilizando Open Finance para conectar usuários e empresas de forma eficiente.
