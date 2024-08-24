import React, {useState} from "react";
import { Navigate } from "react-router-dom";
import './AdjustTheLights.css';
// import axios from 'axios';

function AdjustTheLights() {
    const[goToContactHome, setGoToContactHome] = useState(false);
    // const[goToContact, setGoToContact] = useState(false);
    const[goToContactPowerConsumption, setGoToContactPowerConsumption] = useState(false);
    const[goToContactNotification1, setGoToContactNotification1] = useState(false);
    // const [brightness] = useState(70);
    // // , setBrightness
    // const [isOn, setIsOn] = useState(false);

    if(goToContactHome){
        return <Navigate to = "/"/>
    }
    // if(goToContact){
    //     return <Navigate to = "/AdjustTheLights"/>
    // }
    if(goToContactPowerConsumption){
        return <Navigate to = "/PowerConsumption"/>
    }
    if(goToContactNotification1){
        return <Navigate to = "/Notification1"/>
    }


    

    

    // const handleBrightnessChange = (e) => {
    //   const newBrightness = e.target.value;
    //   setBrightness(newBrightness);
    //   if (isOn) {
    //     // Gửi yêu cầu điều chỉnh độ sáng khi đèn đang bật
    //     axios.post('/api/led', {
    //       action: 'on',
    //       brightness: newBrightness
    //     })
    //     .then(response => console.log(response.data))
    //     .catch(error => console.error('There was an error!', error));
    //   }
    // };
    
    // const toggleLight = () => {
    //   const action = isOn ? 'off' : 'on';
    //   axios.post('/api/led', {
    //     action: action,
    //     brightness: brightness
    //   })
    //   .then(response => console.log(response.data))
    //   .catch(error => console.error('There was an error!', error));
    //   setIsOn(!isOn);
    // };

    


    return (
      <div className="App">
          <div id="banner-top">          
              <div class="top-title">
                  <h1>Light Sensor</h1>
              </div>
                  <div class="top-list-menu">
                  <div class="top-menu">
                      <button class="buttonOfWedsite" onClick={() =>
                        setGoToContactHome(true)
                      }>Home</button>
                  </div>
                  <div class="top-menu-1">
                      <button class="buttonOfWedsite">Adjust the lights</button>
                  </div>  
                  <div class="top-menu">
                      <button class="buttonOfWedsite" onClick={() =>
                        setGoToContactPowerConsumption(true)
                      }>Power consumption</button>
                  </div>
                  <div class="top-menu">
                      <button class="buttonOfWedsite" onClick={() =>
                        setGoToContactNotification1(true)
                      }>Notification</button>
                  </div>
              </div>
          </div>
          <div class="circle1"></div>
          <div class="circle2"></div>
          <div>
          <div class="buttonMain">
            {/* <button class="buttonOnOff1" onClick={() => toggleLight()}
              {...isOn ? 'off' : 'on'}
              >Turn on</button> */}
            {/* <button class="buttonOnOff2">Turn off</button> */}
          </div>
          </div>
          <div id="container">
            <div class="square">
                <input type="range" id="bright-range" min="20" max="90" onchange="fun(this)"></input>
            </div>
          </div>
      </div>
    );
  }


  // const turnOnLed = (brightness) => {
  //   fetch('/api/led', {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json'
  //     },
  //     body: JSON.stringify({
  //       action: 'on',
  //       brightness: brightness
  //     })
  //   })
  //   .then(response => response.json())
  //   .then(data => console.log(data));
  // };
  
  // const turnOffLed = () => {
  //   fetch('/api/led', {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json'
  //     },
  //     body: JSON.stringify({
  //       action: 'off'
  //     })
  //   })
  //   .then(response => response.json())
  //   .then(data => console.log(data));
  // };
  
  export default AdjustTheLights;