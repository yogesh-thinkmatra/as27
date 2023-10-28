import React, { useState, useEffect } from "react";
import { Table,Button } from "flowbite-react";
import axios from "axios";
import { Link, Outlet } from "react-router-dom";
function Sites() {
    const [sites, setSites] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const handleClick = () => {
      setLoading(true);
      axios.get('http://127.0.0.1:8000/api/assign-site')
        .then(response => {
          console.log('Request successful:', response.data);
          getData()
        })
        .catch(error => {
          console.error('Request failed:', error);
    
        })
        .finally(() => {
          setLoading(false);
        });
    }

    
    const getData=()=>{
      axios
        .get("http://127.0.0.1:8000/api/site")
        .then((response) => {
          console.log("API Response:", response.data); // Log the API response
          setSites(response.data.data);
          setLoading(false);
        })
        .catch((error) => {
          console.error("API Error:", error); // Log any errors
          setError(error);
          setLoading(false);
        });
    }


  
    useEffect(() => {
      getData()
    }, []);
  
    if (loading) {
      return <div>Loading...</div>;
    }
  
    if (error) {
      return <div>Error: {error.message}</div>;
    }
  
  return (
    <div className="p-4">

<Button onClick={handleClick}>Auto Assign</Button>

    <Table>
      <Table.Head>
        <Table.HeadCell>Name</Table.HeadCell>
        <Table.HeadCell>Phone Number</Table.HeadCell>
        <Table.HeadCell>Grievance</Table.HeadCell>
        <Table.HeadCell>Assigned To</Table.HeadCell>
  
      </Table.Head>
      <Table.Body className="divide-y">
        {sites.map((site) => (
          <Table.Row
            key={site.id}
            className="bg-white dark:border-gray-700 dark:bg-gray-800"
          >
            <Table.Cell className="whitespace-nowrap font-medium text-gray-900 dark:text-white">
              {site.name}
            </Table.Cell>
            <Table.Cell>{site.phone_number}</Table.Cell>
            <Table.Cell>{site.grievance ? "Yes" : "No"}</Table.Cell>
            <Table.Cell>{site.electrician==null?"Not Assigned" :site.electrician}</Table.Cell>
            
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  </div>
  )
}

export default Sites