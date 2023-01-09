import pathlib


# Root path
ROOT = pathlib.Path(__file__).parents[1]

# Path to folder containing chargemaster files
chargemaster_path = ROOT / "src/chargemasters"

# list of delimiters possible in chargemasters
delimiters = [
    ',',
    '|',
    ';'
    ]

# Allowed ASCII chars
allowed_chars = [
    32,33,35,36,37,38,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,
    60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,
    86,87,88,89,90,91,92,93,95,97,98,99,100,101,102,103,104,105,106,107,108,109,
    110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126
    ]

# Pattern for finding header in csv
# header_pattern = r"(?i)(?=.*(description|descr|service|desc))(.*(price|pricing|charge(s?)|pay).*)"
header_pattern = r"(?i)^(?!(?:.*(?:note|disclaimer|transparency).*))(?:.*(?:.*(description|descr|service|desc).*((price|pricing|charge(s?)|pay).*)$))"

# Patterns for parsing through csv, txt, etc.
patterns = {
    # "CARY MEDICAL CENTER chunk": r"(.*|\w{1,})(\,{6})\n(\,{6})\n((\w*\s?\W?)\,(.*)\,( \w* )(\,{4}))\n(\,{6})\n",
    # "empty_comma_row": r"(?<!\w|\d|\,|\"|\'| )(\,{3,})",
    # "headers": r"(?i)(?=.*?(?:description|descrip|desc))(?=.*?(?:price|pay(?:\w{0,2})|plan|charge(s)?))(?=.*?(?:negotiated)?).*",
    # "headers_new": r"(?i)(\,?(?=.*?(?:description|descrip|desc|service))\,?)(?=.*?(?:price|pay(?:\w{0,2})|plan|charge(s)?))(?=.*?(?:negotiated)?)(?!.*(disclaimer|cms|require)).*",
    "test": r"(?i)(?=.*(description|descr|service))(.*(price|charge(s?)|pay).*)"
    # "any_comma_not_in_quotes": r",(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))"
    }

# Regex pattern for words that shouldn't exist in a hospital header
bad_header = r"(?i)(disclaimer|transparency|note)"
# bad_header = r"(?i)^(?!(?:.*(?:note|disclaimer).*))(?:.*(?:.*(description|service).*$))"

# Levels of difficulty parsing various chargemaster file types (to me)
file_types = {
    'easy': ['.txt', '.csv'],
    'med': ['.xml', '.json'],
    'hard': ['.pdf', '.xlsx']
    }

# Columns removed when generating the insurance list
fouls = [
    '',
    'base price',
    'pricing min',
    'pricing max',
    'update date',
    'code',
    'procedure',
    'unit',
    'desc',
    'description',
    'hosp',
    'pricing amt',
    'code type',
    'revenue code',
    'payer',
    'plan',
    ]

# Possibly use this to filter insurances vs $fouls
allowed_insurances = [
    'aetna',
    'medicaid aetna better health',
    'ameriplus',
    'archbold med center',
    'avmed',
    'florida blue',
    'bright health',
    'capital health plan',
    'centivo',
    'choice med man',
    'cigna',
    'community care plan',
    'wc corvel',
    'coventry healthcare',
    'disney cruise line',
    'employer direct',
    'evolutions',
    'ez comp',
    'first health',
    'florida health alliance',
    'fringe benefit coordinators',
    'genex',
    'haven hospice',
    'health first',
    'humana',
    'medicaid amerihealth claritas',
    'medicaid florida community care plan',
    'medicaid humana',
    'medicaid integral quality care psn',
    'medicaid molina healthcare',
    'medicaid prestige',
    'medicaid simply healthcare',
    'medicaid sunshine',
    'medicaid united healthcare',
    'medicaid vivida',
    'medicaid wellcare staywell',
    'medicare aetna',
    'medicare bright health',
    'medicare capital health',
    'medicare devoted health',
    'medicare florida blue',
    'medicare health first health plan',
    'medicare humana',
    'medicare united',
    'medicare usa senior care',
    'medicare wellcare',
    'multiplan',
    'north florida evaluation and treatment center',
    'northeast florida state hospital',
    'wc orchid medical (naval hosp)',
    'prime health',
    'wc rockport health',
    'united',
    'usa senior care',
    'tricare',
    'va',
    'volusia health network',
    'wellcare hk',
    'uninsured/self pay',
    ]

# Replace various column names with a more universal name
# Keys are to be renamed to paired values
reword = {
    'pricing amt': 'base price',
    r'(?i)[^\r\n\,]*(description|descr|desc|service)[^\r\n\,]*': 'description',
    'desc': 'description',
    'quantity': 'unit',
    }
