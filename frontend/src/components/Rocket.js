import Button from '@mui/material/Button';
import { Grid } from '@mui/material';

function Rocket({ rocket, updateRocket, socketData}) {
  
  const launchRocket = async () => {
    try {
      const response = await fetch(`http://localhost:8080/launch_rocket/${rocket.id}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      // Add a delay before fetching the rocket data
      setTimeout(async () => {
        const data = await response.json();
        updateRocket(data);
      }, 500); // Delay for 1 second
    } catch (error) {
      console.error('Failed to launch rocket:', error);
    }
  };

  const deployRocket = async () => {
    try {
      const response = await fetch(`http://localhost:8080/deploy_rocket/${rocket.id}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      //console.log(data);
  
      updateRocket(data); // Update the rocket data in the parent component
    } catch (error) {
      console.error('Failed to launch rocket:', error);
    }
  };
  
  const cancelRocket = async () => {
    try {
      const response = await fetch(`http://localhost:8080/cancel_rocket/${rocket.id}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      //console.log(data);
  
      updateRocket(data); // Update the rocket data in the parent component
    } catch (error) {
      console.error('Failed to launch rocket:', error);
    }
  };

  return (
    <Grid container spacing={3}>
    <Grid item xs={12} sm={4}>
      <div><strong>Rocket Info</strong></div>
      <div>ID: {rocket.id}</div>
      <div>Mass: {rocket.mass}</div>
      <div>Payload Weight: {rocket.payload.weight}</div>
      <div>Telemetry Host: {rocket.telemetry.host}</div>
      <div>Telemetry Port: {rocket.telemetry.port}</div>
    </Grid>
    <Grid item xs={12} sm={4}>
      <div><strong>Telemetry Timestamps</strong></div>
      <div>Rocket Status: {rocket.status}</div>
      <div>Cancelled: {rocket.timestamps.cancelled ? rocket.timestamps.cancelled : 'null'}</div>
      <div>Deployed: {rocket.timestamps.deployed ? rocket.timestamps.deployed : 'null'}</div>
      <div>Launched: {rocket.timestamps.launched ? rocket.timestamps.launched : 'null'}</div>
      <div>Failed: {rocket.timestamps.failed ? rocket.timestamps.failed : 'null'}</div>
    </Grid>
    <Grid item xs={12} sm={4}>
      <div><strong>Realtime Data</strong></div>
      <div>Acceleration: {socketData.acceleration}</div>
      <div>Altitude: {socketData.altitude}</div>
      <div>Speed: {socketData.speed}</div>
      <div>Thrust: {socketData.thrust}</div>
      <div>Temperature: {socketData.temperature}</div>
    </Grid>
    <Grid item xs={12}>
    <Grid container justifyContent="center">
      <Button variant="contained" color="primary" style={{margin: '3%'}} onClick={deployRocket} disabled={rocket.status === "deployed"}>
        Deploy
      </Button>
      <Button variant="contained" color="secondary" style={{margin: '3%'}} onClick={launchRocket} disabled={rocket.status === "launched"}>
        Launch
      </Button>
      <Button variant="contained" color="error" style={{margin: '3%'}} onClick={cancelRocket} disabled={rocket.status === 'deployed' || rocket.status === 'cancelled' || rocket.status === 'waiting'}>
        Cancel
      </Button>
    </Grid>
  </Grid>
    </Grid>
    
  );
}

export default Rocket;