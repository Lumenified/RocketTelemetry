import React, { useState, useEffect } from 'react';
import Weather from './components/Weather';
import RocketList from './components/RocketList';
import { MDBCard, MDBCardBody, MDBCardTitle } from 'mdb-react-ui-kit';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Grid } from '@mui/material';

const theme = createTheme({
  palette: {
    mode: 'light', // or 'dark'
  },
});

function App() {
  const [data, setData] = useState({rockets: [], weather: {}});
  const [isLoading, setIsLoading] = useState(true);
  const [isInitialFetch, setIsInitialFetch] = useState(true);
  /*
  EventSource is a built-in browser API that allows us to receive server-sent events.
  */
  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8080/weather");
  
    eventSource.onmessage = (event) => {
      const updatedWeather = JSON.parse(event.data);
      //console.log(updatedWeather);
      setData(prevData => ({...prevData, weather: updatedWeather}));
    };
    
    return () => {
      eventSource.close();
    };
  }, []);

  useEffect(() => {
    const fetchData = () => {
      fetch('http://localhost:8080', {
        headers: {
          'Content-Type': 'application/json; charset=utf-8'
        }
      })
      .then(response => response.json())
      .then(data => {
        //console.log(data);
        setData(data);
        setIsLoading(false);
        if (isInitialFetch) {
          setIsInitialFetch(false);
        }
      });
    };
    
    

    fetchData();
  }, [isInitialFetch]);

  const updateRocket = (updatedRocket) => {
    setData((prevData) => {
      return {
        ...prevData,
        rockets: prevData.rockets.map((rocket) =>
          rocket.id === updatedRocket.id ? updatedRocket : rocket
        ),
      };
    });
  };
  if (isInitialFetch && isLoading) {
    return <div>Loading...</div>;
  }


  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
  <ThemeProvider theme={theme}>
    <header className="App-header">
      <Grid container direction="row" alignItems="center" justify="center" spacing={2}>
        <Grid item xs={12} sm={12} md={12}>
          <MDBCard>
            <MDBCardBody>
              <MDBCardTitle>Weather</MDBCardTitle>
              <div>
                <Weather weather={data.weather} />
              </div>
            </MDBCardBody>
          </MDBCard>
        </Grid>
        <Grid item xs={12} sm={12} md={12}>
          <MDBCard className="dark-theme">
            <MDBCardBody>
              <MDBCardTitle>Rocket List</MDBCardTitle>
              <div>
                <RocketList rockets={data.rockets} updateRocket={updateRocket} />
              </div>
            </MDBCardBody>
          </MDBCard>
        </Grid>
      </Grid>
    </header>
  </ThemeProvider>
);
}

export default App;