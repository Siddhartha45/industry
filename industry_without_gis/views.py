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
        
        if 'industry_reg_no' in df.columns:
            industry_reg_no = row['industry_reg_no']
            if pd.notna(industry_reg_no):
                industry_data['industry_reg_no'] = industry_reg_no
                
        if 'reg_date' in df.columns:
            reg_date = row['reg_date']
            if pd.notna(reg_date):
                try:
                    datetime_obj = pd.to_datetime(reg_date)
                    formatted_reg_date = datetime_obj.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
                    industry_data['reg_date'] = formatted_reg_date
                except ValueError:
                    industry_data['reg_date'] = None
                    
        if 'owner_name' in df.columns:
            owner_name = row['owner_name']
            if pd.notna(owner_name):
                industry_data['owner_name'] = owner_name
                
        if 'industry_address' in df.columns:
            industry_address = row['industry_address']
            if pd.notna(industry_address):
                industry_data['industry_address'] = industry_address
                
        if 'male' in df.columns:
            male_value = row['male'] if pd.notnull(row['male']) else 0
            try:
                male_value = int(male_value)
            except ValueError:
                male_value = 0
            industry_data['male'] = male_value
        total_manpower = 0
        
        if 'female' in df.columns:
            female_value = row['female'] if pd.notnull(row['female']) else 0
            try:
                female_value = int(female_value)
            except ValueError:
                female_value = 0
            industry_data['female'] = female_value
        
            total_manpower = female_value + male_value
            
        if 'yearly_capacity' in df.columns:
            yearly_capacity_value = row['yearly_capacity'] if pd.notnull(row['yearly_capacity']) else 0
            yearly_capacity_value = str(yearly_capacity_value).replace(',', '')  # Remove commas from the number
            try:
                industry_data['yearly_capacity'] = float(yearly_capacity_value)
            except ValueError:
                industry_data['yearly_capacity'] = 0
        
        if 'fixed_capital' in df.columns:
            fixed_capital_value = row['fixed_capital'] if pd.notnull(row['fixed_capital']) else 0
            fixed_capital_value = str(fixed_capital_value).replace(',', '')  # Remove commas from the number
            try:
                industry_data['fixed_capital'] = float(fixed_capital_value)
            except ValueError:
                industry_data['fixed_capital'] = 0
        
        if 'current_capital' in df.columns:
            current_capital_value = row['current_capital'] if pd.notnull(row['current_capital']) else 0
            current_capital_value = str(current_capital_value).replace(',', '')  # Remove commas from the number
            try:
                industry_data['current_capital'] = float(current_capital_value)   
            except ValueError:
                industry_data['current_capital'] = 0
            
        if 'total_capital' in df.columns:
            total_capital_value = row['total_capital'] if pd.notnull(row['total_capital']) else 0
            total_capital_value = str(total_capital_value).replace(',', '') # Remove commas from the number
            try:
                industry_data['total_capital'] = float(total_capital_value)
            except ValueError:
                industry_data['total_capital'] = 0
        
        if industry_data:
            industry = IndustryWithoutGis(**industry_data)
            if hasattr(industry, 'total_manpower'):
                industry.total_manpower = total_manpower
            industry.save() 
    return messages.success(request, "The excel data is saved to database.")