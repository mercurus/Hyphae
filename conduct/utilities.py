import secrets
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db import models
from django.contrib import messages
from django.shortcuts import redirect


def template_variables_context(request):
    """Context processor for global variable colors and icons"""
    return {
        # 'submit_color': 'light-green-9',
        # 'navbar_hilight': 'orange-6',
        'icon_check': 'fa fa-check',
        'icon_folk': 'fa fa-user-friends',
        'icon_topic': 'fas fa-globe',
        'icon_morph': 'fa fa-puzzle-piece',
        'icon_note': 'fa fa-paper-plane',
        'icon_search': 'fa fa-search',
        'icon_': 'fa fa-',
    }


class Enumeration(object):
    """
    https://djangosnippets.org/snippets/1647/
    A small helper class for more readable enumerations,
    and compatible with Django's choice convention.
    You may just pass the instance of this class as the choices
    argument of model/form fields.

    Example:
    MY_ENUM = Enumeration([
        (database_val, code_val, verbose_val),
        (100, 'MY_NAME', 'My verbose name'),
        (200, 'MY_AGE', 'My verbose age'),
    ])
    assert MY_ENUM.MY_AGE == 100
    assert MY_ENUM[1] == (200, 'My verbose age')
    """

    def __init__(self, enum_list):
        self.enum_list = [ (item[0], item[2]) for item in enum_list ]
        #code value to db value (MY_ENUM.MY_NAME == 100)
        self.enum_dict = { item[1]: item[0] for item in enum_list }
        #db value to verbose value (MY_ENUM['100'] == 'My verbose name')
        self.enum_dict.update({ str(item[0]): item[2] for item in enum_list })

    def __contains__(self, val):
        return val in self.enum_dict

    def __len__(self):
        return len(self.enum_list)

    def __getitem__(self, val):
        if isinstance(val, str):
            return self.enum_dict[val]
        elif isinstance(val, int):
            return self.enum_list[val]

    def __getattr__(self, name):
        return self.enum_dict[name]

    def __iter__(self):
        return self.enum_list.__iter__()

    # #Return the description text for the given key
    # def get_text(self, key):
    #     for tupl in self.enum_list:
    #         if key == tupl[0]:
    #             return tupl[1]
    #     return ''

    # #return the enums but include the enum value in the display text
    # def val_in_text(self):
    #     return [ (tupl[0], tupl[0] + ' - ' + tupl[1]) for tupl in self.enum_list ]

    # #return enums with a blank first value
    # def with_blank(self):
    #     enums_with_blank = [('', '---------')]
    #     enums_with_blank.extend(self.enum_list)
    #     return enums_with_blank


class EnumField(models.CharField):
    """
    This is to create a CharField that knows how to translate its own enum/choice value
    into the full text in a template. Set its kwarg 'enum' to an Enumeration.
    Used in tandem with template_utilities.readable
    """
    def __init__(self, *args, **kwargs):
        if 'enum' in kwargs: #necessary during makemigrations I guess?
            self.enum = kwargs['enum'] #should be an Enumeration
            del kwargs['enum'] #Django won't accept this kwarg so we delete it
            kwargs['choices'] = self.enum.enum_list
        super().__init__(*args, **kwargs)

    def readable(self, val):
        if val in self.enum:
            return self.enum[val]
        return ''


def new_token():
    """For the api"""
    return secrets.token_urlsafe(16)


def query_from_form(search_fields, form):
    """
    https://docs.djangoproject.com/en/3.0/topics/db/queries/#complex-lookups-with-q-objects
    search_fields should be a dictionary where
    the key is the filter (alias__icontains) and
    the value is the model field name (alias) and
    form should be the Form containing the search parameters
    """
    query = { k: form[v].value() for k, v in search_fields.items() if form[v].value() }
    if 'alias__icontains' in query and 'name__icontains' in query:
        query_alias = query.copy()
        del query_alias['name__icontains']
        del query['alias__icontains']
        return Q(**query) | Q(**query_alias) #search by name OR alias
    return Q(**query)


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


