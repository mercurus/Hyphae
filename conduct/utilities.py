import secrets
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db import models
from django.contrib import messages
from django.shortcuts import redirect


def new_token():
    """For the api"""
    return secrets.token_urlsafe(16)


# def group_required(*group_names):
#     """
#     https://djangosnippets.org/snippets/1703/
#     Decorator requiring membership in at least one of the groups passed in
#     Usage:
#     @group_required('admins','editors')
#     def myview(request, id):
#         ...
#     """
#     def in_groups(u):
#         if u.is_authenticated:
#             if u.is_superuser or bool(u.groups.filter(name__in=group_names)):
#                 return True
#             raise PermissionDenied
#         return False
#     return user_passes_test(in_groups)


def levenshtein_distance(source, target):
    """
    Calculate the number of character insertions, deletions, or substitutions 
    that it takes to transform the string source into target
    https://people.cs.pitt.edu/~kirk/cs1501/assignments/editdistance/Levenshtein%20Distance.htm
    """
    source = source.lower()
    target = target.lower()
    source_len = len(source)
    target_len = len(target)
    if source_len == 0:
        return target_len
    if target_len == 0:
        return source_len

    #initialize
    matrix = [[0 for x in range(target_len + 1)] for y in range(source_len + 1)]
    for i in range(source_len + 1):
        matrix[i][0] = i
    for i in range(target_len + 1):
        matrix[0][i] = i

    #find costs
    for i in range(1, source_len + 1):
        s_char = source[i - 1]
        for j in range(1, target_len + 1):
            t_char = target[j - 1]
            if s_char == t_char:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i-1][j] + 1, matrix[i][j-1] + 1, matrix[i-1][j-1] + cost)

    return matrix[source_len][target_len]


