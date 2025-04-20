'use client'

import React, { useEffect, useState } from 'react'

const Dashboard = () => {

  const [userId, setUserId] = useState(null);
  const [salary, setSalary] = useState(0);
  const [budget, setBudget] = useState(0);
  const [remainingBudget, setRemainingBudget] = useState(0);
  const [pieChartUrl, setPieChartUrl] = useState('');
  const [barChartUrl, setBarChartUrl] = useState('');
  // const [lineChartUrl, setLineChartUrl] = useState('');

  useEffect(() => {
    const userIdLocal = localStorage.getItem('user_id');
    if (userIdLocal) {
      setUserId(userIdLocal);
    }
  }, []);

  useEffect(() => {
    if (userId) {
      fetchIncome();
    }
  }, [userId]);

  // useEffect(() => {
  //   // Trigger the backend to generate the chart
  //   if(userId) {
  //     fetch('http://127.0.0.1:5000/pie-chart', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({ userId }),
  //     })
  //       .then(async res => {
  //         console.log(res);
  //         const data = await res.json();
  //         if (res.ok) {
  //           console.log(data);
            
  //           // Set the chart image URL
  //           setPieChartUrl('http://127.0.0.1:5000'+data.chart_url);
  //         } else {
  //           console.error('Failed to generate visualization');
  //         }
  //       })
  //       .catch(err => console.error(err));

  //   }
  // }, [userId]);

  // useEffect(() => {
  //   // Trigger the backend to generate the chart
  //   if(userId) {
  //     fetch('http://127.0.0.1:5000/bar-chart', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({ userId }),
  //     })
  //       .then(async res => {
  //         console.log(res);
  //         const data = await res.json();
  //         if (res.ok) {
  //           console.log(data);
            
  //           // Set the chart image URL
  //           setBarChartUrl('http://127.0.0.1:5000'+data.chart_url);
  //         } else {
  //           console.error('Failed to generate visualization');
  //         }
  //       })
  //       .catch(err => console.error(err));

  //   }
  // }, [userId]);



  useEffect(() => {
    // Trigger the backend to generate the chart
    if(userId) {
      fetch('http://127.0.0.1:5000/charts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userId }),
      })
        .then(async res => {
          console.log(res);
          const data = await res.json();
          if (res.ok) {
            console.log(data);
            // Set the chart image URL
            setPieChartUrl('http://127.0.0.1:5000'+data.pie_chart_url);
            setBarChartUrl('http://127.0.0.1:5000'+data.bar_chart_url);
          } else {
            console.error('Failed to generate visualization');
          }
        })
        .catch(err => console.error(err));

    }
  }, [userId]);


  // useEffect(() => {
  //   // Trigger the backend to generate the chart
  //   if(userId) {
  //     fetch('http://127.0.0.1:5000/line-chart', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({ userId }),
  //     })
  //       .then(async res => {
  //         console.log(res);
  //         const data = await res.json();
  //         if (res.ok) {
  //           console.log(data);
            
  //           // Set the chart image URL
  //           setLineChartUrl('http://127.0.0.1:5000'+data.chart_url);
  //         } else {
  //           console.error('Failed to generate visualization');
  //         }
  //       })
  //       .catch(err => console.error(err));

  //   }
  // }, [userId]);

  const fetchIncome = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/get-remaining-budget', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userId })
      });
      const data = await res.json();

      if (res.ok) {
        console.log('Data :', data);
        setSalary(data.salary);
        setBudget(data.budget);
        setRemainingBudget(data.remaining_budget);
      } else {
        console.error(data.message);
      }
    } catch (err) {
      console.error('Failed to fetch income:', err.message);
    }
  };

  return (
    <>
    <div className='bg-[#060a14]'>
      <div className='m-8'>
        <h1 className='text-2xl font-bold'>Dashboard</h1>

        <section className=" body-font">
          <div className="container mx-auto">
            <div className="flex flex-wrap">
              <div className="xl:w-1/3 md:w-1/2 p-4">
                <div className="border border-sky-400 p-6 rounded-lg">
                  <div className="flex justify-between">
                    <h3 className="text-base  ">Salary</h3>
                  </div>
                  <h2 className="text-2xl mt-2">{salary}</h2>
                </div>
              </div>
              <div className="xl:w-1/3 md:w-1/2 p-4">
                <div className="border border-sky-400 p-6 rounded-lg">
                  <div className="flex justify-between">
                    <h3 className="text-base  ">Budget</h3>
                  </div>
                  <h2 className="text-2xl mt-2">{budget}</h2>
                </div>
              </div>
              <div className="xl:w-1/3 md:w-1/2 p-4">
                <div className="border border-sky-400 p-6 rounded-lg">
                  <div className="flex justify-between">
                    <h3 className="text-base  ">Remaining Budget</h3>
                  </div>
                  <h2 className="text-2xl mt-2">{remainingBudget}</h2>
                </div>
              </div>
            </div>
          </div>
        </section>

        <div className='charts'>
          <h1 className='text-lg font-semibold mb-8'>Charts</h1>
          <div className='flex mb-8'>
          <div className='me-8'>{pieChartUrl ? (
            <img src={pieChartUrl} alt="Pie Chart" style={{ width: '100%', maxWidth: '500px' }} />
          ) : (
            <p>Loading chart...</p>
          )}</div>
          <br />
          {barChartUrl ? (
            <img src={barChartUrl} alt="Bar Chart" style={{ width: '100%', maxWidth: '500px' }} />
          ) : (
            <p>Loading chart...</p>
          )}
</div>
          {/* {lineChartUrl ? (
            <img src={lineChartUrl} alt="line Chart" style={{ width: '100%', maxWidth: '500px' }} />
          ) : (
            <p>Loading chart...</p>
          )} */}
        </div>

      </div>
      </div>
    </>
  )
}

export default Dashboard;