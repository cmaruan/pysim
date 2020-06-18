import os
import time
import json
import pickle
import warnings
from pprint import pprint
from multiprocessing import Manager


from pysim.core.signals import before_job_starts, after_job_finishes
from pysim.core.signals import job_completed, cleanup, keyboard_interrupt, clear_job_queue
from pysim.utils import get_config_folder


class LogEvents:
    def __init__(self, **kwargs):
        job_completed.register_handler(self.completed)

    def completed(self, job, old_state, **kwargs):
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

    def after(self, context, **kwargs):
        job = context['job']
        self.current_state[job.hash] = job
        with open(os.path.join(self.root, '.unsaved-state'), 'wb') as state:
            pickle.dump(dict(self.current_state), state)

    def cleanup(self, **kwargs):
        os.remove(os.path.join(self.root, '.unsaved-state'))


class GracefulKeyboardInterrupt:
    def __init__(self, job_list, **kwargs):
        from pysim.core.conf import settings
        if not getattr(settings, 'CAPTURE_SIGINT', False):
            warnings.warn(
                "For %s to work properly, "
                "'CAPTURE_SIGINT' needs to be set."
                % (self.__class__))
            return
        keyboard_interrupt.register_handler(self.handle_sigint)

    def handle_sigint(self, **kwargs):
        print("Clearing job queue...")
        clear_job_queue.send()
