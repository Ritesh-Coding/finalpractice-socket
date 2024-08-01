import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const App = () => {
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState('');
    const [employeeId, setEmployeeId] = useState(1); // Replace with actual employee ID
    const chatSocket = useRef(null);

    useEffect(() => {
        // Fetch past messages
        axios.get('http://127.0.0.1:8000/api/chat/')
            .then(response => {
                setMessages(response.data);
            });

        // Connect to WebSocket
        chatSocket.current = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + employeeId
            + '/'
        );

        chatSocket.current.onmessage = function(e) {
            const data = JSON.parse(e.data);
            setMessages(prevMessages => [...prevMessages, data]);
        };

        chatSocket.current.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        return () => {
            chatSocket.current.close();
        };
    }, [employeeId]);

    const handleSendMessage = () => {
        chatSocket.current.send(JSON.stringify({
            'message': message,
            'employee_id': employeeId
        }));
        setMessage('');
    };

    return (
        <div>
            <textarea readOnly value={messages.map(msg => `${msg.employee_id}: ${msg.message}`).join('\n')} cols="100" rows="20" />
            <br />
            <input
                type="text"
                size="100"
                value={message}
                onChange={e => setMessage(e.target.value)}
                onKeyUp={e => { if (e.key === 'Enter') handleSendMessage(); }}
            />
            <br />
            <button onClick={handleSendMessage}>Send</button>
        </div>
    );
};

export default App;
