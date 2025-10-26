# 📧 Email Classifier AI - AutoU

![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)
![ML](https://img.shields.io/badge/ML-Naive%20Bayes-orange.svg)
![NLP](https://img.shields.io/badge/NLP-Scikit--learn-lightblue.svg)

---

## 🚀 Visão Geral

Sistema inteligente de **classificação automática de emails** que utiliza **Processamento de Linguagem Natural (NLP)** e o algoritmo **Naive Bayes** para categorizar emails em **Produtivo** ou **Improdutivo**, sugerindo **respostas automáticas contextualizadas**.

---

## 🎯 Funcionalidades

### 🤖 Classificação Inteligente
- Algoritmo **Naive Bayes** treinado com dataset em português  
- Pré-processamento **NLP completo** (tokenização, stop words, lemmatization)  
- Fallback inteligente baseado em palavras-chave  
- Múltiplas camadas de análise para maior precisão  

### 📄 Suporte Multi-Formato
- Entrada de texto direto via interface web  
- **Arquivos PDF** com extração automática de texto  
- **Drag & Drop** para melhor experiência do usuário  

### 💬 Sistema de Respostas
- Respostas **contextuais** baseadas no conteúdo do email  
- **10+ templates** para cada categoria  
- Respostas **profissionais e personalizadas**  
- Sistema de **fallback robusto**  

---

## 🛠️ Tecnologias Utilizadas

### 🔧 Backend
- **Python 3.9** - Linguagem principal  
- **Flask** - Framework web  
- **Scikit-learn** - Machine Learning (Naive Bayes)  
- **NLTK** - Processamento de Linguagem Natural  
- **PyPDF2** - Extração de texto de PDFs  
- **Pandas & NumPy** - Manipulação de dados  

### 🎨 Frontend
- **HTML5** - Estrutura semântica  
- **CSS3** - Estilos modernos (Design System AutoU)  
- **JavaScript Vanilla** - Interatividade  
- **Bootstrap 5** - Componentes UI  
- **Font Awesome** - Ícones  

---

## ☁️ Deploy & Infraestrutura

- **Render.com** - Hospedagem cloud  
- **GitHub** - Versionamento e CI/CD  
- **CORS** - Comunicação entre serviços  

### ⚙️ Configuração no Render

#### Backend Service
- Tipo: `Web Service`  
- Root Directory: `backend`  
- Build Command: `pip install -r requirements.txt`  
- Start Command: `python app.py`  

#### Frontend Service
- Tipo: `Static Site`  
- Root Directory: `frontend`  
- Publish Directory: `.`  

---

## 📊 Algoritmo de Classificação

### 🔍 Processamento NLP
```python
1. Tokenização → Divide texto em palavras  
2. Remoção Stop Words → Elimina palavras comuns  
3. Lemmatization → Reduz palavras à raiz  
4. Limpeza → Remove caracteres especiais

🚀 Como Executar

📋 Pré-requisitos
- Python 3.9+
🔧 Instalação Local
1️⃣ Clonar o repositório
- git clone https://github.com/seu-usuario/email-classifier.git
cd email-classifier

