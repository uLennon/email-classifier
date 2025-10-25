import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import PyPDF2
import random


# Download recursos NLTK
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt_tab')
except:
    print("⚠️ Recursos NLTK já baixados")

class ProcessadorTexto:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words_pt = set(stopwords.words('portuguese'))
        self.stop_words_en = set(stopwords.words('english'))
        self.stop_words = self.stop_words_pt.union(self.stop_words_en)
        print("🔧 Processador de Texto inicializado")
    
    def extrair_texto_pdf(self, arquivo_pdf):
        """
        Extrai texto de arquivos PDF
        """
        print("📄 Extraindo texto do PDF...")
        try:
            pdf_reader = PyPDF2.PdfReader(arquivo_pdf)
            texto = ""
            for pagina in pdf_reader.pages:
                texto += pagina.extract_text() + "\n"
            print(f"✅ PDF processado: {len(texto)} caracteres")
            return texto
        except Exception as e:
            print(f"❌ Erro ao extrair PDF: {e}")
            return ""
    
    def preprocessar_texto(self, texto):
        """
        Pré-processamento completo do texto
        """
        print("🔄 Pré-processando texto...")
        
        # 1. Conversão para minúsculo
        texto = texto.lower()
        
        # 2. Remoção de caracteres especiais, números e URLs
        texto = re.sub(r'http\S+', '', texto)  # Remove URLs
        texto = re.sub(r'[^a-zA-ZÀ-ÿ\s]', ' ', texto)  # Mantém apenas letras e espaços
        texto = re.sub(r'\s+', ' ', texto)  # Remove múltiplos espaços
        
        # 3. Tokenização
        tokens = word_tokenize(texto, language='portuguese')
        print(f"   ✅ Tokenização: {len(tokens)} tokens")
        
        # 4. Remoção de stop words
        tokens_sem_stopwords = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        print(f"   ✅ Stop words removidas: {len(tokens_sem_stopwords)} tokens")
        
        # 5. Lemmatization
        tokens_lemmatized = [self.lemmatizer.lemmatize(token) for token in tokens_sem_stopwords]
        print(f"   ✅ Lemmatization aplicada")
        
        # 6. Reconstrução do texto
        texto_processado = ' '.join(tokens_lemmatized)
        print(f"   📊 Texto processado: {texto_processado[:100]}...")
        
        return texto_processado

