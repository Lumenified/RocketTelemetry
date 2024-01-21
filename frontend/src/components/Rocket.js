
function Rocket({ rocket }) {
  return (
    <div>
      <div><strong>INFO</strong></div>
      <div>ID: {rocket.id}</div>
      <div>Mass: {rocket.mass}</div>
      <div>Model: {rocket.model}</div>
      <div>Payload Description: {rocket.payload.description}</div>
      <div>Payload Weight: {rocket.payload.weight}</div>
      <div>Speed: {rocket.speed}</div>
      <div>Status: {rocket.status}</div>
      <div>Telemetry Host: {rocket.telemetry.host}</div>
      <div>Telemetry Port: {rocket.telemetry.port}</div>
      <div><strong>Timestamps</strong></div>
      <div>Cancelled: {rocket.timestamps.cancelled ? rocket.timestamps.cancelled : 'null'}</div>
      <div>Deployed: {rocket.timestamps.deployed ? rocket.timestamps.deployed : 'null'}</div>
      <div>Failed: {rocket.timestamps.failed ? rocket.timestamps.failed : 'null'}</div>
      <div>Launched: {rocket.timestamps.launched ? rocket.timestamps.launched : 'null'}</div>
    </div>
    
  );
}

export default Rocket;