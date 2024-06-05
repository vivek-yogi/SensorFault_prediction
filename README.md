# SensorFault_prediction

### 1.Problem statement.

**Data:** Sensor Data

***Problem statement:***

* The system in focus is the Air Pressure system(APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class corresponds to component failures for a specific component of the APS system.The negative class corresponds to trucks with failures for components not related to the APS system.

* The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.

* The total cost of a prediction model the sum of Cost_1 multiplied by the number of instances with type 1 failure and Cost_2 with the number of instances with type 2 failure,resulting in a Total cost. In this case Cost_1 refers to the cost that an unnecessary check needs to be done by an mechanic at a workshop, while Cost_2 refer to the cost of missing a fault which may result to a breakdown.

* Total_cost = Cost_1 * No_Instances + Cost_2 * No_instances.

* It can be observed from above problem statement that we have to reduce the false positive and false negative and more precisly the false negative because cost related to false negative is much higher than cost related to false positive. 
