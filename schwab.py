import pandas as pd
import util.db as db

# read in data
df = pd.read_csv('schwab.csv', na_filter=False)

# #####################################################################
# # FORMAT COLUMNS
# #####################################################################

# Column Name (source):     Date
# Column Name (database):   trade_date, settle_date
# Null:                     not null, not null
# Split from Date
# Convert date to datetime
dates = df["Date"].str.split(" ", n=3, expand=True)
df['Trade Date'] = pd.to_datetime(dates[3])
df['Date'] = pd.to_datetime(dates[0])

# Column Name (source):     Symbol
# Column Name (database):   sym, exp_date, strike_price, call_or_put
# Null:                     null
# Extract from Symbol
details = df['Symbol'].str.split(" ", n=4, expand=True)
df['sym'] = details[0]
df['exp_date'] = pd.to_datetime(details[1])
df['strike_price'] = pd.to_numeric(details[2])
df['call_or_put'] = details[3]

# Column Name (source):     Symbol
# Column Name (database):   option
# Null:                     null
# Concat from sym, exp_date, strike_Price, call_or_put
df['Symbol'] = df['sym'] + df['call_or_put'] + df['exp_date'].dt.strftime('%y%m%d') + df['strike_price'].astype(str)

# Column Name (source):     n/a
# Column Name (database):   broker
# Null:                     not null
df['Institution'] = 'Schwab'

# Column Name (source):     Price, Fees & Comm, Amount
# Column Name (database):   price, commission, regulatory_fee, amount
# Null:                     null
# Remove dollar sign ($), comma (,), parenthesis, and whitespace
regex_symbol = '(\$|\,|\(|\)|\s)'
df['Price'] = df['Price'].str.replace(regex_symbol, '', regex=True)
df['Price'] = pd.to_numeric(df['Price'])

df['Fees & Comm'] = df['Fees & Comm'].str.replace(regex_symbol, '', regex=True)
df['Fees & Comm'] = pd.to_numeric(df['Fees & Comm'])

df['Amount'] = df['Amount'].str.replace(regex_symbol, '', regex=True)
df['Amount'] = pd.to_numeric(df['Amount'])