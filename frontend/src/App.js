import { useState, useEffect } from "react"
import axios from "axios"
import "./App.css"
import { Bar } from "react-chartjs-2"
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from "chart.js"

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

function App() {
  const [logged, setLogged] = useState(false)
  const [u, setU] = useState("")
  const [p, setP] = useState("")
  const [chart, setChart] = useState([])

  const login = () => {
    axios.post("http://127.0.0.1:8000/api/login/", {
      username: u,
      password: p
    }).then(res => {
      if (res.data.ok) setLogged(true)
      else alert("Invalid login")
    })
  }

  useEffect(() => {
    if (logged) {
      axios.get("http://127.0.0.1:8000/api/chart/")
        .then(res => setChart(res.data))
    }
  }, [logged])

  if (!logged) {
    return (
      <div className="login-box">
        <h2>Electricity Board Login</h2>
        <input placeholder="Username" onChange={e => setU(e.target.value)} />
        <input type="password" placeholder="Password" onChange={e => setP(e.target.value)} />
        <button onClick={login}>Login</button>
      </div>
    )
  }

  const totalApproved = chart.find(x => x.status === "Approved")?.count || 0
  const totalPending = chart.find(x => x.status === "Pending")?.count || 0
  const totalRejected = chart.find(x => x.status === "Rejected")?.count || 0

  const chartData = {
    labels: chart.map(x => x.status),
    datasets: [
      {
        label: "Applications",
        data: chart.map(x => x.count)
      }
    ]
  }

  return (
    <>
      <div className="navbar">
        <h3>Electricity Board System</h3>
        <button className="logout" onClick={() => setLogged(false)}>Logout</button>
      </div>

      <div className="container">
        <div className="stats">
          <div className="stat">Approved<br /><b>{totalApproved}</b></div>
          <div className="stat">Pending<br /><b>{totalPending}</b></div>
          <div className="stat">Rejected<br /><b>{totalRejected}</b></div>
        </div>

        <div className="card">
          <h2 className="dashboard-title">Electricity Board Dashboard</h2>
          <Bar data={chartData} />
        </div>
      </div>
    </>
  )
}

export default App