US_STATES = [
    ('AK', 'Alaska'),
    ('AL', 'Alabama'),
    ('AR', 'Arkansas'),
    ('AZ', 'Arizona'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DC', 'District Of Columbia'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('IA', 'Iowa'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('MA', 'Massachusetts'),
    ('MD', 'Maryland'),
    ('ME', 'Maine'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MO', 'Missouri'),
    ('MS', 'Mississippi'),
    ('MT', 'Montana'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('NE', 'Nebraska'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NV', 'Nevada'),
    ('NY', 'New York'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VA', 'Virginia'),
    ('VT', 'Vermont'),
    ('WA', 'Washington'),
    ('WI', 'Wisconsin'),
    ('WV', 'West Virginia'),
    ('WY', 'Wyoming'),
]


US_STATES_TO_ABBR = {
    tup[1]: tup[0]
for tup in US_STATES }


#https://djangosnippets.org/snippets/494/
COUNTRIES = [
    ('USA', 'United States of America'),
    ('CAN', 'Canada'),
    ('MEX', 'Mexico'),
]


#https://djangosnippets.org/snippets/494/
# COUNTRIES = [
#     ('USA', 'United States of America'),
#     ('AFG', 'Afghanistan'),
#     ('ALA', 'Aland Islands'),
#     ('ALB', 'Albania'),
#     ('DZA', 'Algeria'),
#     ('ASM', 'American Samoa'),
#     ('AND', 'Andorra'),
#     ('AGO', 'Angola'),
#     ('AIA', 'Anguilla'),
#     ('ATA', 'Antarctica'),
#     ('ATG', 'Antigua and Barbuda'),
#     ('ARG', 'Argentina'),
#     ('ARM', 'Armenia'),
#     ('ABW', 'Aruba'),
#     ('AUS', 'Australia'),
#     ('AUT', 'Austria'),
#     ('AZE', 'Azerbaijan'),
#     ('BHS', 'Bahamas'),
#     ('BHR', 'Bahrain'),
#     ('BGD', 'Bangladesh'),
#     ('BRB', 'Barbados'),
#     ('BLR', 'Belarus'),
#     ('BEL', 'Belgium'),
#     ('BLZ', 'Belize'),
#     ('BEN', 'Benin'),
#     ('BMU', 'Bermuda'),
#     ('BTN', 'Bhutan'),
#     ('BOL', 'Bolivia'),
#     ('BES', 'Bonaire, Sint Eustatius and Saba'),
#     ('BIH', 'Bosnia and Herzegovina'),
#     ('BWA', 'Botswana'),
#     ('BVT', 'Bouvet Island'),
#     ('BRA', 'Brazil'),
#     ('IOT', 'British Indian Ocean Territory'),
#     ('BRN', 'Brunei Darussalam'),
#     ('BGR', 'Bulgaria'),
#     ('BFA', 'Burkina Faso'),
#     ('BDI', 'Burundi'),
#     ('CPV', 'Cabo Verde'),
#     ('KHM', 'Cambodia'),
#     ('CMR', 'Cameroon'),
#     ('CAN', 'Canada'),
#     ('CYM', 'Cayman Islands'),
#     ('CAF', 'Central African Republic'),
#     ('TCD', 'Chad'),
#     ('CHL', 'Chile'),
#     ('CHN', 'China'),
#     ('CXR', 'Christmas Island'),
#     ('CCK', 'Cocos (Keeling) Islands'),
#     ('COL', 'Colombia'),
#     ('COM', 'Comoros'),
#     ('COD', 'Congo (the Democratic Republic of the)'),
#     ('COG', 'Congo'),
#     ('COK', 'Cook Islands'),
#     ('CRI', 'Costa Rica'),
#     ('HRV', 'Croatia'),
#     ('CUB', 'Cuba'),
#     ('CUW', 'Curaçao'),
#     ('CYP', 'Cyprus'),
#     ('CZE', 'Czechia'),
#     ('CIV', 'Côte d\'Ivoire'),
#     ('DNK', 'Denmark'),
#     ('DJI', 'Djibouti'),
#     ('DMA', 'Dominica'),
#     ('DOM', 'Dominican Republic'),
#     ('ECU', 'Ecuador'),
#     ('EGY', 'Egypt'),
#     ('SLV', 'El Salvador'),
#     ('GNQ', 'Equatorial Guinea'),
#     ('ERI', 'Eritrea'),
#     ('EST', 'Estonia'),
#     ('SWZ', 'Eswatini'),
#     ('ETH', 'Ethiopia'),
#     ('FLK', 'Falkland Islands [Malvinas]'),
#     ('FRO', 'Faroe Islands'),
#     ('FJI', 'Fiji'),
#     ('FIN', 'Finland'),
#     ('FRA', 'France'),
#     ('GUF', 'French Guiana'),
#     ('PYF', 'French Polynesia'),
#     ('ATF', 'French Southern Territories'),
#     ('GAB', 'Gabon'),
#     ('GMB', 'Gambia'),
#     ('GEO', 'Georgia'),
#     ('DEU', 'Germany'),
#     ('GHA', 'Ghana'),
#     ('GIB', 'Gibraltar'),
#     ('GRC', 'Greece'),
#     ('GRL', 'Greenland'),
#     ('GRD', 'Grenada'),
#     ('GLP', 'Guadeloupe'),
#     ('GUM', 'Guam'),
#     ('GTM', 'Guatemala'),
#     ('GGY', 'Guernsey'),
#     ('GIN', 'Guinea'),
#     ('GNB', 'Guinea-Bissau'),
#     ('GUY', 'Guyana'),
#     ('HTI', 'Haiti'),
#     ('HMD', 'Heard Island and McDonald Islands'),
#     ('VAT', 'Holy See'),
#     ('HND', 'Honduras'),
#     ('HKG', 'Hong Kong'),
#     ('HUN', 'Hungary'),
#     ('ISL', 'Iceland'),
#     ('IND', 'India'),
#     ('IDN', 'Indonesia'),
#     ('IRN', 'Iran (Islamic Republic of)'),
#     ('IRQ', 'Iraq'),
#     ('IRL', 'Ireland'),
#     ('IMN', 'Isle of Man'),
#     ('ISR', 'Israel'),
#     ('ITA', 'Italy'),
#     ('JAM', 'Jamaica'),
#     ('JPN', 'Japan'),
#     ('JEY', 'Jersey'),
#     ('JOR', 'Jordan'),
#     ('KAZ', 'Kazakhstan'),
#     ('KEN', 'Kenya'),
#     ('KIR', 'Kiribati'),
#     ('PRK', 'Korea (the Democratic People\'s Republic of)'),
#     ('KOR', 'Korea (the Republic of)'),
#     ('KWT', 'Kuwait'),
#     ('KGZ', 'Kyrgyzstan'),
#     ('LAO', 'Lao People\'s Democratic Republic'),
#     ('LVA', 'Latvia'),
#     ('LBN', 'Lebanon'),
#     ('LSO', 'Lesotho'),
#     ('LBR', 'Liberia'),
#     ('LBY', 'Libya'),
#     ('LIE', 'Liechtenstein'),
#     ('LTU', 'Lithuania'),
#     ('LUX', 'Luxembourg'),
#     ('MAC', 'Macao'),
#     ('MDG', 'Madagascar'),
#     ('MWI', 'Malawi'),
#     ('MYS', 'Malaysia'),
#     ('MDV', 'Maldives'),
#     ('MLI', 'Mali'),
#     ('MLT', 'Malta'),
#     ('MHL', 'Marshall Islands'),
#     ('MTQ', 'Martinique'),
#     ('MRT', 'Mauritania'),
#     ('MUS', 'Mauritius'),
#     ('MYT', 'Mayotte'),
#     ('MEX', 'Mexico'),
#     ('FSM', 'Micronesia (Federated States of)'),
#     ('MDA', 'Moldova (the Republic of)'),
#     ('MCO', 'Monaco'),
#     ('MNG', 'Mongolia'),
#     ('MNE', 'Montenegro'),
#     ('MSR', 'Montserrat'),
#     ('MAR', 'Morocco'),
#     ('MOZ', 'Mozambique'),
#     ('MMR', 'Myanmar'),
#     ('NAM', 'Namibia'),
#     ('NRU', 'Nauru'),
#     ('NPL', 'Nepal'),
#     ('NLD', 'Netherlands'),
#     ('NCL', 'New Caledonia'),
#     ('NZL', 'New Zealand'),
#     ('NIC', 'Nicaragua'),
#     ('NER', 'Niger'),
#     ('NGA', 'Nigeria'),
#     ('NIU', 'Niue'),
#     ('NFK', 'Norfolk Island'),
#     ('MNP', 'Northern Mariana Islands'),
#     ('NOR', 'Norway'),
#     ('OMN', 'Oman'),
#     ('PAK', 'Pakistan'),
#     ('PLW', 'Palau'),
#     ('PSE', 'Palestine, State of'),
#     ('PAN', 'Panama'),
#     ('PNG', 'Papua New Guinea'),
#     ('PRY', 'Paraguay'),
#     ('PER', 'Peru'),
#     ('PHL', 'Philippines'),
#     ('PCN', 'Pitcairn'),
#     ('POL', 'Poland'),
#     ('PRT', 'Portugal'),
#     ('PRI', 'Puerto Rico'),
#     ('QAT', 'Qatar'),
#     ('MKD', 'Republic of North Macedonia'),
#     ('ROU', 'Romania'),
#     ('RUS', 'Russian Federation'),
#     ('RWA', 'Rwanda'),
#     ('BLM', 'Saint Barthélemy'),
#     ('SHN', 'Saint Helena, Ascension and Tristan da Cunha'),
#     ('KNA', 'Saint Kitts and Nevis'),
#     ('LCA', 'Saint Lucia'),
#     ('MAF', 'Saint Martin (French part)'),
#     ('SPM', 'Saint Pierre and Miquelon'),
#     ('VCT', 'Saint Vincent and the Grenadines'),
#     ('WSM', 'Samoa'),
#     ('SMR', 'San Marino'),
#     ('STP', 'Sao Tome and Principe'),
#     ('SAU', 'Saudi Arabia'),
#     ('SEN', 'Senegal'),
#     ('SRB', 'Serbia'),
#     ('SYC', 'Seychelles'),
#     ('SLE', 'Sierra Leone'),
#     ('SGP', 'Singapore'),
#     ('SXM', 'Sint Maarten (Dutch part)'),
#     ('SVK', 'Slovakia'),
#     ('SVN', 'Slovenia'),
#     ('SLB', 'Solomon Islands'),
#     ('SOM', 'Somalia'),
#     ('ZAF', 'South Africa'),
#     ('SGS', 'South Georgia and the South Sandwich Islands'),
#     ('SSD', 'South Sudan'),
#     ('ESP', 'Spain'),
#     ('LKA', 'Sri Lanka'),
#     ('SDN', 'Sudan'),
#     ('SUR', 'Suriname'),
#     ('SJM', 'Svalbard and Jan Mayen'),
#     ('SWE', 'Sweden'),
#     ('CHE', 'Switzerland'),
#     ('SYR', 'Syrian Arab Republic'),
#     ('TWN', 'Taiwan (Province of China)'),
#     ('TJK', 'Tajikistan'),
#     ('TZA', 'Tanzania, United Republic of'),
#     ('THA', 'Thailand'),
#     ('TLS', 'Timor-Leste'),
#     ('TGO', 'Togo'),
#     ('TKL', 'Tokelau'),
#     ('TON', 'Tonga'),
#     ('TTO', 'Trinidad and Tobago'),
#     ('TUN', 'Tunisia'),
#     ('TUR', 'Turkey'),
#     ('TKM', 'Turkmenistan'),
#     ('TCA', 'Turks and Caicos Islands'),
#     ('TUV', 'Tuvalu'),
#     ('UGA', 'Uganda'),
#     ('UKR', 'Ukraine'),
#     ('ARE', 'United Arab Emirates'),
#     ('GBR', 'United Kingdom of Great Britain and Northern Ireland'),
#     ('UMI', 'United States Minor Outlying Islands'),
#     ('URY', 'Uruguay'),
#     ('UZB', 'Uzbekistan'),
#     ('VUT', 'Vanuatu'),
#     ('VEN', 'Venezuela (Bolivarian Republic of)'),
#     ('VNM', 'Viet Nam'),
#     ('VGB', 'Virgin Islands (British)'),
#     ('VIR', 'Virgin Islands (U.S.)'),
#     ('WLF', 'Wallis and Futuna'),
#     ('ESH', 'Western Sahara'),
#     ('YEM', 'Yemen'),
#     ('ZMB', 'Zambia'),
#     ('ZWE', 'Zimbabwe'),
# ]
