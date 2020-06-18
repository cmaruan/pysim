import os
import time
import pickle
import hashlib
import subprocess
import multiprocessing as mp
from copy import copy, deepcopy
from queue import Empty as QueueEmpty
from itertools import count

from pysim.core.conf import settings
from pysim.core import signals


class Job:
    CREATED = 'CREATED'
    SCHEDULED = 'SCHEDULED'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    ERROR = 'ERROR'
    _VALID_STATES = [
        CREATED, SCHEDULED,
        RUNNING, COMPLETED,
        CANCELED, ERROR,
    ]
    _dispacher = {
        CREATED: signals.job_created,
        SCHEDULED: signals.job_scheduled,
        RUNNING: signals.job_running,
        COMPLETED: signals.job_completed,
        CANCELED: signals.job_canceled,
        ERROR: signals.job_error,
    }

    def __init__(self, id, executable, cli_args, meta, app_options):
        self.id = id
        self.executable = executable
        self.cli_args = cli_args
        self.app_options = app_options
        self.meta = meta
        self.state = None
        pickled_job = pickle.dumps([executable, cli_args])
        self.hash = hashlib.sha256(pickled_job).hexdigest()

        for stream in ['STDIN', 'STDOUT', 'STDERR']:
            setattr(self, stream, meta[stream])
        self.set_state(Job.CREATED)

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __str__(self):
        return '<Job id=%d status=%s>' % (self.id, self.state)

    def __repr__(self):
        return str(self)

    def parse(self):
        line = f'{self.executable}'
        if self.STDIN:
            line += f' <{self.STDIN}'
        if self.STDOUT:
            line += f' >{self.STDOUT}'
        if self.STDERR:
            line += f' 2>{self.STDERR}'
        if self.cli_args:
            line += ' ' + ' '.join(f'{k} {v}' for k, v in self.cli_args)
        return line

    def set_state(self, new_state, send_signal=True):
        if new_state not in Job._VALID_STATES:
            raise ValueError("Invalid state %s" % (new_state))
        old_state = self.state
        self.state = new_state
        if send_signal:
            Job._dispacher[new_state].send(job=self, old_state=old_state)

    def run(self):
        if self.state != Job.SCHEDULED:
            return

        self.set_state(Job.RUNNING)

        if self.app_options['fake']:
            time.sleep(0.5)
        else:
            args = map(str, sum(self.cli_args, ()))
            open_streams = {}
            for stream, mode in [('STDIN', 'r'), ('STDOUT', 'w'), ('STDERR', 'w')]:
                file_stream = getattr(self, stream, None)
                if file_stream:
                    os.makedirs(os.path.dirname(file_stream), exist_ok=True)
                    open_streams[stream.lower()] = open(file_stream, mode)

            subprocess.run([self.executable, *args], **open_streams)

            for stream in open_streams.values():
                stream.close()

        self.set_state(Job.COMPLETED)


class Application:
    def __init__(self, app_options):
        self.job_queue = mp.Queue()
        self.job_list = []

        id_generator = count()
        for args in settings.args:
            parsed_values, args = settings.parse_variables(args)
            job = Job(next(id_generator),
                      getattr(settings, 'EXECUTABLE'),
                      list(args.items()),
                      parsed_values,
                      vars(app_options))
            job.set_state(job.SCHEDULED)
            self.job_list.append(job)

        self._loaded_plugins = []
        for plugin_class in settings.enabled_plugins:
            plugin = plugin_class(job_list=self.job_list)
            self._loaded_plugins.append(plugin)
        
        signals.clear_job_queue.register_handler(self.cancell_all_jobs)

    def run(self):
        for job in self.job_list:
            self.job_queue.put(job)

        total_workers = getattr(settings, 'PARALLEL_INSTANCES')
        workforce = []

        for w in range(total_workers):
            worker = mp.Process(target=self._worker, args=(w,))
            workforce.append(worker)
            worker.start()

        for worker in workforce:
            worker.join()

        signals.cleanup.send()

    def cancell_all_jobs(self):
        while True:
            try:
                job = self.job_queue.get_nowait()
                job.set_state(job.CANCELED)
            except QueueEmpty:
                return

    def _worker(self, id):
        while True:
            try:
                job = self.job_queue.get_nowait()
            except QueueEmpty:
                return

            context = {'job': copy(job)}

            signals.before_job_starts.send(context=context)
            job.run()
            signals.after_job_finishes.send(context=context)
