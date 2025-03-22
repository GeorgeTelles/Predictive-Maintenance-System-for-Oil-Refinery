import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def load_data_from_excel(file_path):
    operational_data = pd.read_excel(file_path, sheet_name='Operational Data')
    maintenance_data = pd.read_excel(file_path, sheet_name='Maintenance Data')
    failure_records = pd.read_excel(file_path, sheet_name='Occurrence Records')
    return operational_data, maintenance_data, failure_records

# Function for data preprocessing
def preprocess_data(operational_df, maintenance_df, failures_df):
    df = operational_df.merge(maintenance_df, on=['Equipment ID', 'Date'], how='left')
    df = df.merge(failures_df, on=['Equipment ID', 'Date'], how='left')
    df['Failure'] = df['Observed Symptom'].notnull().astype(int)
    df['Days Since Last Maintenance'] = df.groupby('Equipment ID')['Date'].diff().dt.days
    df['Cumulative Operating Hours'] = df.groupby('Equipment ID')['Operating Hours'].cumsum()
    df.fillna({'Maintenance Type': 'None', 'Replaced Parts': 'None'}, inplace=True)
    return df

def train_predictive_model(df):
    features = ['Temperature (°C)', 'Pressure (bar)', 'Vibration (mm/s)', 
                'Days Since Last Maintenance', 'Cumulative Operating Hours']
    target = 'Failure'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    
    return model

# Generate alerts and recommendations
def generate_recommendations(df, model, features):
    alerts = []
    recommendations = []
    
    latest_data = df.groupby('Equipment ID').last().reset_index()
    
    for _, row in latest_data.iterrows():
        X_latest_df = pd.DataFrame(row[features].values.reshape(1, -1), columns=features)
        
        prob_failure = model.predict_proba(X_latest_df)[0][1]
        
        equipment_name = row['Equipment']
        
        if prob_failure > 0.7:
            alerts.append(f"CRITICAL ALERT: {equipment_name} (ID: {row['Equipment ID']})\n  - Failure probability: {prob_failure:.0%}\n")
            recommendations.append(f"[HIGH] {equipment_name} (ID: {row['Equipment ID']}): Perform immediate inspection within the next 24 hours.")
        elif prob_failure > 0.5:
            recommendations.append(f"[MEDIUM] {equipment_name} (ID: {row['Equipment ID']}): Schedule preventive maintenance within the next 72 hours.")
    
    return alerts, recommendations


def run_scan():
    file_path = 'Data.xlsx'
    
    # Load and process data
    operational_df, maintenance_df, failures_df = load_data_from_excel(file_path)
    processed_df = preprocess_data(operational_df, maintenance_df, failures_df)
    
    # Train the model
    model = train_predictive_model(processed_df)
    
    # Generate alerts and recommendations
    features = ['Temperature (°C)', 'Pressure (bar)', 'Vibration (mm/s)', 
                'Days Since Last Maintenance', 'Cumulative Operating Hours']
    alerts, recommendations = generate_recommendations(processed_df, model, features)
    
    # Display alerts and recommendations
    alert_text.delete(1.0, tk.END) 
    rec_text.delete(1.0, tk.END)    
    
    alert_text.insert(tk.END, "\n".join(alerts))  # Display alerts
    rec_text.insert(tk.END, "\n".join(recommendations))  # Display recommendations

# GUI setup with Tkinter
root = tk.Tk()
root.title("Predictive Maintenance System")
root.geometry("600x600")

# Button
scan_button = tk.Button(root, text="SCAN EQUIPMENT", command=run_scan, height=2, width=40)
scan_button.pack(pady=20)

alert_label = tk.Label(root, text="CRITICAL ALERTS:")
alert_label.pack()
alert_text = scrolledtext.ScrolledText(root, width=70, height=10)
alert_text.pack(pady=10)

rec_label = tk.Label(root, text="MAINTENANCE RECOMMENDATIONS:")
rec_label.pack()
rec_text = scrolledtext.ScrolledText(root, width=70, height=10)
rec_text.pack(pady=10)

root.mainloop()