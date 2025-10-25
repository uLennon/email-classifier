from flask import Flask, request, jsonify
from flask_cors import CORS
from sistema_completo import SistemaEmail
import os

app = Flask(__name__)
CORS(app)

# Inicializa o sistema 
sistema = SistemaEmail()

@app.route('/')
def home():
    return jsonify({
        "message": "Sistema de Classificação de Emails",
        "status": "online",
        "caracteristicas": [
            "Processamento NLP completo",
            "Classificação Naive Bayes", 
            "Suporte a PDF e texto",
            "Respostas contextuais"
        ]
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_email():
    try:
        # Verifica se é upload de arquivo ou texto
        if 'file' in request.files:
            arquivo = request.files['file']
            if arquivo.filename != '':
                if arquivo.filename.lower().endswith('.pdf'):
                    resultado = sistema.processar_entrada(arquivo=arquivo)
                else:
                    return jsonify({'error': 'Apenas arquivos PDF são suportados', 'status': 'error'}), 400
            else:
                return jsonify({'error': 'Nenhum arquivo selecionado', 'status': 'error'}), 400
        else:
            data = request.get_json()
            texto = data.get('text', '').strip()
            if not texto:
                return jsonify({'error': 'Texto do email é obrigatório', 'status': 'error'}), 400
            resultado = sistema.processar_entrada(texto=texto)
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({
            'error': f'Erro interno: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'email-classifier',
        'mode': '100%',
        'nlp_processing': 'active',
        'naive_bayes': 'active'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)