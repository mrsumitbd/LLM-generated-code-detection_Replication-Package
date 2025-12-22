
class MockCompletion:
                        def __init__(self):
                            self.choices = [type('obj', (object,), {
                                'message': type('obj', (object,), {
                                    'content': "抱歉，由于API错误无法生成回答。"
                                })()
                            })()]