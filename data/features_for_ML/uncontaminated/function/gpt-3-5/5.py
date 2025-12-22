def extrair_dados_academicos(texto_total):
    import re

    padrao_disciplina = r'(?P<codigo>\d{5})\s+(?P<disciplina>.*?)\s+(?P<mencao>[A-E][+-]?)'
    padrao_semestre = r'Semestre\s+(\d{4}/\d)'
    padrao_ignorar = r'II|MI|SR'

    dados_academicos = []
    semestre_atual = None

    for match_semestre in re.finditer(padrao_semestre, texto_total):
        semestre_atual = match_semestre.group(1)

    for match_disciplina in re.finditer(padrao_disciplina, texto_total):
        if semestre_atual and re.search(padrao_ignorar, match_disciplina.group('mencao')) is None:
            dados_academicos.append({
                'semestre': semestre_atual,
                'codigo': match_disciplina.group('codigo'),
                'disciplina': match_disciplina.group('disciplina'),
                'mencao': match_disciplina.group('mencao')
            })

    return dados_academicos