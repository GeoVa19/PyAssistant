"""
    Copyright (C) 2018  George Vasios and Dimitris Kalpaktzidis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROMPT_FILE_NAME = os.path.join(PROJECT_ROOT, "media", "prompt.mp3")
STARTUP_XML_FILE_NAME = os.path.join(PROJECT_ROOT, "aiml_sets", "std-startup.xml")
BASE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json?"
BRAIN_FILE = "bot_brain.brn"
ERROR_MESSAGE = "I didn't get that. Please make sure that your question has the right format. " \
                "Say 'I need some help' to read the instructions."
LANGUAGE_DICTIONARY = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azeerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese": "zh-CN",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "iw",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Kurdish": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nyanja (Chichewa)": "ny",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali	": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu"
}

CURRENCIES = {'United Arab Emirates Dirham': 'AED', 'Afghan Afghani': 'AFN', 'Lek': 'ALL',
              'Dram': 'AMD', 'Netherlands Antillean Guilder': 'ANG', 'Kwanza': 'AOA',
              'Argentine Peso': 'ARS', 'Australian Dollar': 'AUD', 'Aruban Florin': 'AWG', 'Azerbaijani Manat': 'AZN',
              'Barbadian Dollar': 'BBD', 'Bangladeshi Taka': 'BDT',
              'Lev': 'BGN', 'Bahraini Dinar': 'BHD', 'Burundian Franc': 'BIF', 'Bermudan Dollar': 'BMD',
              'Brunei Dollar': 'BND', 'Bolivian Boliviano': 'BOB', 'Brazilian Real': 'BRL', 'Bahamian Dollar': 'BSD',
              'Bhutanese Ngultrum': 'BTN', 'Botswanan Pula': 'BWP', 'New Belarusian Ruble': 'BYN',
              'Belarusian Ruble': 'BYR', 'Belize Dollar': 'BZD', 'Canadian Dollar': 'CAD', 'Congolese Franc': 'CDF',
              'Swiss Franc': 'CHF', 'Chilean Unit of Account (UF)': 'CLF', 'Chilean Peso': 'CLP',
              'Yuan': 'CNY',
              'Colombian Peso': 'COP', 'Costa Rican Colón': 'CRC', 'Cuban Convertible Peso': 'CUC',
              'Cuban Peso': 'CUP',
              'Cape Verdean Escudo': 'CVE', 'Czech Republic Koruna': 'CZK', 'Djiboutian Franc': 'DJF',
              'Krone': 'DKK', 'Dominican Peso': 'DOP', 'Algerian Dinar': 'DZD', 'Egyptian Pound': 'EGP',
              'Eritrean Nakfa': 'ERN', 'Ethiopian Birr': 'ETB', 'Euro': 'EUR', 'Fijian Dollar': 'FJD',
              'Falkland Islands Pound': 'FKP', 'British Pound': 'GBP', 'Georgian Lari': 'GEL',
              'Guernsey Pound': 'GGP', 'Ghanaian Cedi': 'GHS', 'Gibraltar Pound': 'GIP', 'Gambian Dalasi': 'GMD',
              'Guinean Franc': 'GNF', 'Guatemalan Quetzal': 'GTQ', 'Guyanaese Dollar': 'GYD',
              'Hong Kong Dollar': 'HKD',
              'Honduran Lempira': 'HNL', 'Croatian Kuna': 'HRK', 'Haitian Gourde': 'HTG', 'Hungarian Forint': 'HUF',
              'Indonesian Rupiah': 'IDR', 'Israeli New Sheqel': 'ILS', 'Manx pound': 'IMP', 'Indian Rupee': 'INR',
              'Iraqi Dinar': 'IQD', 'Iranian Rial': 'IRR', 'Icelandic Króna': 'ISK', 'Jersey Pound': 'JEP',
              'Jamaican Dollar': 'JMD', 'Jordanian Dinar': 'JOD', 'Japanese Yen': 'JPY', 'Kenyan Shilling': 'KES',
              'Kyrgystani Som': 'KGS', 'Cambodian Riel': 'KHR', 'Comorian Franc': 'KMF', 'North Korean Won': 'KPW',
              'South Korean Won': 'KRW', 'Kuwaiti Dinar': 'KWD', 'Cayman Islands Dollar': 'KYD',
              'Kazakhstani Tenge': 'KZT', 'Laotian Kip': 'LAK', 'Lebanese Pound': 'LBP', 'Sri Lankan Rupee': 'LKR',
              'Liberian Dollar': 'LRD', 'Lesotho Loti': 'LSL', 'Lithuanian Litas': 'LTL', 'Latvian Lats': 'LVL',
              'Libyan Dinar': 'LYD', 'Moroccan Dirham': 'MAD', 'Moldovan Leu': 'MDL', 'Malagasy Ariary': 'MGA',
              'Macedonian Denar': 'MKD', 'Myanma Kyat': 'MMK', 'Mongolian Tugrik': 'MNT', 'Macanese Pataca': 'MOP',
              'Mauritanian Ouguiya': 'MRO', 'Mauritian Rupee': 'MUR', 'Maldivian Rufiyaa': 'MVR',
              'Malawian Kwacha': 'MWK', 'Mexican Peso': 'MXN', 'Malaysian Ringgit': 'MYR', 'Mozambican Metical': 'MZN',
              'Namibian Dollar': 'NAD', 'Nigerian Naira': 'NGN', 'Nicaraguan Córdoba': 'NIO', 'Norwegian Krone': 'NOK',
              'Nepalese Rupee': 'NPR', 'New Zealand Dollar': 'NZD', 'Omani Rial': 'OMR', 'Panamanian Balboa': 'PAB',
              'Peruvian Nuevo Sol': 'PEN', 'Papua New Guinean Kina': 'PGK', 'Philippine Peso': 'PHP',
              'Pakistani Rupee': 'PKR', 'Polish Zloty': 'PLN', 'Paraguayan Guarani': 'PYG', 'Qatari Rial': 'QAR',
              'Romanian Leu': 'RON', 'Serbian Dinar': 'RSD', 'Russian Ruble': 'RUB', 'Rwandan Franc': 'RWF',
              'Saudi Riyal': 'SAR', 'Solomon Islands Dollar': 'SBD', 'Seychellois Rupee': 'SCR',
              'Sudanese Pound': 'SDG', 'Swedish Krona': 'SEK', 'Singapore Dollar': 'SGD', 'Saint Helena Pound': 'SHP',
              'Sierra Leonean Leone': 'SLL', 'Somali Shilling': 'SOS', 'Surinamese Dollar': 'SRD',
              'São Tomé and Príncipe Dobra': 'STD', 'Salvadoran Colón': 'SVC', 'Syrian Pound': 'SYP',
              'Swazi Lilangeni': 'SZL', 'Thai Baht': 'THB', 'Tajikistani Somoni': 'TJS', 'Turkmenistani Manat': 'TMT',
              'Tunisian Dinar': 'TND', 'Tongan Paʻanga': 'TOP', 'Turkish Lira': 'TRY',
              'Trinidad and Tobago Dollar': 'TTD', 'New Taiwan Dollar': 'TWD', 'Tanzanian Shilling': 'TZS',
              'Ukrainian Hryvnia': 'UAH', 'Ugandan Shilling': 'UGX', 'United States Dollar': 'USD', 'US Dollar': 'USD',
              'Uruguayan Peso': 'UYU', 'Uzbekistan Som': 'UZS', 'Venezuelan Bolívar Fuerte': 'VEF',
              'Vietnamese Dong': 'VND', 'Vanuatu Vatu': 'VUV', 'Samoan Tala': 'WST', 'CFA Franc BEAC': 'XAF',
              'Silver (troy ounce)': 'XAG', 'Gold (troy ounce)': 'XAU', 'East Caribbean Dollar': 'XCD',
              'Special Drawing Rights': 'XDR', 'CFA Franc BCEAO': 'XOF', 'CFP Franc': 'XPF', 'Yemeni Rial': 'YER',
              'South African Rand': 'ZAR', 'Zambian Kwacha': 'ZMW',
              'Zimbabwean Dollar': 'ZWL'}