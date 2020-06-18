

class Signal:
    def __init__(self, name):
        self._handlers = []
        self.name = name

    def send(self, **kwargs):
        for handler in self._handlers:
            handler(**kwargs)

    def register_handler(self, handler):
        self._handlers.append(handler)
    
    def unregister_handler(self, handler):
        self._handlers.remove(handler)
    
    def __str__(self):
        return '<Signal name=%s handlers=%d>' % (self.name, len(self._handlers))
    
    def __repr__(self):
        return str(self)


job_created = Signal(name='job_created')
job_scheduled = Signal(name='job_scheduled')
job_running = Signal(name='job_running')
job_completed = Signal(name='job_completed')
job_canceled = Signal(name='job_canceled')
job_error = Signal(name='job_error')

before_job_starts = Signal(name='before_job_starts')
after_job_finishes = Signal(name='after_job_finishes')

cleanup = Signal(name='cleanup')
clear_job_queue = Signal(name='clear_job_queue')
keyboard_interrupt = Signal(name='keyboard_interrupt')

def register_handler(signal): 
    def wrapper(func):
        signal.register_handler(func)
        return func 
    return wrapper 