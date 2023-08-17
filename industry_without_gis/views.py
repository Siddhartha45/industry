import pandas as pd

from django.contrib import messages

from .models import IndustryWithoutGis


def without_gis_data_import(request, file):
    """function for exporting excel data of industries without gis to IndutryWithoutGis model"""
    dtype_mapping = {
                'reg_date': str,
                'industry_reg_no': str,
            }
    df = pd.read_excel(file, dtype=dtype_mapping)
    
    for _, row in df.iterrows():
        industry_data = {}
        
        if 'industry_name' in df.columns:
            industry_name = row['industry_name']
            if pd.notna(industry_name):
                industry_data['industry_name'] = industry_name
            else:                                                   # Excel row not having industry_name value are not entered
                continue
                
        if 'reg_date' in df.columns:
            reg_date = row['reg_date']
            if pd.notna(reg_date):
                try:
                    datetime_obj = pd.to_datetime(reg_date)
                    formatted_reg_date = datetime_obj.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
                    industry_data['reg_date'] = formatted_reg_date
                except ValueError:
                    industry_data['reg_date'] = None
                    
        column_names = ['owner_name', 'industry_address', 'industry_reg_no']
        for column in column_names:
            if column in df.columns:
                value = row[column]
                if pd.notna(value):
                    industry_data[column] = value

        manpower_colums = ['male', 'female']
        for manpower_column in manpower_colums:
            if manpower_column in df.columns:
                manpower_value = row[manpower_column] if pd.notna(row[manpower_column]) else 0
                try:
                    int_manpower_value = int(manpower_value)
                except ValueError:
                    int_manpower_value = 0
                industry_data[manpower_column] = int_manpower_value
        # Stores value of total manpower
        total_manpower = industry_data['male'] + industry_data['female']
        
        capital_columns = ['yearly_capacity', 'fixed_capital', 'current_capital', 'total_capital']
        for capital_column in capital_columns:
            if capital_column in df.columns:
                capital_value = row[capital_column] if pd.notna(row[capital_column]) else 0
                clean_capital_value = str(capital_value).replace(',', '')   # Remove commas from the number
                try:
                    float_capital_value = float(clean_capital_value)
                except ValueError:
                    float_capital_value = 0
                industry_data[capital_column] = float_capital_value
        
        if industry_data:
            industry = IndustryWithoutGis(**industry_data)
            if hasattr(industry, 'total_manpower'):
                industry.total_manpower = total_manpower
            industry.save() 
    return messages.success(request, "The excel data is saved to database.")