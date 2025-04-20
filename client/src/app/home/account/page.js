'use client'

import React, { useState, useEffect } from 'react'

const Account = () => {

  const [userId, setUserId] = useState(null);
  const [user, setUser] = useState(null);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [dob, setDob] = useState(new Date());
  const [gender, setGender] = useState('');

  useEffect(() => {
    const userIdLocal = localStorage.getItem('user_id');
    if (userIdLocal) {
      setUserId(userIdLocal);
    }
  }, []);

  useEffect(() => {
    if (userId) {
      fetchUser();
    }
  }, [userId]);

  const fetchUser = async () => {
    if (!userId) return;

    try {
      const response = await fetch(`http://127.0.0.1:5000/account/${userId}`);

      const data = await response.json();

      if (response.ok) {
        console.log("Fetched user:", data);
        // Do something with the user data, like setting it to state
        setUser(data);
        // setDateFormat(data.dob);
      } else {
        console.error("Failed to fetch user:", data.message);
      }
    } catch (error) {
      console.error("Error fetching user:", error);
    }
  };

  const handleGenderChange = (e) => {
    setGender(e.target.value);
    console.log('Selected Gender:', e.target.value);
  };

  const updateAccount = async () => {
    if (!userId) {
      console.error('User ID is missing');
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:5000/update-account/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, dob, gender }),
      });

      const data = await response.json();

      if (response.ok) {
        alert('User updated successfully!');
        fetchUser();
        console.log(data);
      } else {
        alert('Failed to update user');
      }
    } catch (error) {
      console.error('Error updating user:', error);
    }
  };

  const setDateFormat = (dateStr) => {
    console.log(dateStr);

    const date = new Date(dateStr);

    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();

    const formattedDate = `${year}-${month}-${day}`;
    console.log(formattedDate);
    return formattedDate;
  }


  return (
    <>
      <div className='m-8'>
        <h1>Account</h1>
        <form className="max-w-sm mx-auto" onSubmit={updateAccount}>
          <div className="mb-5">
            <label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your name</label>
            <input type="text" id="name"
              value={user?.name}
              onChange={(e) => setName(e.target.value)}
              className="shadow-xs bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-xs-light" required />
          </div>
          <div className="mb-5">
            <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your email</label>
            <input type="email" id="email"
              value={user?.email}
              onChange={(e) => setEmail(e.target.value)}
              className="shadow-xs bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-xs-light" required />
          </div>
          <div className="mb-5">
            <label htmlFor="dob" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your date of birth</label>
            <input type="date" id="dob"
              value={setDateFormat(user?.dob)}
              onChange={(e) => setDob(e.target.value)}
              className="shadow-xs bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-xs-light" />
          </div>
          <div className="mb-5">
            <label htmlFor="gender" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">You gender</label>
            <div className="flex items-center mb-4">
              <input id="default-radio-1" type="radio" value="male" name="gender"
                checked={user?.gender === 'male'}
                onChange={handleGenderChange}
                className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
              <label htmlFor="default-radio-1" className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Male</label>
            </div>
            <div className="flex items-center">
              <input id="default-radio-2" type="radio" value="female" name="gender"
                checked={user?.gender === 'female'}
                onChange={handleGenderChange}
                className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
              <label htmlFor="default-radio-2" className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Female</label>
            </div>
          </div>
          <button type="submit" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Save</button>
        </form>

      </div>
    </>
  )
}

export default Account;