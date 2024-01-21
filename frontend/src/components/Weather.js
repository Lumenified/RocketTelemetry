import React from "react";
import {
  MDBCard,
  MDBCardBody,
  MDBCol,
  MDBRow,
  MDBTypography,
} from "mdb-react-ui-kit";



function WeatherDetail({ label, value }) {
  return (
    <MDBTypography variant="body1">
      {label}: {value}
    </MDBTypography>
  );
}



function Weather({ weather }) {
  const weatherCondition = weather;
  const Temperature = weatherCondition?.temperature;
  const speed = weatherCondition?.wind?.speed;
  let precipitationIcon;
  const precipitationTypes = Object.keys(weatherCondition.precipitation);
  for (let i = 0; i < precipitationTypes.length; i++) {
    if (weatherCondition.precipitation[precipitationTypes[i]]) {
      precipitationIcon = <i className={`wi wi-${precipitationTypes[i]}`} style={{ fontSize: '3em' }} />;
      break;
    }
  }
  if (!precipitationIcon) {
    precipitationIcon = <i className="wi wi-day-sunny" style={{ fontSize: '3em' }} />;
  }
  return (
    <MDBCard style={{ width: "100%" }}>
  <MDBCardBody>
    <MDBRow>
      <MDBCol md="6" className="text-left">
        <MDBTypography variant="h6" className="mb-3 text-muted">{weatherCondition.time}</MDBTypography>
        <WeatherDetail label="Temperature" value={`${Temperature}°C`} />
        <WeatherDetail label="Humidity" value={`${weatherCondition.humidity}%`} />
        <WeatherDetail label="Pressure" value={`${weatherCondition.pressure} hPa`} />
      </MDBCol>
      <MDBCol md="6" className="text-center">
      <i className={`wi wi-wind towards-${Math.round(weatherCondition.wind.angle)}-deg`} style={{ fontSize: '3em' }} />
      <p>{`${speed} m/s`}</p>
  <div>
    {precipitationIcon}
  </div>  
</MDBCol>
    </MDBRow>
  </MDBCardBody>
</MDBCard>
  );
}
export default Weather;