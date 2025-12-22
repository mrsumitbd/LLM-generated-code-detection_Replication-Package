def _add_terminate(r: Resource):
    def terminate():
        r.terminate()
    
    r.terminate = terminate