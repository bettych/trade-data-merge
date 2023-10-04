import pandas as pd
import util.db as db
import re
from collections import namedtuple
# from decimal import Decimal

# read in data
df = pd.read_csv('fidelity.csv', na_filter=False)

# remove unnecessary columns
cols_to_drop = [
    'Security Type',
    'Accrued Interest ($)',
    'Security Description'
]
df = df.drop(columns = cols_to_drop)

# rename columns
df = df.rename(columns = {
    'Price ($)':'Price',
    'Commission ($)':'Commission',
    'Fees ($)':'Fees',
    'Amount ($)':'Amount',
    'Action':'Description'
    })

# strip whitespace
for col in df.columns:
    df[col] = df[col].str.strip(to_strip=None)
    df[col] = df[col].str.replace('  ', '')


# #####################################################################
# # FORMAT COLUMNS
# #####################################################################

# Column Name (source):     Run Date
# Column Name (database):   trade_date
# Null:                     not null
# Convert date to datetime
df['Run Date'] = pd.to_datetime(df['Run Date'])

# Column Name (source):     Settlement Date
# Column Name (database):   settle_date
# Null:                     null
# Convert date to datetime
df['Settlement Date'] = pd.to_datetime(df['Settlement Date'])

# Column Name (source):     Symbol
# Column Name (database):   exp_date
# Null:                     null
# Extract expiration date from Symbol
regex_exp_date = '(\d{6}(?=[CP]))'
df['Expiration Date'] = df['Symbol'].str.extract(regex_exp_date).fillna('')
df['Expiration Date'] = pd.to_datetime(
    df['Expiration Date'], 
    format = "%y%m%d", 
    errors = "coerce"
    )

# Column Name (source):     Symbol
# Column Name (database):   strike_price
# Null:                     null
# Extract strike price from Symbol
regex_strike_price = '((?<=\d[CP]).+)'
df['Strike Price'] = df['Symbol'].str.extract(regex_strike_price)
df['Strike Price'] = pd.to_numeric(df['Strike Price'])


# Column Name (source):     Symbol
# Column Name (database):   call_or_put
# Null:                     null
# Extract option type (call or put) from Symbol
regex_call_put = '((?<=\d)[CP](?=\d))'
df['Call or Put'] = df['Symbol'].str.extract(regex_call_put).fillna('')

# Column Name (source):     Symbol
# Column Name (database):   option
# Null:                     null
# Extract option from Symbol
regex_option = '((?<=\-).+)'
df['Option'] = df['Symbol'].str.extract(regex_option).fillna('')

# Column Name (source):     Symbol
# Column Name (database):   symbol
# Null:                     null
# Extract option from Symbol
regex_symbol = '([A-Z]{1,5})'
df['Symbol'] = df['Symbol'].str.extract(regex_symbol).fillna('')


# Column Name (source):     Price
# Column Name (database):   price
# Null:                     null
# Conver to numeric
df['Price'] = pd.to_numeric(df['Price'])

# Column Name (source):     Commission
# Column Name (database):   commission
# Null:                     null
# Conver to numeric
df['Commission'] = pd.to_numeric(df['Commission'])

# Column Name (source):     Fees
# Column Name (database):   regulatory_fee
# Null:                     null
# Conver to numeric
df['Fees'] = pd.to_numeric(df['Fees'])

# Column Name (source):     n/a
# Column Name (database):   broker
# Null:                     not null
df['Institution'] = 'Fidelity'

# Column Name (source):     Amount
# Column Name (database):   amount
# Null:                     null
# Convert to numeric
df['Amount'] = pd.to_numeric(df['Amount'])


# Column Name (source):     Description
# Column Name (database):   Category
# Column Name (database):   Type
# Null:                     not null

category = []
type = []

connection = db.connect_to_db()
cursor = connection.cursor()

cursor.execute("SELECT * FROM reference WHERE fidelity IS NOT NULL")
reference = cursor.fetchall()

for index, value in df["Description"].items():
    for each in reference:
        result = re.search(each[3], value)
        if result != None:
            category.append(each[1]) # category
            type.append(each[2]) # type
            break

df['Category'] = category
df['Type'] = type