import re
from typing import List, Dict, Any

def extrair_dados_academicos(texto_total: str) -> List[Dict[str, Any]]:
    """
    Extrai todos os dados acadêmicos do texto usando regex patterns otimizados.
    Funciona com ambos os formatos de histórico escolar.

    Nota: Ignora automaticamente disciplinas com menções II, MI e SR:
        - II: Incomparável por Infrequência
        - MI: Média Insuficiente
        - SR: Sem Rendimento
    """
    # Normaliza o texto: substitui vírgula por ponto em notas e remove espaços extras
    texto = re.sub(r'\s+', ' ', texto_total.strip())

    # Padrões para capturar disciplina e nota em diferentes formatos
    patterns = [
        # Ex.: "Matemática 8,5" ou "Matemática 8.5"
        r'(?P<disciplina>[A-Za-zÀ-ÿ0-9\s]+?)\s+(?P<nota>\d{1,2}[.,]\d{1,2})\s*(?P<menção>II|MI|SR)?',
        # Ex.: "Matemática - Nota: 8,5" ou "Matemática - Nota=8.5"
        r'(?P<disciplina>[A-Za-zÀ-ÿ0-9\s]+?)\s*-\s*Nota\s*[:=]\s*(?P<nota>\d{1,2}[.,]\d{1,2})\s*(?P<menção>II|MI|SR)?',
        # Ex.: "Matemática: 8,5" ou "Matemática:8.5"
        r'(?P<disciplina>[A-Za-zÀ-ÿ0-9\s]+?)\s*:\s*(?P<nota>\d{1,2}[.,]\d{1,2})\s*(?P<menção>II|MI|SR)?',
        # Ex.: "Disciplina: Matemática, Nota: 8,5"
        r'Disciplina\s*[:=]\s*(?P<disciplina>[A-Za-zÀ-ÿ0-9\s]+?)\s*,\s*Nota\s*[:=]\s*(?P<nota>\d{1,2}[.,]\d{1,2})\s*(?P<menção>II|MI|SR)?',
    ]

    resultados = []

    for pattern in patterns:
        for match in re.finditer(pattern, texto, flags=re.IGNORECASE):
            disciplina = match.group('disciplina').strip()
            nota_str = match.group('nota').replace(',', '.')
            try:
                nota = float(nota_str)
            except ValueError:
                continue  # ignora se não for número válido

            menção = match.group('menção')
            if menção:  # ignora disciplinas com menções II, MI ou SR
                continue

            # Evita duplicatas: se já existir a disciplina, atualiza apenas se nota for maior
            existente = next((d for d in resultados if d['disciplina'].lower() == disciplina.lower()), None)
            if existente:
                if nota > existente['nota']:
                    existente['nota'] = nota
            else:
                resultados.append({'disciplina': disciplina, 'nota': nota})

    return resultados