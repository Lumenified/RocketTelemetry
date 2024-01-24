/* import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';

const SocketData = ({ id, children, socketDataRef }) => {
  const [data, setData] = useState(null);
  const socketRef = useRef(null);

  useEffect(() => {
    socketRef.current = io('http://localhost:8080');

    socketRef.current.on('connect', () => {
      console.log("I'm connected!");
    });

    socketRef.current.on('update_data', (allData) => {
      console.log('I received a message!');
      console.log(allData);

      // Find the data for the current rocket
      const rocketData = allData.find(rocket => rocket.id === id);
      if (rocketData) {
        setData(rocketData);
        // Update the ref with the socket data
        socketDataRef.current = rocketData;
      }
    });

    socketRef.current.on('disconnect', () => {
      console.log("I'm disconnected!");
    });

    // Clean up the effect
    return () => socketRef.current.disconnect();
  }, [id, socketDataRef]); // Re-run the effect when the id or socketDataRef changes

  return children(data);
};

export default SocketData;*/