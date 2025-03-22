import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def load_data_from_excel(file_path):
    operational_data = pd.read_excel(file_path, sheet_name='Operational Data')
    maintenance_data = pd.read_excel(file_path, sheet_name='Maintenance Data')
    failure_records = pd.read_excel(file_path, sheet_name='Occurrence Records')
    
    return operational_data, maintenance_data, failure_records


# Data preprocessing
def preprocess_data(operational_df, maintenance_df, failures_df):
    df = operational_df.merge(maintenance_df, on=['Equipment ID', 'Date'], how='left')
    df = df.merge(failures_df, on=['Equipment ID', 'Date'], how='left')
    
    # Feature engineering
    df['Failure'] = df['Observed Symptom'].notnull().astype(int)
    df['Days Since Last Maintenance'] = df.groupby('Equipment ID')['Date'].diff().dt.days
    df['Cumulative Operating Hours'] = df.groupby('Equipment ID')['Operating Hours'].cumsum()
    df.fillna({'Maintenance Type': 'None', 'Replaced Parts': 'None'}, inplace=True)
    return df


# Train predictive model
def train_predictive_model(df):
    features = ['Temperature (°C)', 'Pressure (bar)', 'Vibration (mm/s)',
                'Days Since Last Maintenance', 'Cumulative Operating Hours']
    target = 'Failure'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    
    # print("Model Evaluation:")
    # print(classification_report(y_test, model.predict(X_test)))
    return model


# Generate recommendations and alerts
def generate_recommendations(df, model):
    alerts = []
    recommendations = []
    
    # Analyze the last 7 days for each equipment
    latest_data = df.groupby('Equipment ID').last().reset_index()
    
    for _, row in latest_data.iterrows():
        X_latest_df = pd.DataFrame(row[features].values.reshape(1, -1), columns=features)
        
        prob_failure = model.predict_proba(X_latest_df)[0][1]

        equipment_name = row['Equipment'] 
        
        if prob_failure > 0.7:
            alerts.append({
                'Equipment ID': row['Equipment ID'],
                'Equipment Name': equipment_name,
                'Failure Probability': f"{prob_failure:.0%}",
                'Alerts': [
                    f"Critical failure probability ({prob_failure:.0%})",
                    f"Expected symptom: {row['Observed Symptom'] or 'Unknown'}"
                ]
            })
            
            maintenance_rec = {
                'Equipment ID': row['Equipment ID'],
                'Equipment Name': equipment_name, 
                'Recommended Actions': [
                    f"Perform immediate inspection within the next 24 hours",
                    f"Check {row['Replaced Parts']}",
                    f"Monitor {row['Failure Cause']}"
                ],
                'Priority': 'High'
            }
            recommendations.append(maintenance_rec)
            
        elif prob_failure > 0.5:
            recommendations.append({
                'Equipment ID': row['Equipment ID'],
                'Equipment Name': equipment_name,
                'Recommended Actions': [
                    f"Schedule preventive maintenance within the next 72 hours",
                    f"Check vibration trend: {row['Vibration (mm/s)']:.1f} mm/s"
                ],
                'Priority': 'Medium'
            })
    
    return alerts, recommendations


if __name__ == "__main__":
    # 1. Load and process data
    file_path = 'Data.xlsx'
    operational_df, maintenance_df, failures_df = load_data_from_excel(file_path)
    processed_df = preprocess_data(operational_df, maintenance_df, failures_df)
    
    # 2. Train the model
    model = train_predictive_model(processed_df)
    
    # 3. Generate alerts and recommendations
    features = ['Temperature (°C)', 'Pressure (bar)', 'Vibration (mm/s)',
                'Days Since Last Maintenance', 'Cumulative Operating Hours']
    alerts, recommendations = generate_recommendations(processed_df, model)
    
    # Display results
    print("\nCRITICAL ALERTS:")
    for alert in alerts:
        print(f"\n[!] ALERT: {alert['Equipment Name']} (Equipment ID {alert['Equipment ID']})")
        for msg in alert['Alerts']:
            print(f"  - {msg}")

    print("\nMAINTENANCE RECOMMENDATIONS:")
    for rec in recommendations:
        print(f"\n[{rec['Priority']}] {rec['Equipment Name']} (Equipment ID {rec['Equipment ID']}):")
        for action in rec['Recommended Actions']:
            print(f"  • {action}")