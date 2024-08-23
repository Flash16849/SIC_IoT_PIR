
import { Line } from 'react-chartjs-2';
import {
  Chart as Chartjs,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,  
} from "chart.js";
import {ChartData} from "./Fake_Data"

Chartjs.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend, 
)

function barChartOfDay() {
  const options = {};
    
  return (
    <div className="App">
        <Line options={options} data={ChartData} />
    </div>
  );
}
  
  export default barChartOfDay;