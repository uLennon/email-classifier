// Configuração - ATUALIZE COM SUA URL DO BACKEND
const BACKEND_URL = 'http://localhost:5000'; // Local development
// const BACKEND_URL = 'https://seu-backend.onrender.com'; // Production

// Elementos DOM
const elements = {
    dropZone: document.getElementById('dropZone'),
    fileInput: document.getElementById('fileInput'),
    browseBtn: document.getElementById('browseBtn'),
    emailText: document.getElementById('emailText'),
    analyzeBtn: document.getElementById('analyzeBtn'),
    loadingSpinner: document.getElementById('loadingSpinner'),
    resultsCard: document.getElementById('resultsCard'),
    classificationBadge: document.getElementById('classificationBadge'),
    badgeLabel: document.getElementById('badgeLabel'),
    badgeDesc: document.getElementById('badgeDesc'),
    responseText: document.getElementById('responseText'),
    copyBtn: document.getElementById('copyBtn'),
    newAnalysisBtn: document.getElementById('newAnalysisBtn'),
    errorAlert: document.getElementById('errorAlert'),
    errorText: document.getElementById('errorText')
};

// Estado da aplicação
let currentFile = null;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadHistory();
});

// Configura todos os event listeners
function initializeEventListeners() {
    // Drag & Drop
    elements.dropZone.addEventListener('dragover', handleDragOver);
    elements.dropZone.addEventListener('dragleave', handleDragLeave);
    elements.dropZone.addEventListener('drop', handleDrop);
    
    // Browse button
    elements.browseBtn.addEventListener('click', () => elements.fileInput.click());
    elements.fileInput.addEventListener('change', handleFileSelect);
    
    // Text area input
    elements.emailText.addEventListener('input', handleTextInput);
    
    // Analyze button
    elements.analyzeBtn.addEventListener('click', analyzeEmail);
    
    // Copy button
    elements.copyBtn.addEventListener('click', copyResponse);
    
    // New analysis button
    elements.newAnalysisBtn.addEventListener('click', resetAnalysis);
}

// Drag & Drop handlers
function handleDragOver(e) {
    e.preventDefault();
    elements.dropZone.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    elements.dropZone.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    elements.dropZone.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// Processa arquivo selecionado
function handleFile(file) {
    if (!isValidFileType(file)) {
        showError('Por favor, selecione apenas arquivos .txt ou .pdf');
        return;
    }
    
    currentFile = file;
    
    // Limpa textarea
    elements.emailText.value = '';
    
    // Mostra info do arquivo
    showFileInfo(file);
    
    // Lê conteúdo do arquivo
    readFileContent(file);
}

// Lê conteúdo do arquivo
function readFileContent(file) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        elements.emailText.value = e.target.result;
        updateAnalyzeButton();
    };
    
    reader.onerror = function() {
        showError('Erro ao ler o arquivo');
    };
    
    if (file.type === 'text/plain') {
        reader.readAsText(file);
    } else if (file.type === 'application/pdf') {
        // Para PDF, mostramos mensagem (em produção, integraria com PDF.js)
        elements.emailText.value = `[Arquivo PDF: ${file.name}]\n\nPara melhor análise, extraia o texto do PDF e cole acima.`;
        updateAnalyzeButton();
    }
}

// Valida tipo de arquivo
function isValidFileType(file) {
    const allowedTypes = ['text/plain', 'application/pdf'];
    return allowedTypes.includes(file.type);
}

// Mostra informações do arquivo
function showFileInfo(file) {
    const fileInfo = document.createElement('div');
    fileInfo.className = 'file-info';
    fileInfo.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-file me-2"></i>
            <div>
                <strong>${file.name}</strong>
                <div class="text-muted small">${formatFileSize(file.size)}</div>
            </div>
            <button class="btn btn-sm btn-outline-danger ms-auto" onclick="removeFile()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Remove info anterior se existir
    const existingInfo = elements.dropZone.querySelector('.file-info');
    if (existingInfo) {
        existingInfo.remove();
    }
    
    elements.dropZone.appendChild(fileInfo);
}

// Remove arquivo selecionado
function removeFile() {
    currentFile = null;
    elements.fileInput.value = '';
    elements.emailText.value = '';
    
    const fileInfo = elements.dropZone.querySelector('.file-info');
    if (fileInfo) {
        fileInfo.remove();
    }
    
    updateAnalyzeButton();
}

// Formata tamanho do arquivo
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Handler de input de texto
function handleTextInput() {
    currentFile = null;
    elements.fileInput.value = '';
    
    const fileInfo = elements.dropZone.querySelector('.file-info');
    if (fileInfo) {
        fileInfo.remove();
    }
    
    updateAnalyzeButton();
}

// Atualiza estado do botão de análise
function updateAnalyzeButton() {
    const hasText = elements.emailText.value.trim().length > 0;
    elements.analyzeBtn.disabled = !hasText;
}

