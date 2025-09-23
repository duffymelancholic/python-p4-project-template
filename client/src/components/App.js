import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import FoodInsights from "./FoodInsights";

function App() {
  return (
    <Switch>
      <Route path="/foods">
        <FoodInsights />
      </Route>
      <Route path="/">
        <h1>Project Client</h1>
      </Route>
    </Switch>
  );
}

export default App;
