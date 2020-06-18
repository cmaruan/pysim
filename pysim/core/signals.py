

class Signal:
    def __init__(self):
        self._handlers = []

    def send(self, *args, **kwargs):
        for handler in self._handlers:
            handler(*args, **kwargs)

    def register_handler(self, handler):
        self._handlers.append(handler)
    
    def unregister_handler(self, handler):
        self._handlers.remove(handler)


job_created = Signal()
job_scheduled = Signal()
job_running = Signal()
job_completed = Signal()
job_canceled = Signal()
job_error = Signal()

before_job_starts = Signal()
after_job_finishes = Signal()

cleanup = Signal()

def register_handler(signal): 
    def wrapper(func):
        signal.register_handler(func)
        return func 
    return wrapper 