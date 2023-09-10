from industry_without_gis.excel_name import *


sex_mapping = {
    "अन्य": "OTHERS",
    "पुरुष": "MALE",
    "महिला": "FEMALE",
}

caste_mapping = {
    "दलित": "DALIT",
    "जनजाती": "JANAJATI",
    "अन्य": "OTHERS",
}

investment_mapping = {
    "साना": "SMALL",
    "लघु": "MINIATURE",
    "घरेलु": "DOMESTIC",
    "मझौला": "MEDIUM",
    "ठुलो": "LARGE",
}

industry_acc_product_mapping = {
    "उर्जामूलक": "E",
    "उत्पादनमूलक": "MF",
    "कृषि": "AF",
    "खनिज": "MI",
    "निमार्ण": "I",
    "पर्यटन": "T",
    "सूचना": "IC",
    "सेवा": "S",
    "अन्य": "O",
}

current_status_mapping = {
    "सक्रिय": "A",
    "निष्कृय": "I",
}

ownership_mapping = {
    "निजी": "PRIVATE",
    "साझेदारी": "PARTNERSHIP",
}

raw_materials_source_mapping = {
    "स्थानिय": "LOCAL",
    "आयातित": "IMPORTED",
}

current_running_capacity_mapping = {
    "७०-१००%": "A",
    "५०-७०%": "B",
    "५०% भन्दा कम": "C",
    "२५% भन्दा कम": "D",
}

district_mapping = {
    "कैलाली": "KAILALI",
    "कन्चनपुर": "KANCHANPUR",
    "डडेल्धुरा": "DADELDHURA",
    "डोटी": "DOTI",
    "अछाम": "ACHHAM",
    "बाजुरा": "BAJURA",
    "बझांग": "BAJHANG",
    "बैतडी": "BAITADI",
    "दार्चुला": "DARCHULA",
}