class ClassificadorNaiveBayes:
    def __init__(self):
        self.modelo = None
        self.vectorizer = None
        self._treinar_modelo()
        print("🎯 Classificador Naive Bayes inicializado")
    
    def _criar_dataset_treinamento(self):
        """
        Cria dataset de treinamento para emails em português
        """
        # Emails produtivos (requerem ação)
        emails_produtivos = [
            "preciso de ajuda com erro no sistema",
            "solicito suporte técnico urgente",
            "problema com acesso à plataforma",
            "não consigo fazer login na conta",
            "erro ao processar pagamento",
            "sistema apresenta falha crítica",
            "necessito assistência com software",
            "relatório não está gerando",
            "dúvida sobre funcionalidade do produto",
            "como configurar nova conta",
            "problema de conectividade com servidor",
            "atualização quebrou funcionalidade",
            "bug na interface do usuário",
            "solicitação de novo recurso",
            "problema de performance no sistema",
            "erro na importação de dados",
            "backup não está funcionando",
            "relatório com dados incorretos",
            "sistema lento para carregar",
            "integração com API falhando",
            "problema de segurança detectado",
            "dados corrompidos no banco",
            "funcionalidade não responde",
            "erro crítico na aplicação",
            "suporte necessário para implantação"
        ]
        
        # Emails improdutivos (cumprimentos, agradecimentos)
        emails_improdutivos = [
            "obrigado pela ajuda",
            "parabéns pelo excelente trabalho",
            "feliz natal e ano novo",
            "agradeço o suporte da equipe",
            "cumprimentos à diretoria",
            "excelente atendimento ao cliente",
            "felicitações pelo aniversário",
            "bom trabalho da equipe técnica",
            "agradecimento pelo serviço prestado",
            "saudações cordiais a todos",
            "reconhecimento pelo empenho",
            "feliz ano novo prospero",
            "boas festas de final de ano",
            "parabéns pelo projeto concluído",
            "agradecimento pela parceria",
            "felicidades para a empresa",
            "cumprimentos de boa tarde",
            "reconhecimento do bom trabalho",
            "agradeço a atenção dispensada",
            "feliz páscoa para todos",
            "parabéns pelo aniversário da empresa",
            "saudações aos colegas de trabalho",
            "agradecimento pelo rápido retorno",
            "feliz dia dos namorados",
            "cumprimentos de bom dia"
        ]
        
        textos = emails_produtivos + emails_improdutivos
        labels = [1] * len(emails_produtivos) + [0] * len(emails_improdutivos)  # 1=Produtivo, 0=Improdutivo
        
        return textos, labels
    
    def _treinar_modelo(self):
        """
        Treina o modelo Naive Bayes
        """
        print("🤖 Treinando modelo Naive Bayes...")
        
        # Cria dataset de treinamento
        textos, labels = self._criar_dataset_treinamento()
        
        # Cria pipeline de processamento
        self.modelo = Pipeline([
            ('vectorizer', CountVectorizer(ngram_range=(1, 2), max_features=1000)),
            ('classifier', MultinomialNB())
        ])
        
        # Treina o modelo
        self.modelo.fit(textos, labels)
        print("✅ Modelo treinado com sucesso!")
    
    def classificar(self, texto):
        """
        Classifica texto usando Naive Bayes
        """
        try:
            probabilidades = self.modelo.predict_proba([texto])[0]
            predicao = self.modelo.predict([texto])[0]
            confianca = max(probabilidades)
            
            print(f"🎯 Naive Bayes - Predição: {'Produtivo' if predicao == 1 else 'Improdutivo'}")
            print(f"🎯 Confiança: {confianca:.3f}")
            
            if confianca > 0.6:  # Confiança mínima
                return "Produtivo" if predicao == 1 else "Improdutivo"
            else:
                return self._classificacao_fallback(texto)
                
        except Exception as e:
            print(f"❌ Erro Naive Bayes: {e}")
            return self._classificacao_fallback(texto)
    
    def _classificacao_fallback(self, texto):
        """
        Fallback baseado em palavras-chave
        """
        texto_lower = texto.lower()
        
        palavras_produtivas = [
            'problema', 'erro', 'bug', 'falha', 'ajuda', 'suporte', 'urgente',
            'solicitação', 'não funciona', 'não consigo', 'preciso de ajuda',
            'como fazer', 'dúvida', 'questão', 'pagamento', 'fatura', 'contrato'
        ]
        
        palavras_improdutivas = [
            'obrigado', 'parabéns', 'feliz natal', 'ano novo', 'boas festas',
            'agradecimento', 'cumprimentos', 'excelente trabalho', 'felicitações'
        ]
        
        score_produtivo = sum(1 for palavra in palavras_produtivas if palavra in texto_lower)
        score_improdutivo = sum(1 for palavra in palavras_improdutivas if palavra in texto_lower)
        
        print(f"🎯 Fallback - Produtivo: {score_produtivo}, Improdutivo: {score_improdutivo}")
        
        return "Produtivo" if score_produtivo > score_improdutivo else "Improdutivo"