// Função principal de análise
async function analyzeEmail() {
    const emailText = elements.emailText.value.trim();
    
    if (!emailText) {
        showError('Por favor, insira algum texto para análise');
        return;
    }
    
    // Mostra loading
    setLoadingState(true);
    hideError();
    hideResults();
    
    try {
        const response = await fetch(`${BACKEND_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: emailText
            })
        });
        
        if (!response.ok) {
            throw new Error(`Erro ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showResults(data);
            saveToHistory(emailText, data);
        } else {
            throw new Error(data.error || 'Erro desconhecido');
        }
        
    } catch (error) {
        console.error('Erro na análise:', error);
        showError(`Falha na análise: ${error.message}`);
    } finally {
        setLoadingState(false);
    }
}

// Mostra resultados da análise
function showResults(data) {
    // Atualiza badge de classificação
    elements.classificationBadge.className = `classification-badge ${data.categoria.toLowerCase()}`;
    elements.badgeLabel.textContent = data.categoria.toUpperCase();
    elements.badgeDesc.textContent = data.categoria === 'Produtivo' 
        ? 'Requer ação ou resposta' 
        : 'Não requer ação imediata';
    
    // Atualiza resposta sugerida
    elements.responseText.textContent = data.resposta_sugerida;
    
    // Mostra card de resultados
    elements.resultsCard.classList.remove('d-none');
    
    // Scroll para resultados
    elements.resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Esconde resultados
function hideResults() {
    elements.resultsCard.classList.add('d-none');
}

// Copia resposta para clipboard
async function copyResponse() {
    try {
        await navigator.clipboard.writeText(elements.responseText.textContent);
        
        // Feedback visual
        const originalText = elements.copyBtn.innerHTML;
        elements.copyBtn.innerHTML = '<i class="fas fa-check me-2"></i>Copiado!';
        elements.copyBtn.classList.remove('btn-outline-success');
        elements.copyBtn.classList.add('btn-success');
        
        setTimeout(() => {
            elements.copyBtn.innerHTML = originalText;
            elements.copyBtn.classList.remove('btn-success');
            elements.copyBtn.classList.add('btn-outline-success');
        }, 2000);
        
    } catch (err) {
        showError('Erro ao copiar texto');
    }
}

// Reseta análise
function resetAnalysis() {
    elements.emailText.value = '';
    elements.fileInput.value = '';
    currentFile = null;
    
    const fileInfo = elements.dropZone.querySelector('.file-info');
    if (fileInfo) {
        fileInfo.remove();
    }
    
    hideResults();
    hideError();
    updateAnalyzeButton();
    
    // Scroll para topo
    elements.dropZone.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Controla estado de loading
function setLoadingState(loading) {
    if (loading) {
        elements.analyzeBtn.disabled = true;
        elements.loadingSpinner.classList.remove('d-none');
        elements.analyzeBtn.querySelector('.btn-text').textContent = 'Analisando...';
    } else {
        elements.analyzeBtn.disabled = false;
        elements.loadingSpinner.classList.add('d-none');
        elements.analyzeBtn.querySelector('.btn-text').textContent = 'Analisar Email';
    }
}

// Mostra erro
function showError(message) {
    elements.errorText.textContent = message;
    elements.errorAlert.classList.remove('d-none');
}

// Esconde erro
function hideError() {
    elements.errorAlert.classList.add('d-none');
}

// Histórico local (localStorage)
function saveToHistory(emailText, result) {
    try {
        const history = getHistory();
        const historyItem = {
            text: emailText.substring(0, 100) + (emailText.length > 100 ? '...' : ''),
            category: result.categoria,
            response: result.resposta_sugerida,
            timestamp: new Date().toISOString()
        };
        
        history.unshift(historyItem);
        
        // Mantém apenas os últimos 10 itens
        if (history.length > 10) {
            history.pop();
        }
        
        localStorage.setItem('emailClassifierHistory', JSON.stringify(history));
    } catch (error) {
        console.error('Erro ao salvar histórico:', error);
    }
}

function getHistory() {
    try {
        return JSON.parse(localStorage.getItem('emailClassifierHistory')) || [];
    } catch {
        return [];
    }
}

function loadHistory() {
    // Poderia ser usado para mostrar histórico na UI
    const history = getHistory();
    console.log('Histórico carregado:', history);
}

// Teste rápido da conexão
async function testConnection() {
    try {
        const response = await fetch(`${BACKEND_URL}/health`);
        if (response.ok) {
            console.log('✅ Conexão com backend estabelecida');
        } else {
            console.warn('⚠️ Backend pode estar offline');
        }
    } catch (error) {
        console.error('❌ Não foi possível conectar com o backend:', error);
    }
}

// Testa conexão ao carregar a página
testConnection();