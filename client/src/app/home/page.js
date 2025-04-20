'use client';

import React, { useEffect, useRef, useState } from 'react'

const Home = () => {

  const [isEditingSalary, setIsEditingSalary] = useState(false);
  const [isEditingBudget, setIsEditingBudget] = useState(false);
  const [salary, setSalary] = useState(0);
  const [budget, setBudget] = useState(0);
  const [userId, setUserId] = useState(null);

  const salaryRef = useRef(null);
  const budgetRef = useRef(null);

  const handleEditSalary = () => {
    setIsEditingSalary(true);
    setTimeout(() => salaryRef.current?.focus(), 0);
  };

  const handleEditBudget = () => {
    setIsEditingBudget(true);
    setTimeout(() => budgetRef.current?.focus(), 0);
  };

  const fetchIncome = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/get-income', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userId })
      });
      const data = await res.json();

      if (res.ok) {
        console.log('Income:', data);
        setSalary(data.salary);
        setBudget(data.budget);
      } else {
        console.error(data.message);
      }
    } catch (err) {
      console.error('Failed to fetch income:', err.message);
    }
  };


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


  // handle outside click
  useEffect(() => {
    const handleClickOutside = async (e) => {
      if (isEditingSalary && salaryRef.current && !salaryRef.current.contains(e.target)) {
        setIsEditingSalary(false);
        try {
          const res = await fetch('http://127.0.0.1:5000/update-salary', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId, salary }),
          });

          const result = await res.json();
          if (!res.ok) throw new Error(result.message);
          fetchIncome();
          console.log('Salary updated');
        } catch (err) {
          console.error('Failed to update salary:', err.message);
        }
      }
      if (isEditingBudget && budgetRef.current && !budgetRef.current.contains(e.target)) {
        setIsEditingBudget(false);
        try {
          const res = await fetch('http://127.0.0.1:5000/update-budget', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId, budget }),
          });

          const result = await res.json();
          if (!res.ok) throw new Error(result.message);
          fetchIncome();
          console.log('Budget updated');
        } catch (err) {
          console.error('Failed to update budget:', err.message);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isEditingSalary, salary, isEditingBudget, budget]);

  return (
    <>
      <div className='m-8'>
        <h1 className='text-lg'>Home page</h1>
        <section className="text-gray-600 body-font">
          <div className="container mx-auto">
            <div className="flex flex-wrap">
              <div className="xl:w-1/3 md:w-1/2 p-4">
                <div className="border border-gray-200 p-6 rounded-lg">
                  <div className="flex justify-between">
                    <h3 className="text-base text-gray-900">Salary</h3>
                    <svg
                      className="w-6 h-6 text-gray-800 dark:text-white cursor-pointer"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      onClick={handleEditSalary}
                    >
                      <path
                        stroke="currentColor"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="m14.304 4.844 2.852 2.852M7 7H4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-4.5m2.409-9.91a2.017 2.017 0 0 1 0 2.853l-6.844 6.844L8 14l.713-3.565 6.844-6.844a2.015 2.015 0 0 1 2.852 0Z"
                      />
                    </svg>
                  </div>
                  {isEditingSalary ? (
                    <input
                      type='number'
                      ref={salaryRef}
                      className="text-2xl border border-gray-300 rounded px-2 py-1 mt-2 w-full"
                      value={salary}
                      onChange={(e) => setSalary(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && setIsEditingSalary(false)}
                    />
                  ) : (
                    <h2 className="text-2xl mt-2">{salary}</h2>
                  )}
                </div>
              </div>

              <div className="xl:w-1/3 md:w-1/2 p-4">
                <div className="border border-gray-200 p-6 rounded-lg">
                  <div className="flex justify-between">
                    <h3 className="text-base text-gray-900">Budget</h3>
                    <svg
                      className="w-6 h-6 text-gray-800 dark:text-white cursor-pointer"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      onClick={handleEditBudget}
                    >
                      <path
                        stroke="currentColor"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="m14.304 4.844 2.852 2.852M7 7H4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-4.5m2.409-9.91a2.017 2.017 0 0 1 0 2.853l-6.844 6.844L8 14l.713-3.565 6.844-6.844a2.015 2.015 0 0 1 2.852 0Z"
                      />
                    </svg>
                  </div>
                  {isEditingBudget ? (
                    <input
                      type='number'
                      ref={budgetRef}
                      className="text-2xl border border-gray-300 rounded px-2 py-1 mt-2 w-full"
                      value={budget}
                      onChange={(e) => setBudget(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && setIsEditingBudget(false)}
                    />
                  ) : (
                    <h2 className="text-2xl mt-2">{budget}</h2>
                  )}
                </div>
              </div>
            </div>
          </div>
        </section>

        <h1 className='mb-2 text-lg font-semibold text-gray-900 dark:text-white'>Recommendations</h1>
        <ul class="max-w-md space-y-1 text-gray-500 list-disc list-inside dark:text-gray-400">
            <li>
                At least 10 characters (and up to 100 characters)
            </li>
            <li>
                At least one lowercase character
            </li>
            <li>
                Inclusion of at least one special character, e.g., ! @ # ?
            </li>
        </ul>

      </div>

    </>
  )
}

export default Home