```markdown
# Predictive Maintenance System for Oil Refinery

This system was developed to monitor and optimize equipment maintenance operations in an oil refinery. It uses machine learning to predict equipment failures and generate preventive maintenance recommendations, improving the efficiency and safety of operations.

## Features

### 1. **Data Loading and Processing**
   - The system loads operational, maintenance, and failure data from an Excel file with three worksheets:
     - **Operational Data**: Information on equipment performance (temperature, pressure, vibration, etc.).
     - **Maintenance Data**: History of performed maintenance, including replaced parts and maintenance type.
     - **Failure Records**: Data on registered failures, including observed symptoms and identified causes.
   - These data are combined to create a single dataset, where each row represents an entry for a specific equipment, with operational, maintenance, and failure information.

### 2. **Data Preprocessing**
   - Combines data from different sources based on `Equipment ID` and `Date`.
   - Creates new variables useful for analysis, such as:
     - **Failure**: Indicates if a failure symptom has been recorded.
     - **Days since last maintenance**: Calculates the difference in days since the last maintenance.
     - **Accumulated operating hours**: Total sum of operating hours for each piece of equipment.
   - Fills missing values with default information (e.g., "None" for maintenance type).

### 3. **Failure Prediction Model**
   - Uses a **Random Forest** model to predict the probability of failure for each piece of equipment based on operational and maintenance variables.
   - The model is trained with 80% of the data and tested with the remaining 20%, providing an evaluation of its accuracy.
   - Features analyzed by the model include temperature, pressure, vibration, days since the last maintenance, and accumulated operating hours.

### 4. **Alert and Recommendation Generation**
   - The system generates maintenance alerts and recommendations based on the failure probability calculated by the model:
     - **Critical Alerts**: If the failure probability exceeds 70%, a critical alert is generated, recommending an immediate inspection.
     - **Preventive Maintenance Recommendations**: For probabilities between 50% and 70%, the system suggests scheduling preventive maintenance in the coming days.
   - Recommendations include specific actions, such as checking replaced parts, inspecting critical components, and monitoring variables like vibration and temperature.

### 5. **Result Display**
   - Results are presented clearly and objectively, displaying critical alerts and maintenance recommendations for each piece of equipment.
   - Information includes the **equipment name**, **equipment ID**, **failure probability**, and **recommended actions**, with a service priority.

## Technologies Used
- **Pandas**: For data manipulation and analysis.
- **Scikit-learn**: For predictive modeling using the Random Forest algorithm.
- **Excel**: For importing and working with spreadsheet data.

## Benefits
- **Maintenance Optimization**: Anticipating failures before they occur, reducing downtime and increasing operational efficiency.
- **Safety**: Early detection of potentially critical failures helps prevent accidents and equipment damage.
- **Operational Efficiency**: Better allocation of maintenance resources, prioritizing equipment with higher failure risks.

This system can be a powerful tool for refining maintenance processes in an oil refinery, promoting greater safety, cost reduction, and increasing equipment lifespan.
```
