import React from "react";
import { Navigate } from "react-router-dom";
import './PowerConsumption.css';


function PowerConsumption() {
    const[goToContactHome, setGoToContactHome] = React.useState(false);
    const[goToContact, setGoToContact] = React.useState(false);
    const[goToContactNotification1, setGoToContactNotification1] = React.useState(false);
    const[goToContactDay, setGoToContactDay] = React.useState(false);
    const[goToContactMonth, setGoToContactMonth] = React.useState(false);
    if(goToContactHome){
        return <Navigate to = "/"/>
    }
    if(goToContact){
        return <Navigate to = "/AdjustTheLights"/>
    }
    if(goToContactNotification1){
        return <Navigate to = "/Notification1"/>
    }
    if(goToContactDay){
        return <Navigate to = "/barChartOfDay"/>
    }
    if(goToContactMonth){
        return <Navigate to = "/barChartOfMonth"/>
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
                      <button class="buttonOfWedsite">Power consumption</button>
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
          <div class="buttonMain1">
            <button class="buttonOnOff3" onClick={() =>
                        setGoToContactMonth(true)
                      }>Month</button>
            <button class="buttonOnOff4" onClick={() =>
                        setGoToContactDay(true)
                      }>Day</button>
          </div>
          <div class="enterDate">
          <form>
              <label>
                Enter:
                <input type="date" name="name" class="input1"/>
              </label>
              <input type="submit" value="Submit" class="input2"/>
            </form>
          </div>
      </div>
    );
  }
  
  export default PowerConsumption;