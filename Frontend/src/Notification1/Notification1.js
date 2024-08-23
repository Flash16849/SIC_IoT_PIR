import React from "react";
import { Navigate } from "react-router-dom";
import './Notification1.css';

function Notification1() {
    const[goToContactHome, setGoToContactHome] = React.useState(false);
    const[goToContact, setGoToContact] = React.useState(false);
    const[goToContactPowerConsumption, setGoToContactPowerConsumption] = React.useState(false);
    if(goToContactHome){
        return <Navigate to = "/"/>
    }
    if(goToContact){
        return <Navigate to = "/AdjustTheLights"/>
    }
    if(goToContactPowerConsumption){
        return <Navigate to = "/PowerConsumption"/>
    }

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
                      <button class="buttonOfWedsite" onClick={() =>
                        setGoToContact(true)
                      }>Adjust the lights</button>
                  </div>  
                  <div class="top-menu">
                      <button class="buttonOfWedsite" onClick={() =>
                        setGoToContactPowerConsumption(true)
                      }>Power consumption</button>
                  </div>
                  <div class="top-menu">
                      <button class="buttonOfWedsite">Notification</button>
                  </div>
              </div>
          </div>
          <div class="circle1"></div>
          <div class="circle2"></div>
      </div>
    );
  }
  
  export default Notification1;