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
    
    dados_academicos = {
        'disciplinas': [],
        'periodos': [],
        'media_geral': None,
        'situacao_final': None
    }
    
    # Padrão para extrair períodos (ex: "1º Período", "2º Período", etc)
    pattern_periodos = r'(\d+)º\s+(?:Período|PERÍODO)'
    periodos = re.findall(pattern_periodos, texto_total)
    dados_academicos['periodos'] = sorted(list(set(periodos)), key=lambda x: int(x))
    
    # Padrão para extrair disciplinas com suas informações
    # Formato: Nome da disciplina, código, carga horária, frequência, menção/nota
    pattern_disciplina = r'([A-ZÁÉÍÓÚ][A-Za-záéíóúñ\s\-/]+?)\s+(\d+)\s+(\d+)\s+(\d+(?:[.,]\d+)?)\s+([A-Z]{2}|[0-9]{1,2}(?:[.,][0-9]+)?)'
    
    matches = re.finditer(pattern_disciplina, texto_total)
    
    for match in matches:
        nome_disciplina = match.group(1).strip()
        codigo = match.group(2).strip()
        carga_horaria = match.group(3).strip()
        frequencia = match.group(4).strip().replace(',', '.')
        mencao = match.group(5).strip()
        
        # Ignorar disciplinas com menções II, MI e SR
        if mencao in ['II', 'MI', 'SR']:
            continue
        
        # Converter menção para nota se for numérica
        try:
            nota = float(mencao.replace(',', '.'))
        except ValueError:
            nota = mencao
        
        disciplina = {
            'nome': nome_disciplina,
            'codigo': codigo,
            'carga_horaria': int(carga_horaria),
            'frequencia': float(frequencia),
            'mencao': mencao,
            'nota': nota
        }
        
        dados_academicos['disciplinas'].append(disciplina)
    
    # Extrair média geral (padrões comuns)
    pattern_media = r'(?:Média|MÉDIA)\s*(?:Geral|GERAL)?[:\s]+([0-9]{1,2}(?:[.,][0-9]+)?)'
    match_media = re.search(pattern_media, texto_total, re.IGNORECASE)
    if match_media:
        dados_academicos['media_geral'] = float(match_media.group(1).replace(',', '.'))
    
    # Extrair situação final
    pattern_situacao = r'(?:Situação|SITUAÇÃO)\s*(?:Final|FINAL)?[:\s]+([A-Za-záéíóú\s]+?)(?:\n|$)'
    match_situacao = re.search(pattern_situacao, texto_total, re.IGNORECASE)
    if match_situacao:
        dados_academicos['situacao_final'] = match_situacao.group(1).strip()
    
    return dados_academicos