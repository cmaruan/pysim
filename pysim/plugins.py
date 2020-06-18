import os
import time
import json
import pickle
from pprint import pprint
from multiprocessing import Manager
from pysim.core.signals import before_job_starts, after_job_finishes
from pysim.core.signals import job_completed, cleanup
from pysim.utils import get_config_folder

class LogEvents:
    def __init__(self, **kwargs):
        # before_job_starts.register_handler(self.before)
        job_completed.register_handler(self.after)
    
    def before(self,  job, old_state):
        print(job)

    def after(self,  job, old_state):
        print(job)


class SaveIntermediaryState:
    def __init__(self, job_list, **kwargs):
        from uuid import uuid4
        self.manager = Manager()
        self.current_state = self.manager.dict()

        self.root = get_config_folder()
        os.makedirs(self.root, exist_ok=True)

        if os.path.exists(os.path.join(self.root, '.unsaved-state')):
            with open(os.path.join(self.root, '.unsaved-state'), 'rb') as old_state:
                state = pickle.load(old_state)
                self.current_state.update(**state)


        if 'uuid' in self.current_state:
            self.uuid = self.current_state['uuid']
        else:
            self.uuid = uuid4()

        for job in job_list:
            if job.hash in self.current_state:
                job.set_state(job.COMPLETED, send_signal=False)

        after_job_finishes.register_handler(self.after)
        cleanup.register_handler(self.cleanup)

    def after(self, context):
        job = context['job']
        self.current_state[job.hash] = job
        with open(os.path.join(self.root, '.unsaved-state'), 'wb') as state:
            pickle.dump(dict(self.current_state), state)
    
    def cleanup(self):
        os.remove(os.path.join(self.root, '.unsaved-state'))