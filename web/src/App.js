import "fontsource-roboto";
import React, {
    useEffect,
    useState,
} from "react";
import './App.css';
import { TextField, Box, Button } from "@material-ui/core";
import io from "socket.io-client";

const listeners = [
    {
        name: "connected",
        listener: (msg) => {
            console.log("Received connected.", {msg})
        },
        name: "pong",
        listener: (msg) => {
            console.log("Received pong!", {msg})
        }
    },
]

const useApp = ({initListeners}) => {

    const [socket, setSocket] = useState(null);
    const [listeners, setListeners] = useState(initListeners)
    const [msg, setMsg] = useState("foo")

    useEffect(() => {
        const socket = io("localhost:5000");

        listeners.forEach(({ name, listener }, i) => {
            socket.on(name, listener);
        });

        setSocket(socket);

        return () => {
            socket.disconnect();
        };
    }, [listeners]);

    const doPing = () => {
        console.log("emitting ping")
        socket.emit("ping", "ping message")
    }

    const doPush = () => {
        console.log("emitting push:", msg)
        socket.emit("push", msg)
    }

    return {
        doPing,
        doPush,
        textField: {
            value: msg,
            onChange: event => setMsg(event.target.value)
        }
    }
}

const App = () => {

    const {
        doPing,
        doPush,
        textField,
    } = useApp({
        initListeners: listeners,
    })

    return <Box m="2em">
        <Button variant="contained" onClick={doPing}>Ping</Button>
        <Button variant="contained" onClick={doPush}>Push</Button>
        <TextField {...textField} />
    </Box>
}

export default App;
