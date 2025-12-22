def update_list():
                cfg[title][key] = [
                    float(e.text()) if isinstance(v, float) else int(e.text())
                    for e, v in zip(edits, value) if e.text() != ''
                ]