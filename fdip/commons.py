#choices for selecting districts
DISTRICT = (
    ('KAILALI', 'KAILALI'),
    ('KANCHANPUR', 'KANCHANPUR'),
    ('DADELDHURA', 'DADELDHURA'),
    ('DOTI', 'DOTI'),
    ('ACHHAM', 'ACHHAM'),
    ('BAJURA', 'BAJURA'),
    ('BAJHANG', 'BAJHANG'),
    ('BAITADI', 'BAITADI'),
    ('DARCHULA', 'DARCHULA'),
)

#choices for selecting nature of investment
INVESTMENT_CHOICES = (
    ('MINIATURE', 'लघु (Miniature)'),
    ('DOMESTIC', 'घरेलु (Cottage Industry)'),
    ('SMALL', 'साना (Small)'),
    ('MEDIUM', 'मझौला (Medium)'),
    ('LARGE', 'ठुलो (Large)'),
)

#choices for selecting raw material source
MATERIAL_SOURCE = (
    ('LOCAL', 'स्थानिय (Local)'),
    ('IMPORTED', 'आयातित (Imported)'),
)

#choices for selecting type of product based on industry
TYPE_OF_PRODUCT = (
    ('E', 'उर्जामूलक (Energy)'),
    ('MF', 'उत्पादनमूलक (Manufacturing)'),
    ('AF', 'कृषि तथा वन पैदावारमा आधारित (Agricultural or Forestry based)'),
    ('MI', 'खनिज(Mineral)'),
    ('I', 'पूर्वाधार(Infrastructure)'),
    ('T', 'पर्यटन(Tourism)'),
    ('IC', 'सूचना तथा संचार प्रविधि(Information and Communication)'),
    ('S', 'सेवामूलक(Service)'),
    ('O', 'अन्य(Others)'),
)

#choices for selecting current status
CURRENT_STATUS = (
    ('A', 'चालु(Active)'),
    ('I', 'निष्कृय(Inactive)'),
)

#choices for selecting capacity of industry operation
CAPACITY = (
    ('A', '७०-१००% (70-100%)'),
    ('B', '५०-७०% (50-70%)'),
    ('C', '५०% भन्दा कम (Less than 50%)'),
    ('D', '२५% भन्दा कम (Less than 25%)')
)

#choices for selecting sex
SEX_CHOICES = (
    ('MALE', 'पुरुष (Male)'),
    ('FEMALE', 'महिला (Female)'),
    ('OTHERS', 'अन्य (Others)'),
)

#choices for selecting caste
CASTE_CHOICES = (
    ('DALIT', 'दलित (Dalit)'),
    ('JANAJATI', 'जनजाती (Janajati)'),
    ('OTHERS', 'अन्य (Others)'),
)

#choices for ownership
OWNERSHIP_CHOICES = (
    ('PRIVATE', 'निजी (Private)'),
    ('PARTNERSHIP', 'साझेदारी (Partnership)'),
)