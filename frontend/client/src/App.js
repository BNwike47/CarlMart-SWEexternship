import React, { useState, useEffect } from 'react'

function App() {

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

  return (
      <div>

          {(typeof data.home === 'undefined') ? (
            <p>Loading...</p>
          ) : (
            data.home.map((unit, i) => (
              <p key={i}> {unit} </p>
            ))
          )}

      </div>
  )
}

export default App