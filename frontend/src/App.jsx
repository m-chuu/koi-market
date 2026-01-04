import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [fishList, setFishList] = useState([])

  // 1. Fetch data from Python backend when page loads
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/fish')
      .then(response => {
        setFishList(response.data)
      })
      .catch(error => {
        console.error("Error fetching data:", error)
      })
  }, [])

  return (
    <div style={{ padding: "20px" }}>
      <h1>My Koi Fish Shop</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "20px" }}>

        {fishList.map((fish) => (
          <div key={fish.id} style={{ border: "1px solid #ccc", padding: "10px", borderRadius: "8px" }}>
            <img src={fish.image_url} alt={fish.name} style={{ width: "100%" }} />
            <h3>{fish.name}</h3>
            <p>Variety: {fish.variety}</p>
            <p style={{ fontWeight: "bold", color: "green" }}>RM {fish.price_myr}</p>
            <button>Add to Cart</button>
          </div>
        ))}

      </div>
    </div>
  )
}

export default App