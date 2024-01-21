import React, { useRef, useState, useEffect } from 'react';
import io from 'socket.io-client';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Rocket from './Rocket';
import SocketData from './SocketData';
import RocketSocketData from './RocketSocketData';

const RocketList = ({ data }) => {
  const [socketData, setSocketData] = useState(null);
  const socketRef = useRef(null);

  useEffect(() => {
    socketRef.current = io('http://localhost:8080');

    socketRef.current.on('connect', () => {
      console.log("I'm connected!");
    });

    socketRef.current.on('update_data', (allData) => {
      console.log('I received a message!');
      console.log(allData);
      setSocketData(allData);
    });

    socketRef.current.on('disconnect', () => {
      console.log("I'm disconnected!");
    });

    // Clean up the effect
    return () => socketRef.current.disconnect();
  }, []); // Re-run the effect when the id or socketDataRef changes

  return (
    <div>
      {data.map((rocket, index) => (
        <Accordion key={index}>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls={`panel${index}-content`}
            id={`panel${index}-header`}
          >
            <div>
              <Typography>{rocket.model}</Typography>
              <Typography>{rocket.payload.description}</Typography>
            </div>
          </AccordionSummary>
          <AccordionDetails>
            <Rocket rocket={rocket} />
            {socketData && <RocketSocketData data={socketData.find(rocketData => rocketData.id === rocket.id)} rocketId={rocket.id}/>}
          </AccordionDetails>
        </Accordion>
      ))}
    </div>
  );
};

export default RocketList;