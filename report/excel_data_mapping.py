sex_mapping = {
    "Others": "OTHERS",
    "Male": "MALE",
    "Female": "FEMALE",
}

caste_mapping = {
    "Dalit": "DALIT",
    "Janajati": "JANAJATI",
    "Others": "OTHERS",
}

investment_mapping = {
    "Small": "SMALL",
    "Micro": "MINIATURE",
    "Cottage": "DOMESTIC",
    "Medium": "MEDIUM",
    "Large": "LARGE",
}

industry_acc_product_mapping = {
    "Energy": "E",
    "Manufacturing": "MF",
    "Agricultural": "AF",
    "Mineral": "MI",
    "Infrastructure": "I",
    "Tourism": "T",
    "IC": "IC",
    "Service": "S",
    "Others": "O",
}

current_status_mapping = {
    "Active": "A",
    "Inactive": "I",
}

ownership_mapping = {
    "Private": "PRIVATE",
    "Partnership": "PARTNERSHIP",
}

raw_materials_source_mapping = {
    "Local": "LOCAL",
    "Imported": "IMPORTED",
}

current_running_capacity_mapping = {
    "70-100": "A",
    "50-70": "B",
    "50": "C",
    "25": "D",
}

district_mapping = {
    "Kailali": "KAILALI",
    "Kanchanpur": "KANCHANPUR",
    "Dadeldhura": "DADELDHURA",
    "Doti": "DOTI",
    "Achham": "ACHHAM",
    "Bajura": "BAJURA",
    "Bajhang": "BAJHANG",
    "Baitadi": "BAITADI",
    "Darchula": "DARCHULA",
}

local_body_mapping = {
    "Apihimal": "APIHIMAL",
    "Kedarseu": "KEDARSU",
    "Bhimdatta": "BHIMDATTA",
    "Bithadchir": "BITTADCHIR",
    "Bungal": "BUNGAL",
    "Chabispathivera": "CHABBISPATHIVERA",
    "Chaurpati": "CHAURPATI",
    "Dhakari": "DHAKARI",
    "Dhangadhi": "DHANGADI",
    "Durgathali": "DURGATHALI",
    "JayaPrithivi": "JAYPRITHVI",
    "Khaptadchhanna": "KHAPTADCHATRA",
    "Laljhadi": "LALJHADI",
    "Lamkichuha": "LAMKICHUHA",
    "Masta": "MASTA",
    "SaiPaal": "SAIPAL",
    "Shuklaphanta": "SUKLAPHATA",
    "Surma": "SURMA",
    "Talkot": "TALKOT",
    "Thalara": "THALARA",
}

# Read the Excel file and specify data types 
dtype_mapping = {
    'industry_reg_no': str, 
    'reg_date': str,
    'mobile_number': str, 
    'telephone_number': str, 
    'sex': str,
    'caste': str,
    'district': str,
    'local_body': str,
    'investment': str,
    'industry_acc_product': str,
    'current_status': str,
    'ownership': str,
    'raw_materials_source': str,
    'current_running_capacity': str,
}