import pandas as pd
import random

def generate_dates(start, end):
    return pd.date_range(start, end, freq='D')

# Possible equipment
equipment_names = [
    'Centrifugal Pump',
    'Gas Compressor',
    'Heat Exchanger',
    'Steam Turbine',
    'Control Valve',
    'Refrigeration System',
    'Particle Abrasion System',
    'Catalytic Cracking Furnace',
    'Hydrogen Refiner',
    'Vacuum Distillation Unit'
]

def generate_equipment():
    equipment_list = []
    for i in range(1, 51):
        name = equipment_names[(i - 1) % len(equipment_names)] 
        equipment_list.append({'ID': i, 'Name': name})
    return equipment_list


# Generate operational data
def generate_operational_data(equipment_list):
    data = []
    for date in generate_dates('2024-01-01', '2024-06-01'):
        equipment = random.choice(equipment_list)
        temperature = round(random.uniform(70, 130), 2)
        pressure = round(random.uniform(8, 16), 2)
        vibration = round(random.uniform(1, 3), 2)
        operating_hours = random.randint(16, 24)
        energy_consumption = random.randint(300, 500)
        data.append([date, equipment['ID'], equipment['Name'], temperature, pressure, vibration, operating_hours, energy_consumption])
    return pd.DataFrame(data, columns=['Date', 'Equipment ID', 'Equipment', 'Temperature (°C)', 'Pressure (bar)', 'Vibration (mm/s)', 'Operating Hours', 'Energy Consumption (kWh)'])

# Generate maintenance data
def generate_maintenance_data(equipment_list):
    maintenance_types = ['Preventive', 'Corrective']
    replaced_parts = ['Bearing', 'Valve', 'Filter', 'Heat Exchanger', 'Compressor']
    failure_causes = ['Natural wear', 'Electrical failure', 'Leakage', 'Mechanical issue', 'N/A']
    data = []
    for date in generate_dates('2024-01-01', '2024-12-31'):
        equipment = random.choice(equipment_list)
        maintenance_type = random.choice(maintenance_types)
        parts = random.sample(replaced_parts, k=random.randint(1, 3))
        cause = random.choice(failure_causes)
        data.append([date, equipment['ID'], equipment['Name'], maintenance_type, ', '.join(parts), cause])
    return pd.DataFrame(data, columns=['Date', 'Equipment ID', 'Equipment', 'Maintenance Type', 'Replaced Parts', 'Failure Cause'])


# Generate occurrence records data
def generate_occurrence_data(equipment_list):
    parts = ['Bearing', 'Oil Filter', 'Pressure Valve', 'Heat Exchanger', 'Flow Control Valve']
    symptoms = ['Abnormal vibration', 'Pressure loss', 'Lack of pressure', 'Fluid leakage', 'Oil flow anomaly', 'Stopped working']
    data = []
    for date in generate_dates('2024-01-01', '2024-12-31'):
        equipment = random.choice(equipment_list)
        part = random.choice(parts)
        symptom = random.choice(symptoms)
        
        # Class 1 represents failure, if the symptom is "Stopped working", the class will be 1
        failure_class = 1 if symptom == 'Stopped working' else 0
        
        data.append([date, equipment['ID'], equipment['Name'], part, symptom, failure_class])
    
    return pd.DataFrame(data, columns=['Date', 'Equipment ID', 'Equipment', 'Part', 'Observed Symptom', 'Failure Class'])

# Generate the equipment list
equipment_list = generate_equipment()

# Generate the data
operational_data = generate_operational_data(equipment_list)
maintenance_data = generate_maintenance_data(equipment_list)
occurrence_data = generate_occurrence_data(equipment_list)

print(operational_data.head())
print(maintenance_data.head())
print(occurrence_data.head())

# Save
with pd.ExcelWriter('Data.xlsx') as writer:
    operational_data.to_excel(writer, sheet_name='Operational Data', index=False)
    maintenance_data.to_excel(writer, sheet_name='Maintenance Data', index=False)
    occurrence_data.to_excel(writer, sheet_name='Occurrence Records', index=False)