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

from my_worker import MyWorker

log = logging.getLogger(__name__)
log.silent = functools.partial(log.log, 0)

my_worker = None #MyWorker()

worker = None

def init_app():

    global my_worker

    app = flask.Flask(__name__)

    app.config["SECRET_KEY"] = "tkmu7l90u578t3q2cbvsd78345i8gbmghjp70i8ltheuyt"

    socketio = flask_socketio.SocketIO(app, async_mode=None, cors_allowed_origins="*")

    my_worker = MyWorker(socketio=socketio)

    def run(socketio, app):

        log.info("my_worker starting")

        my_worker.start(socketio=socketio)

        log.info("socketio=%s, app=%s, my_worker=%s", socketio, app, my_worker)

        socketio.run(app, debug=False)


    run_server = functools.partial(run, socketio=socketio, app=app)

    return socketio, run_server

socketio, run_server = init_app()

def main():

    log.info("run_server()")
    run_server()
    log.info("run_server() ends")



@socketio.on("connect")
def handle_connect(*args, **kwargs):

    log.info("Received: connect")

    socketio.emit("connected", "you are connected")

@socketio.on("ping")
def handle_connect(*args, **kwargs):

    log.info("Received: ping. Returning pong. args=%s, kwargs=%s", args, kwargs)

    socketio.emit("pong", "from ping")

@socketio.on("push")
def handle_push(msg):
    
    my_worker.push(msg)

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-4s %(name)s %(message)s",
        style="%",
    )

    log.info("main()")

    main()
