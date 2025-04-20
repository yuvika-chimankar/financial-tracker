'use client'

import React from 'react';
import { useState, useEffect } from 'react'
// import { Dialog, DialogBackdrop, DialogPanel, DialogTitle } from '@headlessui/react'
// import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'
import { Input, Option, Select, Button, Dialog, Textarea, IconButton, Typography, DialogBody, DialogHeader, DialogFooter,} from "@material-tailwind/react";
import { XMarkIcon } from "@heroicons/react/24/outline";

const Expense = () => {

  const [open, setOpen] = useState(false);

  const [category, setCategory] = useState('');
  const [item, setItem] = useState('');
  const [amount, setAmount] = useState(0);
  const [date, setDate] = useState(new Date());
  const [description, setDescription] = useState('');
  const [userId, setUserId] = useState(null);

  const [expenses, setExpenses] = useState([]);

  useEffect(() => {
    const userIdLocal = localStorage.getItem('user_id');
    if (userIdLocal) {
      setUserId(userIdLocal);
    }
  }, []);

  useEffect(() => {
    if (userId) {
      fetchExpenses();
    }
  }, [userId]);

  const addExpense = async (e) => {
    e.preventDefault();
    console.log({ category, item, amount, date, description });
    
    const response = await fetch('http://127.0.0.1:5000/add-expense', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ userId, category, item, amount, date, description })
    });

    const data = await response.json();
    if (response.ok) {
      console.log(data);
      handleOpen();
      fetchExpenses();
      clearForm();
    } else {
      alert(data.message);
    }
  };

  const handleOpen = () => setOpen(!open);

  const clearForm = () => {
    setCategory('');
    setItem('');
    setAmount(0);
    setDate(new Date());
    setDescription('');
  }

  const fetchExpenses = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get-expenses/'+userId);
      const data = await response.json();
      setExpenses(data);
    } catch (error) {
      console.error('Error fetching expenses:', error);
    }
  };
  
  return (
    <>
      {/* <p>Create form</p>
        <p>Category, Item, Amount, Date</p>
        <p>Add expense button</p>
        <p>Expenses table</p> */}


      <div className='bg-[#060a14]'>
      <div className="m-8">
        <div className='flex justify-between mb-8'>
          <h1 className='text-2xl font-bold'>Expense</h1>
          <button onClick={handleOpen} className="rounded-full block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" type="button">
            Add Expense
          </button>
        </div>

        <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
          <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400 mb-8">
            <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" className="px-6 py-3">
                  Sr. No.
                </th>
                <th scope="col" className="px-6 py-3">
                  Category
                </th>
                <th scope="col" className="px-6 py-3">
                  Item
                </th>
                <th scope="col" className="px-6 py-3">
                  Amount
                </th>
                <th scope="col" className="px-6 py-3">
                  Date
                </th>
                <th scope="col" className="px-6 py-3">
                  Description
                </th>
              </tr>
            </thead>
            <tbody>
            {expenses.map((expense, index) => (
              <tr className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200" key={index}>
                <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  {index+1}
                </th>
                <td className="px-6 py-4">{expense.category}</td>
                <td className="px-6 py-4">{expense.item}</td>
                <td className="px-6 py-4">{expense.amount}</td>
                <td className="px-6 py-4">{expense.date}</td>
                <td className="px-6 py-4">{expense.description}</td>
              </tr>
              ))}
            </tbody>
          </table>
        </div>


        





{open && <div tabindex="-1" aria-hidden="true" className="overflow-y-auto fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
    <div className="relative p-4 w-full max-w-md max-h-full place-self-center">
        <div className="relative bg-white rounded-lg shadow-sm dark:bg-gray-700">
            <div className="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600 border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Create New Expense
                </h3>
                <button onClick={handleOpen} type="button" className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-toggle="crud-modal">
                    <svg className="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                    </svg>
                    <span className="sr-only">Close modal</span>
                </button>
            </div>
            <form className="p-4 md:p-5" onSubmit={addExpense}>
                <div className="grid gap-4 mb-4 grid-cols-2">
                    <div className="col-span-2">
                        <label for="category" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Category</label>
                        <input type="text" name="category" id="category" 
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Type category" required="true" />
                    </div>
                    <div className="col-span-2">
                        <label for="item" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Item</label>
                        <input type="text" name="item" id="item" 
                        value={item}
                        onChange={(e) => setItem(e.target.value)}
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Type item" required="true" />
                    </div>
                    <div className="col-span-2 sm:col-span-1">
                        <label for="amount" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Amount</label>
                        <input type="number" name="amount" id="amount" 
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Type amount" required="true" />
                    </div>
                    <div className="col-span-2 sm:col-span-1">
                      <label htmlFor="date" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Date</label>
                      <input datepicker id="default-datepicker" type="date" 
                      value={date}
                      onChange={(e) => setDate(e.target.value)}
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Select date" />
                    </div>

                    <div className="col-span-2">
                        <label for="description" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Description</label>
                        <textarea id="description" rows="4" 
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Write description here"></textarea>                    
                    </div>
                </div>
                <button type="submit" className="text-white inline-flex items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                    <svg className="me-1 -ms-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path></svg>
                    Add new record
                </button>
            </form>
        </div>
    </div>
</div> }


      </div>
      </div>
    </>
  )
}

export default Expense;