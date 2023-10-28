import React, { useState, useEffect } from "react";
import { Table } from "flowbite-react";
import axios from "axios";
function Electricians() {
  const [electricians, setElectricians] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/electrician")
      .then((response) => {
        console.log("API Response:", response.data); // Log the API response
        setElectricians(response.data.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("API Error:", error); // Log any errors
        setError(error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div className="p-4">
      <Table>
        <Table.Head>
          <Table.HeadCell>Name</Table.HeadCell>
          <Table.HeadCell>Phone Number</Table.HeadCell>
          <Table.HeadCell>Grievance</Table.HeadCell>
          <Table.HeadCell>Zone</Table.HeadCell>
          <Table.HeadCell>Total Allocation</Table.HeadCell>
        
        </Table.Head>
        <Table.Body className="divide-y">
          {electricians.map((electrician) => (
            <Table.Row
              key={electrician.id}
              className="bg-white dark:border-gray-700 dark:bg-gray-800"
            >
              <Table.Cell className="whitespace-nowrap font-medium text-gray-900 dark:text-white">
                {electrician.name}
              </Table.Cell>
              <Table.Cell>{electrician.phone_number}</Table.Cell>
              <Table.Cell>{electrician.grievance ? "Yes" : "No"}</Table.Cell>
              <Table.Cell>{electrician.cities.join(", ")}</Table.Cell>
              <Table.Cell>{electrician.allotment_count}</Table.Cell>
             
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    </div>
  );
}

export default Electricians;