US_STATES = Enumeration([
    ('AK', 'AK', 'Alaska'),
    ('AL', 'AL', 'Alabama'),
    ('AR', 'AR', 'Arkansas'),
    ('AZ', 'AZ', 'Arizona'),
    ('CA', 'CA', 'California'),
    ('CO', 'CO', 'Colorado'),
    ('CT', 'CT', 'Connecticut'),
    ('DC', 'DC', 'District Of Columbia'),
    ('DE', 'DE', 'Delaware'),
    ('FL', 'FL', 'Florida'),
    ('GA', 'GA', 'Georgia'),
    ('HI', 'HI', 'Hawaii'),
    ('IA', 'IA', 'Iowa'),
    ('ID', 'ID', 'Idaho'),
    ('IL', 'IL', 'Illinois'),
    ('IN', 'IN', 'Indiana'),
    ('KS', 'KS', 'Kansas'),
    ('KY', 'KY', 'Kentucky'),
    ('LA', 'LA', 'Louisiana'),
    ('MA', 'MA', 'Massachusetts'),
    ('MD', 'MD', 'Maryland'),
    ('ME', 'ME', 'Maine'),
    ('MI', 'MI', 'Michigan'),
    ('MN', 'MN', 'Minnesota'),
    ('MO', 'MO', 'Missouri'),
    ('MS', 'MS', 'Mississippi'),
    ('MT', 'MT', 'Montana'),
    ('NC', 'NC', 'North Carolina'),
    ('ND', 'ND', 'North Dakota'),
    ('NE', 'NE', 'Nebraska'),
    ('NH', 'NH', 'New Hampshire'),
    ('NJ', 'NJ', 'New Jersey'),
    ('NM', 'NM', 'New Mexico'),
    ('NV', 'NV', 'Nevada'),
    ('NY', 'NY', 'New York'),
    ('OH', 'OH', 'Ohio'),
    ('OK', 'OK', 'Oklahoma'),
    ('OR', 'OR', 'Oregon'),
    ('PA', 'PA', 'Pennsylvania'),
    ('RI', 'RI', 'Rhode Island'),
    ('SC', 'SC', 'South Carolina'),
    ('SD', 'SD', 'South Dakota'),
    ('TN', 'TN', 'Tennessee'),
    ('TX', 'TX', 'Texas'),
    ('UT', 'UT', 'Utah'),
    ('VA', 'VA', 'Virginia'),
    ('VT', 'VT', 'Vermont'),
    ('WA', 'WA', 'Washington'),
    ('WI', 'WI', 'Wisconsin'),
    ('WV', 'WV', 'West Virginia'),
    ('WY', 'WY', 'Wyoming'),
])


#https://djangosnippets.org/snippets/494/
COUNTRIES = Enumeration([
    ('USA', 'USA', 'United States of America'),
    ('CAN', 'CAN', 'Canada'),
    ('MEX', 'MEX', 'Mexico'),
])



