import re
from collections import Counter

def extrair_dados_academicos(texto_total):
    """
    Extrai todos os dados acadêmicos do texto usando regex patterns otimizados
    Funciona com ambos os formatos de histórico escolar
    
    Nota: Ignora automaticamente disciplinas com menções II, MI e SR:
    - II: Incomparável por Infrequência
    - MI: Média Insuficiente  
    - SR: Sem Rendimento
    """
    print("\n=== INICIANDO EXTRAÇÃO COM REGEX OTIMIZADO ===")
    
    # Debug: mostrar alguns trechos do texto para identificar o formato
    print("[DEBUG] Primeiras 500 chars do texto:")
    print(repr(texto_total[:500]))
    print("[DEBUG] Procurando por padrões de disciplinas...")
    
    # Extrair informações básicas
    curso = extrair_curso(texto_total)
    matriz_curricular = extrair_matriz_curricular(texto_total)
    
    # Extrair IRA e MP (aceita vírgula ou ponto como separador decimal)
    ira_match = padrao_ira.search(texto_total)
    ira = None
    if ira_match:
        ira_str = ira_match.group(1).replace(',', '.')
        ira = float(ira_str)
    print(f"[IRA] Extraído: {ira}")
    
    mp_match = padrao_mp.search(texto_total)
    mp = None
    if mp_match:
        mp_str = mp_match.group(1).replace(',', '.')
        mp = float(mp_str)
    print(f"[MP] Extraído: {mp}")
    
    disciplinas = []
    
    # Adicionar IRA como item se encontrado
    if ira:
        disciplinas.append({"IRA": "IRA", "valor": ira})
    
    # Extrair disciplinas regulares (processamento de duas linhas)
    linhas = texto_total.splitlines()
    disciplinas_encontradas = 0
    disciplinas_ignoradas = 0
    
    print("[DISCIPLINAS] Processando formato original...")
    for i, linha in enumerate(linhas):
        # Buscar linha 1 (disciplina) - formato original
        match_linha1 = padrao_disciplina_linha1.search(linha)
        if match_linha1 and i + 1 < len(linhas):
            # Buscar linha 2 (professor e dados) na próxima linha
            linha_seguinte = linhas[i + 1]
            match_linha2 = padrao_disciplina_linha2.search(linha_seguinte)
            
            if match_linha2:
                # Extrair dados da linha 1
                ano_periodo, prefixo, codigo, nome = match_linha1.groups()
                
                # Extrair dados da linha 2
                professor, carga_h, turma, freq, nota, mencao, situacao = match_linha2.groups()
                
                # Ignorar matérias com menções II, MI e SR
                if mencao.upper() in ['II', 'MI', 'SR']:
                    print(f"  -> Ignorando disciplina com menção {mencao}: {codigo} - {nome.strip()[:30]}...")
                    disciplinas_ignoradas += 1
                    continue
                
                disciplina_data = {
                    "tipo_dado": "Disciplina Regular",
                    "nome": limpar_nome_disciplina(nome.strip()),
                    "status": situacao,
                    "mencao": mencao if mencao != '-' else '-',
                    "creditos": int(int(carga_h) / 15) if carga_h.isdigit() else 0,
                    "codigo": codigo,
                    "carga_horaria": int(carga_h) if carga_h.isdigit() else 0,
                    "ano_periodo": ano_periodo,
                    "prefixo": prefixo,
                    "professor": limpar_nome_professor(professor.strip()),
                    "turma": turma,
                    "frequencia": freq if freq != '--' else None,
                    "nota": nota if nota != '--' else None
                }
                disciplinas.append(disciplina_data)
                disciplinas_encontradas += 1
                print(f"  -> Disciplina (formato original): {codigo} - {nome.strip()[:30]}... (Status: {situacao})")
    
    # Se não encontrou disciplinas no formato original, tenta o formato alternativo
    if disciplinas_encontradas == 0:
        print("[DISCIPLINAS] Tentando formato alternativo...")
        
        # Debug: procurar por padrões que indicam o formato alternativo
        sample_lines = []
        for i, linha in enumerate(linhas[:20]):  # Primeiras 20 linhas para debug
            if re.search(r'\d{4}\.\d[A-ZÀ-Ÿ]', linha):
                sample_lines.append((i, linha))
        
        print(f"[DEBUG] Encontradas {len(sample_lines)} linhas com padrão alternativo nas primeiras 20:")
        for line_num, line_content in sample_lines[:3]:  # Mostrar apenas as primeiras 3
            print(f"  Linha {line_num}: {repr(line_content[:80])}")
        
        for i, linha in enumerate(linhas):
            # Buscar linha 1 (ano/período + nome da disciplina) - formato alternativo
            match_alt_linha1 = padrao_disciplina_alt_linha1.search(linha)
            if match_alt_linha1 and i + 1 < len(linhas):
                linha_seguinte = linhas[i + 1]
                
                print(f"[DEBUG] Linha {i}: {repr(linha[:80])}")
                print(f"[DEBUG] Linha {i+1}: {repr(linha_seguinte[:80])}")
                
                # Buscar linha 2 (professor, dados) na próxima linha
                match_alt_linha2 = padrao_disciplina_alt_linha2.search(linha_seguinte)
                
                if match_alt_linha2:
                    # Extrair dados da linha 1
                    ano_periodo, nome = match_alt_linha1.groups()
                    
                    # Extrair dados da linha 2
                    professor, carga_h, turma, situacao, codigo, carga_h2, freq, mencao = match_alt_linha2.groups()
                    
                    print(f"[DEBUG] Match encontrado: {codigo} - {nome[:30]}")
                    
                    # Ignorar matérias com menções II, MI e SR
                    if mencao.upper() in ['II', 'MI', 'SR']:
                        print(f"  -> Ignorando disciplina com menção {mencao}: {codigo} - {nome.strip()[:30]}...")
                        disciplinas_ignoradas += 1
                        continue
                    
                    disciplina_data = {
                        "tipo_dado": "Disciplina Regular",
                        "nome": limpar_nome_disciplina(nome.strip()),
                        "status": situacao,
                        "mencao": mencao if mencao != '-' else '-',
                        "creditos": int(int(carga_h) / 15) if carga_h.isdigit() else 0,
                        "codigo": codigo,
                        "carga_horaria": int(carga_h) if carga_h.isdigit() else 0,
                        "ano_periodo": ano_periodo,
                        "prefixo": "",
                        "professor": limpar_nome_professor(professor.strip()),
                        "turma": turma,
                        "frequencia": freq if freq != '--' else None,
                        "nota": None  # Nota não está disponível neste formato, usar mencao
                    }
                    disciplinas.append(disciplina_data)
                    disciplinas_encontradas += 1
                    print(f"  -> Disciplina (formato alternativo): {codigo} - {nome.strip()[:30]}... (Status: {situacao})")
                else:
                    print(f"[DEBUG] Linha 2 não fez match: {repr(linha_seguinte[:80])}")
    
    print(f"[DISCIPLINAS] Encontradas {disciplinas_encontradas} disciplinas regulares")
    if disciplinas_ignoradas > 0:
        print(f"[DISCIPLINAS] Ignoradas {disciplinas_ignoradas} disciplinas com menções II, MI ou SR")
    
    # Extrair disciplinas CUMP
    disciplinas_cump = padrao_disciplina_cump.findall(texto_total)
    print(f"[CUMP] Encontradas {len(disciplinas_cump)} disciplinas CUMP")
    
    for disc in disciplinas_cump:
        ano_periodo, prefixo, codigo, nome, carga_h = disc
        
        disciplina_data = {
            "tipo_dado": "Disciplina CUMP",
            "nome": limpar_nome_disciplina(nome.strip()),
            "status": 'CUMP',
            "mencao": '-',
            "creditos": int(int(carga_h) / 15) if carga_h.isdigit() else 0,
            "codigo": codigo,
            "carga_horaria": int(carga_h) if carga_h.isdigit() else 0,
            "ano_periodo": ano_periodo,
            "prefixo": prefixo
        }
        disciplinas.append(disciplina_data)
        print(f"  -> CUMP: {codigo} - {nome.strip()[:30]}...")
    
    # Extrair disciplinas pendentes (formato novo)
    disciplinas_pendentes = padrao_pendentes_novo.findall(texto_total)
    print(f"[PENDENTES] Encontradas {len(disciplinas_pendentes)} disciplinas pendentes (formato novo)")
    
    for pend in disciplinas_pendentes:
        nome, carga_h, codigo = pend[:3]
        status_matricula = pend[3] if len(pend) > 3 else None
        
        status = 'MATR' if status_matricula else 'PENDENTE'
        
        disciplina_data = {
            "tipo_dado": "Disciplina Pendente",
            "nome": limpar_nome_disciplina(nome.strip()),
            "status": status,
            "mencao": '-',
            "creditos": int(int(carga_h) / 15) if carga_h.isdigit() else 0,
            "codigo": codigo,
            "carga_horaria": int(carga_h) if carga_h.isdigit() else 0,
            "ano_periodo": "",
            "prefixo": "",
            "observacao": status_matricula
        }
        disciplinas.append(disciplina_data)
        print(f"  -> Pendente: {codigo} - {nome.strip()[:30]}... (Status: {status})")
    
    # Extrair equivalências
    equivalencias = []
    equivalencias_match = padrao_equivalencias.findall(texto_total)
    print(f"[EQUIVALENCIAS] Encontradas {len(equivalencias_match)} equivalências")
    
    for eq in equivalencias_match:
        codigo_cumpriu, nome_cumpriu, ch_cumpriu, codigo_equivalente, nome_equivalente, ch_equivalente = eq
        equivalencias.append({
            "cumpriu": codigo_cumpriu,
            "nome_cumpriu": nome_cumpriu.strip(),
            "atraves_de": codigo_equivalente, 
            "nome_equivalente": nome_equivalente.strip(),
            "ch_cumpriu": ch_cumpriu,
            "ch_equivalente": ch_equivalente
        })
        print(f"  -> Equivalência: {codigo_cumpriu} ← {codigo_equivalente}")
    
    # Extrair pendências (apenas contar ocorrências)
    pendencias = padrao_pendencias.findall(texto_total)
    if pendencias:
        # Contar ocorrências de cada status
        from collections import Counter
        contagem_pendencias = Counter(pendencias)
        disciplinas.append({"tipo_dado": "Pendencias", "valores": dict(contagem_pendencias)})
        print(f"[PENDENCIAS] Encontradas: {dict(contagem_pendencias)}")
    
    # Extrair o semestre atual
    semestre_atual = extrair_semestre_atual(disciplinas)
    print(f"[SEMESTRE] Semestre atual extraído: {semestre_atual}")
    
    # Calcular o número do semestre baseado em semestres cursados
    numero_semestre = calcular_numero_semestre(disciplinas)
    print(f"[SEMESTRE] Número do semestre calculado: {numero_semestre}º semestre")
    
    print(f"=== EXTRAÇÃO CONCLUÍDA: {len(disciplinas)} itens extraídos ===\n")
    
    return {
        'disciplinas': disciplinas,
        'equivalencias': equivalencias,
        'curso': curso,
        'matriz_curricular': matriz_curricular,
        'media_ponderada': mp,
        'ira': ira,
        'semestre_atual': semestre_atual,
        'numero_semestre': numero_semestre
    }