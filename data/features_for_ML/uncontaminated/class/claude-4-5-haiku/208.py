class AsyncJobResourceWithRawResponse:

    def __init__(self, job: AsyncJobResource) -> None:
        self._job = job

    def __getattr__(self, name: str):
        method = getattr(self._job, name)
        
        if callable(method):
            def wrapper(*args, **kwargs):
                response = method(*args, **kwargs)
                if hasattr(response, '__aiter__'):
                    return response
                return response
            return wrapper
        
        return method