class GeradorRespostas:
    def __init__(self):
        self.respostas_produtivo = [
            "Agradecemos seu contato sobre a questão relatada. Nossa equipe analisará sua solicitação e retornará em até 24 horas úteis com uma solução.",
            "Recebemos sua solicitação. Nossa equipe técnica está analisando o caso e retornará com um posicionamento em breve.",
            "Obrigado pelo seu email. Estamos revisando as informações fornecidas e retornaremos com uma resposta completa em até 48 horas.",
            "Agradecemos a mensagem sobre o problema relatado. Nossa equipe de suporte já foi acionada e entrará em contato em até 2 horas úteis.",
            "Confirmamos o recebimento de sua solicitação. Nossa equipe especializada está trabalhando na análise e retornará em breve.",
            "Recebemos seu relato sobre a dificuldade encontrada. Nossos técnicos estão investigando a questão e fornecerão uma atualização em até 4 horas.",
            "Agradecemos seu contato sobre esta demanda. Nossa equipe está analisando os detalhes e retornará com orientações específicas.",
            "Obrigado por reportar esta questão. Nossa equipe está verificando as informações e retornará com um plano de ação.",
            "Confirmamos o recebimento de sua requisição. Nossa equipe está avaliando a melhor forma de atendê-lo e retornará em breve.",
            "Agradecemos a comunicação sobre este assunto. Nossa equipe está analisando o caso e retornará com uma proposta de solução."
        ]
        
        self.respostas_improdutivo = [
            "Agradecemos sua mensagem e os cumprimentos! Ficamos contentes com o contato e permanecemos à disposição.",
            "Muito obrigado pelo reconhecimento! Ficamos felizes em saber que nosso trabalho está fazendo a diferença.",
            "Agradecemos profundamente os votos de felicidades! Desejamos a você e sua equipe todo sucesso!",
            "Obrigado pela mensagem de apreço! É um prazer poder contribuir com seu sucesso.",
            "Agradecemos os cumprimentos! Estamos sempre disponíveis para novos desafios e colaborações.",
            "Muito obrigado pelo feedback positivo! Sua motivação nos inspira a continuar melhorando.",
            "Agradecemos sua mensagem cordial! Ficamos honrados com o contato e seguimos à disposição.",
            "Obrigado pelas gentis palavras! É gratificante saber que nosso trabalho é valorizado.",
            "Agradecemos a mensagem de cortesia! Estamos sempre empenhados em oferecer o melhor serviço.",
            "Muito obrigado pelo carinho! Continuamos trabalhando para merecer sua confiança."
        ]
        
        self.respostas_contextuais = {
            "Produtivo": {
                "tecnico": [
                    "🔧 **Resposta Técnica**\n\nIdentificamos uma questão técnica em sua mensagem. Nossa equipe de suporte já foi acionada e entrará em contato em até 2 horas úteis para diagnóstico e resolução.",
                    "⚙️ **Suporte Técnico**\n\nDetectamos um problema técnico em sua solicitação. Nossos engenheiros estão analisando o caso e retornarão com uma solução em até 4 horas."
                ],
                "financeiro": [
                    "💰 **Resposta Financeira**\n\nAnalisamos sua solicitação financeira. Nossa equipe especializada revisará o caso e retornará com informações detalhadas em até 24 horas úteis.",
                    "💳 **Atendimento Financeiro**\n\nRecebemos sua questão sobre aspectos financeiros. Nossa equipe contábil está verificando as informações e entrará em contato em até 48 horas."
                ],
                "comercial": [
                    "📋 **Resposta Comercial**\n\nAgradecemos seu contato sobre aspectos comerciais. Nossa equipe revisará sua solicitação e retornará com as informações solicitadas em breve.",
                    "🤝 **Atendimento Comercial**\n\nRecebemos sua mensagem comercial. Nossa equipe de negócios analisará sua demanda e retornará com uma proposta adequada."
                ]
            },
            "Improdutivo": {
                "festividades": [
                    "🎄 **Resposta de Festividades**\n\nAgradecemos profundamente os votos de felicidades! Desejamos a você, sua equipe e familiares um excelente final de ano repleto de alegria!",
                    "⭐ **Cumprimentos Festivos**\n\nMuito obrigado pelas felicitações! Retribuímos os votos de um próspero ano novo cheio de conquistas!"
                ],
                "reconhecimento": [
                    "🏆 **Resposta de Reconhecimento**\n\nMuito obrigado pelo generoso reconhecimento! Ficamos verdadeiramente felizes em saber que nosso trabalho está fazendo a diferença.",
                    "👍 **Agradecimento por Feedback**\n\nAgradecemos seu feedback positivo! Sua motivação nos inspira a continuar melhorando constantemente."
                ],
                "cortesia": [
                    "💌 **Resposta de Cortesia**\n\nAgradecemos sua mensagem! Ficamos contentes com o contato e permanecemos à disposição para qualquer assunto profissional.",
                    "🙏 **Resposta de Agradecimento**\n\nObrigado pela mensagem de apreço! Estamos sempre disponíveis para auxiliar em assuntos profissionais futuros."
                ]
            }
        }
        print("💬 Gerador de Respostas inicializado")
    
    def gerar_resposta(self, texto, categoria):
        """
        Gera resposta baseada na categoria e contexto
        """
        texto_lower = texto.lower()
        
        # Resposta contextual baseada no conteúdo
        if categoria == "Produtivo":
            if any(palavra in texto_lower for palavra in ['erro', 'bug', 'problema', 'não funciona']):
                return random.choice(self.respostas_contextuais["Produtivo"]["tecnico"])
            elif any(palavra in texto_lower for palavra in ['pagamento', 'fatura', 'cobrança', 'financeiro']):
                return random.choice(self.respostas_contextuais["Produtivo"]["financeiro"])
            elif any(palavra in texto_lower for palavra in ['contrato', 'projeto', 'proposta', 'comercial']):
                return random.choice(self.respostas_contextuais["Produtivo"]["comercial"])
            else:
                return random.choice(self.respostas_produtivo)
        else:
            if any(palavra in texto_lower for palavra in ['natal', 'ano novo', 'boas festas']):
                return random.choice(self.respostas_contextuais["Improdutivo"]["festividades"])
            elif any(palavra in texto_lower for palavra in ['parabéns', 'excelente', 'ótimo trabalho']):
                return random.choice(self.respostas_contextuais["Improdutivo"]["reconhecimento"])
            else:
                return random.choice(self.respostas_improdutivo)

