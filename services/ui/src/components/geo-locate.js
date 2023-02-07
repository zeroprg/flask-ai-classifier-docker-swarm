import React, { useState, useEffect } from "react";
import axios from "axios";

const options = {
  method: "GET",
  url: "https://whoisapi-ip-geolocation-v1.p.rapidapi.com/api/v1",
  params: { ipAddress: "8.8.8.8" },
  headers: {
    "X-RapidAPI-Key": 0,
    "X-RapidAPI-Host": "whoisapi-ip-geolocation-v1.p.rapidapi.com",
  },
};

const Geo = (props) => {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
    options.params.ipAddress = "210.54.39.237";
   
      try {
        const response = await axios.request(options);
        setData(response.data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchData();
}, []);

return (
  <div>
    <p>Data: {JSON.stringify(data)}</p>
  </div>
);
};

export default Geo