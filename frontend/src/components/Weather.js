import {useEffect, useState, useMemo} from "react";
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
  const rain = weatherCondition?.precipitation?.rain;
  const snow = weatherCondition?.precipitation?.snow;
  const sleet = weatherCondition?.precipitation?.sleet;
  const hail = weatherCondition?.precipitation?.hail;
  const [precipitationIcon, setPrecipitationIcon] = useState(null);
  const precipitationIcons = useMemo(() => ({
    rain: 'wi-rain',
    snow: 'wi-snow',
    sleet: 'wi-sleet',
    hail: 'wi-hail',
    mix: 'wi-rain-mix',
  }), []);
  
  useEffect(() => {
    let icon = null;
    if (snow && rain) {
      icon = <i className={`wi ${precipitationIcons.mix}`} style={{ fontSize: '3em' }}></i>;
    }
    else if (rain) {
      icon = <i className={`wi ${precipitationIcons.rain}`} style={{ fontSize: '3em' }}></i>;
    } else if (snow) {
      icon = <i className={`wi ${precipitationIcons.snow}`} style={{ fontSize: '3em' }}></i>;
    } else if (sleet) {
      icon = <i className={`wi ${precipitationIcons.sleet}`} style={{ fontSize: '3em' }}></i>;
    } else if (hail) {
      icon = <i className={`wi ${precipitationIcons.hail}`} style={{ fontSize: '3em' }}></i>;
    }
      
    if (!icon) {
      icon = <i className="wi wi-day-sunny" style={{ fontSize: '3em' }} />;
    }
    setPrecipitationIcon(icon);
  }, [rain, snow, sleet, hail, precipitationIcons]);

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