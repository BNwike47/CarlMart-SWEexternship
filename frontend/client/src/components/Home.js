import React, { useState, useEffect } from 'react'

function App() {

  var jsonData = {
    "users": [
        {
            "name": "alan", 
            "age": 23,
            "username": "aturing"
        },
        {
            "name": "john", 
            "age": 29,
            "username": "__john__"
        }
    ]
  }

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/home").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  function handleClick() {
    
    // Send data to the backend via POST
    fetch('http://127.0.0.1:8080/home', {  // Enter your IP address here

      method: 'POST', 
      mode: 'cors', 
      body: JSON.stringify(jsonData) // body data type must match "Content-Type" header

    })
    
  }

  return (
    <>
      <div>

          {(typeof data.home === 'undefined') ? (
            <p>Loading...</p>
          ) : (
            data.home.map((unit, i) => (
              <p key={i}> {unit} </p>
            ))
          )}

      </div>

      <form>
      <label>
        Test text data:
        <input type="text" name="name" />
      </label>
      <input type="submit" value="Submit" />
      </form>

      <div onClick={handleClick} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      Send data to backend
    </div>

      </>
  )
}

export default App