#https://djangosnippets.org/snippets/494/
# COUNTRIES = Enumeration([
#     ('USA', 'USA', 'United States of America'),
#     ('AFG', 'AFG', 'Afghanistan'),
#     ('ALA', 'ALA', 'Aland Islands'),
#     ('ALB', 'ALB', 'Albania'),
#     ('DZA', 'DZA', 'Algeria'),
#     ('ASM', 'ASM', 'American Samoa'),
#     ('AND', 'AND', 'Andorra'),
#     ('AGO', 'AGO', 'Angola'),
#     ('AIA', 'AIA', 'Anguilla'),
#     ('ATA', 'ATA', 'Antarctica'),
#     ('ATG', 'ATG', 'Antigua and Barbuda'),
#     ('ARG', 'ARG', 'Argentina'),
#     ('ARM', 'ARM', 'Armenia'),
#     ('ABW', 'ABW', 'Aruba'),
#     ('AUS', 'AUS', 'Australia'),
#     ('AUT', 'AUT', 'Austria'),
#     ('AZE', 'AZE', 'Azerbaijan'),
#     ('BHS', 'BHS', 'Bahamas'),
#     ('BHR', 'BHR', 'Bahrain'),
#     ('BGD', 'BGD', 'Bangladesh'),
#     ('BRB', 'BRB', 'Barbados'),
#     ('BLR', 'BLR', 'Belarus'),
#     ('BEL', 'BEL', 'Belgium'),
#     ('BLZ', 'BLZ', 'Belize'),
#     ('BEN', 'BEN', 'Benin'),
#     ('BMU', 'BMU', 'Bermuda'),
#     ('BTN', 'BTN', 'Bhutan'),
#     ('BOL', 'BOL', 'Bolivia'),
#     ('BES', 'BES', 'Bonaire, Sint Eustatius and Saba'),
#     ('BIH', 'BIH', 'Bosnia and Herzegovina'),
#     ('BWA', 'BWA', 'Botswana'),
#     ('BVT', 'BVT', 'Bouvet Island'),
#     ('BRA', 'BRA', 'Brazil'),
#     ('IOT', 'IOT', 'British Indian Ocean Territory'),
#     ('BRN', 'BRN', 'Brunei Darussalam'),
#     ('BGR', 'BGR', 'Bulgaria'),
#     ('BFA', 'BFA', 'Burkina Faso'),
#     ('BDI', 'BDI', 'Burundi'),
#     ('CPV', 'CPV', 'Cabo Verde'),
#     ('KHM', 'KHM', 'Cambodia'),
#     ('CMR', 'CMR', 'Cameroon'),
#     ('CAN', 'CAN', 'Canada'),
#     ('CYM', 'CYM', 'Cayman Islands'),
#     ('CAF', 'CAF', 'Central African Republic'),
#     ('TCD', 'TCD', 'Chad'),
#     ('CHL', 'CHL', 'Chile'),
#     ('CHN', 'CHN', 'China'),
#     ('CXR', 'CXR', 'Christmas Island'),
#     ('CCK', 'CCK', 'Cocos (Keeling) Islands'),
#     ('COL', 'COL', 'Colombia'),
#     ('COM', 'COM', 'Comoros'),
#     ('COD', 'COD', 'Congo (the Democratic Republic of the)'),
#     ('COG', 'COG', 'Congo'),
#     ('COK', 'COK', 'Cook Islands'),
#     ('CRI', 'CRI', 'Costa Rica'),
#     ('HRV', 'HRV', 'Croatia'),
#     ('CUB', 'CUB', 'Cuba'),
#     ('CUW', 'CUW', 'Curaçao'),
#     ('CYP', 'CYP', 'Cyprus'),
#     ('CZE', 'CZE', 'Czechia'),
#     ('CIV', 'CIV', 'Côte d\'Ivoire'),
#     ('DNK', 'DNK', 'Denmark'),
#     ('DJI', 'DJI', 'Djibouti'),
#     ('DMA', 'DMA', 'Dominica'),
#     ('DOM', 'DOM', 'Dominican Republic'),
#     ('ECU', 'ECU', 'Ecuador'),
#     ('EGY', 'EGY', 'Egypt'),
#     ('SLV', 'SLV', 'El Salvador'),
#     ('GNQ', 'GNQ', 'Equatorial Guinea'),
#     ('ERI', 'ERI', 'Eritrea'),
#     ('EST', 'EST', 'Estonia'),
#     ('SWZ', 'SWZ', 'Eswatini'),
#     ('ETH', 'ETH', 'Ethiopia'),
#     ('FLK', 'FLK', 'Falkland Islands [Malvinas]'),
#     ('FRO', 'FRO', 'Faroe Islands'),
#     ('FJI', 'FJI', 'Fiji'),
#     ('FIN', 'FIN', 'Finland'),
#     ('FRA', 'FRA', 'France'),
#     ('GUF', 'GUF', 'French Guiana'),
#     ('PYF', 'PYF', 'French Polynesia'),
#     ('ATF', 'ATF', 'French Southern Territories'),
#     ('GAB', 'GAB', 'Gabon'),
#     ('GMB', 'GMB', 'Gambia'),
#     ('GEO', 'GEO', 'Georgia'),
#     ('DEU', 'DEU', 'Germany'),
#     ('GHA', 'GHA', 'Ghana'),
#     ('GIB', 'GIB', 'Gibraltar'),
#     ('GRC', 'GRC', 'Greece'),
#     ('GRL', 'GRL', 'Greenland'),
#     ('GRD', 'GRD', 'Grenada'),
#     ('GLP', 'GLP', 'Guadeloupe'),
#     ('GUM', 'GUM', 'Guam'),
#     ('GTM', 'GTM', 'Guatemala'),
#     ('GGY', 'GGY', 'Guernsey'),
#     ('GIN', 'GIN', 'Guinea'),
#     ('GNB', 'GNB', 'Guinea-Bissau'),
#     ('GUY', 'GUY', 'Guyana'),
#     ('HTI', 'HTI', 'Haiti'),
#     ('HMD', 'HMD', 'Heard Island and McDonald Islands'),
#     ('VAT', 'VAT', 'Holy See'),
#     ('HND', 'HND', 'Honduras'),
#     ('HKG', 'HKG', 'Hong Kong'),
#     ('HUN', 'HUN', 'Hungary'),
#     ('ISL', 'ISL', 'Iceland'),
#     ('IND', 'IND', 'India'),
#     ('IDN', 'IDN', 'Indonesia'),
#     ('IRN', 'IRN', 'Iran (Islamic Republic of)'),
#     ('IRQ', 'IRQ', 'Iraq'),
#     ('IRL', 'IRL', 'Ireland'),
#     ('IMN', 'IMN', 'Isle of Man'),
#     ('ISR', 'ISR', 'Israel'),
#     ('ITA', 'ITA', 'Italy'),
#     ('JAM', 'JAM', 'Jamaica'),
#     ('JPN', 'JPN', 'Japan'),
#     ('JEY', 'JEY', 'Jersey'),
#     ('JOR', 'JOR', 'Jordan'),
#     ('KAZ', 'KAZ', 'Kazakhstan'),
#     ('KEN', 'KEN', 'Kenya'),
#     ('KIR', 'KIR', 'Kiribati'),
#     ('PRK', 'PRK', 'Korea (the Democratic People\'s Republic of)'),
#     ('KOR', 'KOR', 'Korea (the Republic of)'),
#     ('KWT', 'KWT', 'Kuwait'),
#     ('KGZ', 'KGZ', 'Kyrgyzstan'),
#     ('LAO', 'LAO', 'Lao People\'s Democratic Republic'),
#     ('LVA', 'LVA', 'Latvia'),
#     ('LBN', 'LBN', 'Lebanon'),
#     ('LSO', 'LSO', 'Lesotho'),
#     ('LBR', 'LBR', 'Liberia'),
#     ('LBY', 'LBY', 'Libya'),
#     ('LIE', 'LIE', 'Liechtenstein'),
#     ('LTU', 'LTU', 'Lithuania'),
#     ('LUX', 'LUX', 'Luxembourg'),
#     ('MAC', 'MAC', 'Macao'),
#     ('MDG', 'MDG', 'Madagascar'),
#     ('MWI', 'MWI', 'Malawi'),
#     ('MYS', 'MYS', 'Malaysia'),
#     ('MDV', 'MDV', 'Maldives'),
#     ('MLI', 'MLI', 'Mali'),
#     ('MLT', 'MLT', 'Malta'),
#     ('MHL', 'MHL', 'Marshall Islands'),
#     ('MTQ', 'MTQ', 'Martinique'),
#     ('MRT', 'MRT', 'Mauritania'),
#     ('MUS', 'MUS', 'Mauritius'),
#     ('MYT', 'MYT', 'Mayotte'),
#     ('MEX', 'MEX', 'Mexico'),
#     ('FSM', 'FSM', 'Micronesia (Federated States of)'),
#     ('MDA', 'MDA', 'Moldova (the Republic of)'),
#     ('MCO', 'MCO', 'Monaco'),
#     ('MNG', 'MNG', 'Mongolia'),
#     ('MNE', 'MNE', 'Montenegro'),
#     ('MSR', 'MSR', 'Montserrat'),
#     ('MAR', 'MAR', 'Morocco'),
#     ('MOZ', 'MOZ', 'Mozambique'),
#     ('MMR', 'MMR', 'Myanmar'),
#     ('NAM', 'NAM', 'Namibia'),
#     ('NRU', 'NRU', 'Nauru'),
#     ('NPL', 'NPL', 'Nepal'),
#     ('NLD', 'NLD', 'Netherlands'),
#     ('NCL', 'NCL', 'New Caledonia'),
#     ('NZL', 'NZL', 'New Zealand'),
#     ('NIC', 'NIC', 'Nicaragua'),
#     ('NER', 'NER', 'Niger'),
#     ('NGA', 'NGA', 'Nigeria'),
#     ('NIU', 'NIU', 'Niue'),
#     ('NFK', 'NFK', 'Norfolk Island'),
#     ('MNP', 'MNP', 'Northern Mariana Islands'),
#     ('NOR', 'NOR', 'Norway'),
#     ('OMN', 'OMN', 'Oman'),
#     ('PAK', 'PAK', 'Pakistan'),
#     ('PLW', 'PLW', 'Palau'),
#     ('PSE', 'PSE', 'Palestine, State of'),
#     ('PAN', 'PAN', 'Panama'),
#     ('PNG', 'PNG', 'Papua New Guinea'),
#     ('PRY', 'PRY', 'Paraguay'),
#     ('PER', 'PER', 'Peru'),
#     ('PHL', 'PHL', 'Philippines'),
#     ('PCN', 'PCN', 'Pitcairn'),
#     ('POL', 'POL', 'Poland'),
#     ('PRT', 'PRT', 'Portugal'),
#     ('PRI', 'PRI', 'Puerto Rico'),
#     ('QAT', 'QAT', 'Qatar'),
#     ('MKD', 'MKD', 'Republic of North Macedonia'),
#     ('ROU', 'ROU', 'Romania'),
#     ('RUS', 'RUS', 'Russian Federation'),
#     ('RWA', 'RWA', 'Rwanda'),
#     ('BLM', 'BLM', 'Saint Barthélemy'),
#     ('SHN', 'SHN', 'Saint Helena, Ascension and Tristan da Cunha'),
#     ('KNA', 'KNA', 'Saint Kitts and Nevis'),
#     ('LCA', 'LCA', 'Saint Lucia'),
#     ('MAF', 'MAF', 'Saint Martin (French part)'),
#     ('SPM', 'SPM', 'Saint Pierre and Miquelon'),
#     ('VCT', 'VCT', 'Saint Vincent and the Grenadines'),
#     ('WSM', 'WSM', 'Samoa'),
#     ('SMR', 'SMR', 'San Marino'),
#     ('STP', 'STP', 'Sao Tome and Principe'),
#     ('SAU', 'SAU', 'Saudi Arabia'),
#     ('SEN', 'SEN', 'Senegal'),
#     ('SRB', 'SRB', 'Serbia'),
#     ('SYC', 'SYC', 'Seychelles'),
#     ('SLE', 'SLE', 'Sierra Leone'),
#     ('SGP', 'SGP', 'Singapore'),
#     ('SXM', 'SXM', 'Sint Maarten (Dutch part)'),
#     ('SVK', 'SVK', 'Slovakia'),
#     ('SVN', 'SVN', 'Slovenia'),
#     ('SLB', 'SLB', 'Solomon Islands'),
#     ('SOM', 'SOM', 'Somalia'),
#     ('ZAF', 'ZAF', 'South Africa'),
#     ('SGS', 'SGS', 'South Georgia and the South Sandwich Islands'),
#     ('SSD', 'SSD', 'South Sudan'),
#     ('ESP', 'ESP', 'Spain'),
#     ('LKA', 'LKA', 'Sri Lanka'),
#     ('SDN', 'SDN', 'Sudan'),
#     ('SUR', 'SUR', 'Suriname'),
#     ('SJM', 'SJM', 'Svalbard and Jan Mayen'),
#     ('SWE', 'SWE', 'Sweden'),
#     ('CHE', 'CHE', 'Switzerland'),
#     ('SYR', 'SYR', 'Syrian Arab Republic'),
#     ('TWN', 'TWN', 'Taiwan (Province of China)'),
#     ('TJK', 'TJK', 'Tajikistan'),
#     ('TZA', 'TZA', 'Tanzania, United Republic of'),
#     ('THA', 'THA', 'Thailand'),
#     ('TLS', 'TLS', 'Timor-Leste'),
#     ('TGO', 'TGO', 'Togo'),
#     ('TKL', 'TKL', 'Tokelau'),
#     ('TON', 'TON', 'Tonga'),
#     ('TTO', 'TTO', 'Trinidad and Tobago'),
#     ('TUN', 'TUN', 'Tunisia'),
#     ('TUR', 'TUR', 'Turkey'),
#     ('TKM', 'TKM', 'Turkmenistan'),
#     ('TCA', 'TCA', 'Turks and Caicos Islands'),
#     ('TUV', 'TUV', 'Tuvalu'),
#     ('UGA', 'UGA', 'Uganda'),
#     ('UKR', 'UKR', 'Ukraine'),
#     ('ARE', 'ARE', 'United Arab Emirates'),
#     ('GBR', 'GBR', 'United Kingdom of Great Britain and Northern Ireland'),
#     ('UMI', 'UMI', 'United States Minor Outlying Islands'),
#     ('URY', 'URY', 'Uruguay'),
#     ('UZB', 'UZB', 'Uzbekistan'),
#     ('VUT', 'VUT', 'Vanuatu'),
#     ('VEN', 'VEN', 'Venezuela (Bolivarian Republic of)'),
#     ('VNM', 'VNM', 'Viet Nam'),
#     ('VGB', 'VGB', 'Virgin Islands (British)'),
#     ('VIR', 'VIR', 'Virgin Islands (U.S.)'),
#     ('WLF', 'WLF', 'Wallis and Futuna'),
#     ('ESH', 'ESH', 'Western Sahara'),
#     ('YEM', 'YEM', 'Yemen'),
#     ('ZMB', 'ZMB', 'Zambia'),
#     ('ZWE', 'ZWE', 'Zimbabwe'),
# ])