class SistemaEmail:
    def __init__(self):
        self.processador = ProcessadorTexto()
        self.classificador = ClassificadorNaiveBayes()
        self.gerador = GeradorRespostas()
        print("🚀 SISTEMA DE EMAIL INICIALIZADO")
        print("=" * 60)
    
    def processar_entrada(self, arquivo=None, texto=None):
        """
        Processa entrada (PDF ou texto)
        """
        if arquivo:
            # Processa arquivo PDF
            texto_original = self.processador.extrair_texto_pdf(arquivo)
            if not texto_original:
                return {"error": "Não foi possível extrair texto do PDF"}
        elif texto:
            texto_original = texto
        else:
            return {"error": "Nenhuma entrada fornecida"}
        
        print(f"📨 TEXTO ORIGINAL: {texto_original[:100]}...")
        
        # Pré-processamento NLP
        texto_processado = self.processador.preprocessar_texto(texto_original)
        
        # Classificação com Naive Bayes
        categoria = self.classificador.classificar(texto_processado)
        print(f"🏷️ CATEGORIA: {categoria}")
        
        # Geração de resposta
        resposta = self.gerador.gerar_resposta(texto_original, categoria)
        print(f"💡 RESPOSTA: {resposta}")
        
        return {
            'categoria': categoria,
            'resposta_sugerida': resposta,
            'texto_processado': texto_processado,
            'tamanho_original': len(texto_original),
            'status': 'success'
        }

# 🧪 TESTE COMPLETO
def testar_sistema():
    print("🧪 TESTE DO SISTEMA")
    print("=" * 60)
    
    sistema = SistemaEmail()
    
    # Testes com texto
    testes_texto = [
        "Preciso de ajuda urgente com um erro crítico no sistema de pagamento que está impedindo o processamento de faturas.",
        "Parabéns pelo excelente trabalho no projeto! Desejo um feliz natal para toda a equipe!",
        "Como faço para solicitar um relatório detalhado de vendas do último trimestre?",
        "Obrigado pelo suporte rápido na resolução do problema técnico da semana passada."
    ]
    
    for i, texto in enumerate(testes_texto, 1):
        print(f"\n📊 TESTE {i}/4 - TEXTO")
        print("-" * 40)
        
        resultado = sistema.processar_entrada(texto=texto)
        print(f"✅ {resultado['categoria']}: {resultado['resposta_sugerida'][:80]}...")
        print("🎯" + "="*50 + "🎯")

if __name__ == "__main__":
    testar_sistema()