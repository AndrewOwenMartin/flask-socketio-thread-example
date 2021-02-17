# First party libraries
import collections, datetime, functools, itertools
import json, logging, pathlib, random, re
import dataclasses
import typing
import threading
import queue
import time
import string

# Pip libraries
import flask
import flask_socketio
import socketio
import eventlet

log = logging.getLogger(__name__)
log.silent = functools.partial(log.log, 0)

class MyWorker:

    def worker(task_queue, socketio):

        alive = True

        sleep = 1

        log.info("worker starts!")

        while True:

            try:

                task = task_queue.get(block=True, timeout=1)

                log.info("emitting task: %s", task)

                sleep = 1
                socketio.emit("pong", f"task: {task}")

            except queue.Empty:

                sleep = 1

                log.info("Emitting pong, then sleeping for %s", sleep)

                socketio.emit("pong", "empty")

            time.sleep(sleep)

        log.info("worker finished")

    def __init__(self, socketio):

        self.task_queue = eventlet.Queue()
        
        for task in ["one"]:

            self.task_queue.put(task)

        self.worker = functools.partial(
            MyWorker.worker,
            task_queue=self.task_queue,
            socketio=socketio,
        )

        # self.thread = threading.Thread(target=worker, daemon=True)

    def start(self, socketio):

        log.info("starting thread")

        #self.thread = threading.Thread(target=self.worker, daemon=True)
        thread = socketio.start_background_task(self.worker)

        log.info("started")

        #self.thread.start()

    def push(self, msg):

        self.task_queue.put(msg)
