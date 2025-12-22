def wrapper(func):
        if isinstance(signal, (list, tuple)):
            for s in signal:
                s.connect(listener=func, sender=sender)
        else:
            signal.connect(listener=func, sender=sender)
        return func