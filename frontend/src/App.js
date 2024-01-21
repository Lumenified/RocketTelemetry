import React, { useState, useEffect } from 'react';
import Weather from './components/Weather';
import RocketList from './components/RocketList';
import { MDBCard, MDBCardBody, MDBCardTitle } from 'mdb-react-ui-kit';
import { ThemeProvider, createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light', // or 'dark'
  },
});

function App() {
  const [data, setData] = useState({rockets: [], weather: {}});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8080', {
      headers: {
        'Content-Type': 'application/json; charset=utf-8'
      }
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      setData(data);
      setIsLoading(false);
    });
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <header className="App-header">
        <div className='content flex-column d-flex justify-content-center align-items-center'>
    <MDBCard style={{ width: "50rem"}}>
      <MDBCardBody>
        <MDBCardTitle>Weather</MDBCardTitle>
        <div>
          <Weather weather={data.weather} />
        </div>
      </MDBCardBody>
    </MDBCard>
            <MDBCard className="dark-theme">
              <MDBCardBody>
                <MDBCardTitle>Rocket List</MDBCardTitle>
                <div>
                  <RocketList data={data.rockets} />
                </div>
              </MDBCardBody>
            </MDBCard>
          </div>
        </header>
      </div>
    </ThemeProvider>
  );
}

export default App;