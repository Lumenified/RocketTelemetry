import Button from '@mui/material/Button';

function RocketSocketData({ data, rocketId }) {
  const launchRocket = async () => {
    try {
      const response = await fetch(`http://localhost:8080/launch_rocket/${rocketId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Refresh the page after the request
      window.location.reload();
    } catch (error) {
      console.error('Failed to launch rocket:', error);
    }
  };

  const deployRocket = async () => {
    try {
      const response = await fetch(`http://localhost:8080/deploy_rocket/${rocketId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Refresh the page after the request
      window.location.reload();
    } catch (error) {
      console.error('Failed to launch rocket:', error);
    }
  };

  const cancelRocket = async () => {
    try {
      const response = await fetch(`http://localhost:8080/cancel_rocket/${rocketId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Refresh the page after the request
      window.location.reload();
    } catch (error) {
      console.error('Failed to launch rocket:', error);
    }
  };



    return (
      <div>
        <div><strong>Telemetry Data</strong></div>
        <div>Acceleration: {data.acceleration}</div>
        <div>Speed: {data.speed}</div>
        <div>Thrust: {data.thrust}</div>
        <div>Altitude: {data.altitude}</div>
        <div>Temperature: {data.temperature}</div>
        <Button variant="contained" color="primary" style={{margin: '3%'}} onClick={deployRocket}>
        Deploy
      </Button>
      <Button variant="contained" color="secondary" style={{margin: '3%'}} onClick={launchRocket}>
        Launch
      </Button>
      <Button variant="contained" color="error" style={{margin: '3%'}} onClick={cancelRocket}>
        Cancel
      </Button>
      </div>
    );
  }
  
  export default RocketSocketData;