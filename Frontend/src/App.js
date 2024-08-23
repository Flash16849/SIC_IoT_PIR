// import logo from './logo.svg';
import './App.css';
import{ BrowserRouter as Router, Route, Routes} from "react-router-dom";
import AdjustTheLights from "./AdjustTheLights/AdjustTheLights";
import Home from "./Home/Home";
import PowerConsumption from "./PowerConsumption/PowerConsumption";
import Notification1 from "./Notification1/Notification1";

function App() {
  return (
    <div className="App">
        <Router>
            <Routes>
                <Route path ="/" element={<Home />} />
                <Route path ="/AdjustTheLights" element={<AdjustTheLights />} />
                <Route path ="/PowerConsumption" element={<PowerConsumption />} />
                <Route path ="/Notification1" element={<Notification1 />} />
                <Route path ="/barChartOfDay" element={<barChartOfDay />} />
                <Route path ="/barChartOfMonth" element={<barChartOfMonth />} />
            </Routes>
        </Router>
    </div>
  );
}

export default App;
