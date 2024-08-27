import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Chart from 'react-apexcharts';
// import{ BrowserRouter as Router, Route, Routes} from "react-router-dom";
// import AdjustTheLights from "./AdjustTheLights/AdjustTheLights";
// import Home from "./Home/Home";
// import PowerConsumption from "./PowerConsumption/PowerConsumption";
// import Notification1 from "./Notification1/Notification1";

function App() {

  
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/get_e_date'); // Sử dụng await để đợi axios hoàn thành
        setData(response.data); // Lưu dữ liệu vào state sau khi yêu cầu thành công
      } catch (error) {
        console.error("Có lỗi xảy ra khi lấy dữ liệu:", error); // Xử lý lỗi nếu yêu cầu thất bại
      }
    };

    fetchData(); // Gọi hàm fetchData
  }, []);


  const chartData = {
    series: [{
      name: 'Energy Consumed (kWh)',
      data: data.map(item => item.e_usage_daily) // Lấy giá trị năng lượng tiêu thụ
    }],
    options: {
      chart: {
        type: 'line',
        height: 350,  // Màu nền của biểu đồ
        toolbar: {
          show: false // Ẩn toolbar
        },
      },
      xaxis: {
        categories: data.map(item => item.date), // Lấy các ngày làm nhãn (x-axis)
        title: {
          text: 'Date'
        }
      },
      yaxis: {
        title: {
          text: 'Energy Consumed (kWh)'
        }
      },
      title: {
        text: 'Energy Consumption Over the Last 10 Days',
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
      <div id='chart'>
        <Chart
          options={chartData.options}
          series={chartData.series}
          type="line"
          height={500}
          width={1000}
        />
      </div>

        {/* 
            <div className="button-group">
              <button onClick={() => { setShowDaily(true); setShowMonthly(false); }}>Daily</button>
              <button onClick={() => { setShowDaily(false); setShowMonthly(true); }}>Monthly</button>
            </div>
        
        
            <Router>
            <Routes>
                <Route path ="/" element={<Home />} />
                <Route path ="/AdjustTheLights" element={<AdjustTheLights />} />
                <Route path ="/PowerConsumption" element={<PowerConsumption />} />
                <Route path ="/Notification1" element={<Notification1 />} />
                <Route path ="/barChartOfDay" element={<barChartOfDay />} />
                <Route path ="/barChartOfMonth" element={<barChartOfMonth />} />
            </Routes>
        </Router> */}
    </div>
  );
}

export default App;