local_body_mapping = {
    #Dadeldhura localbodies
    "अमरगढी नगरपालिका": "AMARGADHI",
    "परशुराम नगरपालिका": "PARSURAM",
    "आलिताल गाउँपालिका": "ALITAL",
    "भागेश्वर गाउँपालिका": "BHAGYASWOR",
    "नवदुर्गा गाउँपालिका": "NAVADURGA",
    "अजयमेरु गाउँपालिका": "AJAYMERU",
    "गन्यापधुरा गाउँपालिका": "GANYAPDHURA",
    
    #Darchula localbodies
    "महाकाली नगरपालिका": "MAHAKALI",
    "शैल्यशिखर नगरपालिका": "SALYASIKHAR",
    "मालिकार्जुन गाउँपालिका": "MALIKARJUN",
    "अपिहिमाल गाउँपालिका": "APIHIMAL",
    "दुहुँ गाउँपालिका": "DUNHU",
    "नौगाड गाउँपालिका": "NAUGADH",
    "मार्मा गाउँपालिका": "MARMA",
    "लेकम गाउँपालिका": "LEKAM",
    "ब्याँस गाउँपालिका": "BYAS",
    
    #Baitadi localbodies
    "दशरथचन्द नगरपालिका": "DASHRATHCHAND",
    "पाटन नगरपालिका": "PATAN",
    "मेलौली नगरपालिका": "MELAULI",
    "पुर्चौडी नगरपालिका": "PURCHAUDI",
    "सुर्नया गाउँपालिका": "SUNARYA",
    "सिगास गाउँपालिका": "SIGAS",
    "शिवनाथ गाउँपालिका": "SHIVNATH",
    "पञ्चेश्वर गाउँपालिका": "PARBESHWOR",
    "दोगडाकेदार गाउँपालिका": "DOGDAKEDAR",
    "डीलासैनी गाउँपालिका": "DILASAINI",
    
    #Achham localbodies
    "मंगलसेन नगरपालिका": "MANGALSENA",
    "कमलबजार नगरपालिका": "KAMALBAJAR",
    "साँफेबगर नगरपालिका": "SANFEBAGAR",
    "पन्चदेवल विनायक नगरपालिका": "PANCHADEBAL",
    "चौरपाटी गाउँपालिका": "CHAURPATI",
    "मेल्लेख गाउँपालिका": "MELLEKH",
    "बान्निगढी जयगढ गाउँपालिका": "BATRIGADHI",
    "रामारोशन गाउँपालिका": "RAMAROSAN",
    "ढकारी गाउँपालिका": "DHAKARI",
    "तुर्माखाँद गाउँपालिका": "TURMAKHAND",
    
    #Doti localbodies
    "दिपायल सिलगढी नगरपालिका": "DIPAYAL",
    "शिखर नगरपालिका": "SHIKHAR",
    "पूर्वीचौकी गाउँपालिका": "PURBICHAUKI",
    "बडीकेदार गाउँपालिका": "BADIKEDAR",
    "जोरायल गाउँपालिका": "JORAYAL",
    "सायल गाउँपालिका": "SAYAL",
    "आदर्श गाउँपालिका": "AADARSH",
    "के.आई.सिं. गाउँपालिका": "KIC",
    "बोगटान फुड्सिल गाउँपालिका": "BOGTAN",
    
    #Kailali localbodies
    "धनगढी उपमहानगरपालिका": "DHANGADI",
    "टिकापुर नगरपालिका": "TIKAPUR",
    "घोडाघोडी नगरपालिका": "GHODAGHODI",
    "लम्कीचुहा नगरपालिका": "LAMKICHUHA",
    "भजनी नगरपालिका": "VAJANI",
    "गोदावरी नगरपालिका": "GODAWARI",
    "गौरीगंगा नगरपालिका": "GAURIGANGA",
    "जानकी गाउँपालिका": "JANAKI",
    "बर्दगोरिया गाउँपालिका": "BARDAGORIYA",
    "मोहन्याल गाउँपालिका": "MOHANYAL",
    "कैलारी गाउँपालिका": "KAULARI",
    "जोशीपुर गाउँपालिका": "JOSHIPUR",
    "चुरे गाउँपालिका": "CHURE",
    
    #Bajura localbodies
    "बडीमालिका नगरपालिका": "BADIMALIKA",
    "त्रिवेणी नगरपालिका": "TRIBENI",
    "बुढीगंगा नगरपालिका": "BUDHIGANGA",
    "बुढीनन्दा नगरपालिका": "BUDHINANDA",
    "गौमुल गाउँपालिका": "GAUMUL",
    "जगन्‍नाथ गाउँपालिका": "JAGANNATH",
    "स्वामिकार्तिक खापर गाउँपालिका": "SWAMIKARTIK",
    "खप्तड छेडेदह गाउँपालिका": "KHAPTAD",
    "हिमाली गाउँपालिका": "HIMALI",
    
    #Kanchanpur localbodies
    "भीमदत्त नगरपालिका": "BHIMDATTA",
    "पुर्नवास नगरपालिका": "PURNABAS",
    "वेदकोट नगरपालिका": "BEDKOT",
    "दोधारा चादँनी नगरपालिका": "DODHARA",
    "शुक्लाफाँटा नगरपालिका": "SUKLAPHATA",
    "बेलौरी नगरपालिका": "BELAURI",
    "कृष्णपुर नगरपालिका": "KRISHNAPUR",
    "बेलडाडी गाउँपालिका": "BELDADI",
    "लालझाडी गाउँपालिका": "LALJHADI",
    
    #Bajhang localbodies
    "जयपृथ्वी नगरपालिका": "JAYPRITHVI",
    "बुंगल नगरपालिका": "BUNGAL",
    "तलकोट गाउँपालिका": "TALKOT",
    "मष्टा गाउँपालिका": "MASTA",
    "खप्तडछान्ना गाउँपालिका": "KHAPTADCHATRA",
    "थलारा गाउँपालिका": "THALARA",
    "वित्थडचिर गाउँपालिका": "BITTADCHIR",
    "सूर्मा गाउँपालिका": "SURMA",
    "छबिसपाथिभेरा गाउँपालिका": "CHABBISPATHIVERA",
    "दुर्गाथली गाउँपालिका": "DURGATHALI",
    "केदारस्युँ गाउँपालिका": "KEDARSU",
    "साइपाल गाउँपालिका": "SAIPAL",
}

# Read the Excel file and specify data types 
dtype_mapping = {
    industry_reg_no: str, 
    reg_date: str,
    mobile_number: str, 
    telephone_number: str, 
    sex: str,
    caste: str,
    district: str,
    local_body: str,
    investment: str,
    industry_acc_product: str,
    current_status: str,
    ownership: str,
    raw_material_source: str,
    current_running_capacity: str,
}