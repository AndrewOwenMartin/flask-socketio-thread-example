# Flask WebSocket example

Go into `thread-test/web/` and run `npm start`

Go into `thread-test`, activate the venv and run `python -m app`

Open the app at `localhost:3000` and look in the web console.

You should see the server looking in its task queue and sleeping when it's empty.

If you click 'ping', then when the server wakes you'll receive `Received pong!  Object { msg: "from ping" }` in the console.

If you click 'push', then when the server wakes you'll receive `Received pong!  Object { msg: "task: $MSG" }` where `$MSG` will be whatever was in the text box when you clicked.

This shows that socketio is emitting in a thread and in the main app, this is mainly down to using `eventlet.Queue` instead of `queue.Queue` from the standard library and `start_background_task` rather than `threading.Thread` from the standard library. 
