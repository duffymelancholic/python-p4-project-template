import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import FoodInsights from "./FoodInsights";
import SmartAlerts from "./SmartAlerts";
import Gamification from "./Gamification";
import Education from "./Education";

function App() {
  return (
    <Switch>
      <Route path="/foods">
        <FoodInsights />
      </Route>
      <Route path="/alerts">
        <SmartAlerts />
      </Route>
      <Route path="/gamification">
        <Gamification />
      </Route>
      <Route path="/education">
        <Education />
      </Route>
      <Route path="/">
        <h1>Project Client</h1>
      </Route>
    </Switch>
  );
}

export default App;
