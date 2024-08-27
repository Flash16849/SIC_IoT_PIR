import './App.css';
import React, { useEffect, useState } from 'react';
import { database } from "./firebase";
import { ref, get } from "firebase/database";
import Chart from 'react-apexcharts';


function App() {

  
  const [showDaily, setShowDaily] = useState(true);
  const [showMonthly, setShowMonthly] = useState(false);
  const [dailyData, setDailyData] = useState([]);
  const [monthlyData, setMonthlyData] = useState([]);


  const fetchDailyData = () => {
    const dataRef = ref(database, "energy_usage");

    // Lấy dữ liệu từ Realtime Database
    get(dataRef)
      .then((snapshot) => {
        if (snapshot.exists()) {
          const fetchedData = snapshot.val();

          // Chỉ lấy 10 ngày gần nhất
          const sortedKeys = Object.keys(fetchedData).sort((a, b) => new Date(b) - new Date(a));
          const latest10Days = sortedKeys.slice(0, 10);

          const chartData = latest10Days.reverse().map((key) => ({
            date: key,
            energy: parseFloat(fetchedData[key].total_energy_consumed).toFixed(2),
          }));
          
          setDailyData(chartData);
        } else {
          console.log("No data available");
        }
      })
      .catch((error) => {
        console.error("Error fetching data: ", error);
      });
  };

  const fetchMonthlyData = () => {
    const dataRef = ref(database, "monthly_energy_usage");

    // Lấy dữ liệu từ Realtime Database
    get(dataRef)
      .then((snapshot) => {
        if (snapshot.exists()) {
          const fetchedData = snapshot.val();
          const currentYear = new Date().getFullYear();
          const yearData = fetchedData[currentYear];

          if (yearData) {
            const sortedMonths = Object.keys(yearData).sort(); // Sắp xếp các tháng
            const chartData = sortedMonths.slice(0, 12).map((month) => ({
              month: `${currentYear}-${month}`,
              energy: parseFloat(yearData[month].total_energy_consumed).toFixed(2),
            }));

            setMonthlyData(chartData);
          } else {
            console.log(`No data available for year ${currentYear}`);
          }
        } else {
          console.log("No data available");
        }
      })
      .catch((error) => {
        console.error("Error fetching data: ", error);
      });
  };

  

  useEffect(() => {
    fetchDailyData()
    fetchMonthlyData()
  }, []);


  const chartDaily = {
    series: [{
      name: 'Energy Consumed (Wh)',
      data: dailyData.map(data => data.energy), // Lấy giá trị năng lượng tiêu thụ
      color: "#fe7b23"
    }],
    options: {
      chart: {
        type: 'line',
        height: 350,  // Màu nền của biểu đồ
        toolbar: {
          show: false // Ẩn toolbar
        },
      },
      stroke: {
        curve: 'smooth' // Làm đường line mềm mại hơn
      },
      xaxis: {
        categories: dailyData.map(data => data.date), // Lấy các ngày làm nhãn (x-axis)
        title: {
          text: 'Date'
        }
      },
      yaxis: {
        title: {
          text: 'Energy Consumed (Wh)'
        }
      },
      title: {
        text: 'Energy Consumption Over the Last 10 Days',
        align: 'left'
      }
    }
  };

  const chartMonthly = {
    series: [{
      name: 'Energy Consumed (Wh)',
      data: monthlyData.map(data => data.energy), // Lấy giá trị năng lượng tiêu thụ
      color: "#0094ae" // Màu cho line
    }],
    options: {
      chart: {
        type: 'line',
        height: 350,  // Màu nền của biểu đồ
        toolbar: {
          show: false // Ẩn toolbar
        },
      },
      stroke: {
        curve: 'smooth' // Làm đường line mềm mại hơn
      },
      xaxis: {
        categories: monthlyData.map(data => data.month), // Lấy các ngày làm nhãn (x-axis)
        title: {
          text: 'Date'
        }
      },
      yaxis: {
        title: {
          text: 'Energy Consumed (Wh)'
        }
      },
      title: {
        text: 'Energy Consumption monthly',
        align: 'left'
      }
    }
  };

  return (
    <div className="App">
      <div className="circle1"></div>
      <div className="circle2"></div>
      <div id="banner-top">          
        <div className="top-title">
            <h1>Light Sensor</h1>
        </div>
      </div>

      <div className="button-container">
        <button onClick={() => { setShowDaily(true); setShowMonthly(false); }}>Daily</button>
        <button onClick={() => { setShowDaily(false); setShowMonthly(true); }}>Monthly</button>
      </div>

      <div id='chart'>

        {showDaily && 
          <Chart
            options={chartDaily.options}
            series={chartDaily.series}
            type="line"
            height={500}
            width={1000}
          />
        }

        {showMonthly && 
          <Chart
            options={chartMonthly.options}
            series={chartMonthly.series}
            type="line"
            height={500}
            width={1000}
          />
        }
      </div>
    </div>
  );
}

export default App;
