import re

def extrair_dados_academicos(texto_total):
    """
    Extrai todos os dados acadêmicos do texto usando regex patterns otimizados
    Funciona com ambos os formatos de histórico escolar
    
    Nota: Ignora automaticamente disciplinas com menções II, MI e SR:
    - II: Incomparável por Infrequência
    - MI: Média Insuficiente  
    - SR: Sem Rendimento
    """
    # Padrão para extrair disciplinas, notas e créditos
    pattern = r'(\w+)\s+(\d+)\s+(\d+(?:\.\d+)?)\s*(\w+)'
    
    # Padrão para ignorar disciplinas com menções II, MI e SR
    ignore_pattern = r'\b(II|MI|SR)\b'
    
    # Inicializar listas para armazenar os dados
    disciplinas = []
    notas = []
    creditos = []
    
    # Iterar sobre as correspondências do padrão principal
    for match in re.finditer(pattern, texto_total):
        disciplina, credito, nota, menção = match.groups()
        
        # Ignorar disciplinas com menções II, MI e SR
        if re.search(ignore_pattern, menção):
            continue
        
        disciplinas.append(disciplina)
        notas.append(float(nota))
        creditos.append(int(credito))
    
    return disciplinas, notas, creditos