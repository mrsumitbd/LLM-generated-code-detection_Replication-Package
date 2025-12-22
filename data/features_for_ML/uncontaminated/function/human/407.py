from dbcan.annotation.pyhmmer_search import PyHMMERDBCANProcessor

def run_dbCAN_hmmer(config):
    from dbcan.annotation.pyhmmer_search import PyHMMERDBCANProcessor
    processor = PyHMMERDBCANProcessor(config)
    processor.run()