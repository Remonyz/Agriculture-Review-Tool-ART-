import sqlite3

conn = sqlite3.connect('agriculture.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CA'")
table_exists = c.fetchone()

if not table_exists:
    c.execute("""CREATE TABLE CA(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        commodity TEXT,
        planted_acres INTEGER,
        harvested_acres INTEGER,
        yields TEXT,
        production TEXT,
        ppu TEXT,
        value TEXT
    )""")

    c.execute("""CREATE TABLE ALB(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commodity TEXT,
            planted_acres INTEGER,
            harvested_acres INTEGER,
            yields TEXT,
            production TEXT,
            ppu TEXT,
            value TEXT
        )""")

    c.execute("""CREATE TABLE AL(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commodity TEXT,
            planted_acres INTEGER,
            harvested_acres INTEGER,
            yields TEXT,
            production TEXT,
            ppu TEXT,
            value TEXT
        )""")

    c.execute("""CREATE TABLE CO(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commodity TEXT,
            planted_acres INTEGER,
            harvested_acres INTEGER,
            yields TEXT,
            production TEXT,
            ppu TEXT,
            value TEXT
        )""")

    c.execute("""CREATE TABLE CN(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commodity TEXT,
            planted_acres INTEGER,
            harvested_acres INTEGER,
            yields TEXT,
            production TEXT,
            ppu TEXT,
            value TEXT
        )""")



conn.commit()
conn.close()

def insert_data(table, commodity, planted_acres, harvested_acres, yields, production, ppu, value):
    conn = sqlite3.connect('agriculture.db')
    c = conn.cursor()

    for i in range(len(commodity)):
        c.execute("""INSERT INTO {} (commodity, planted_acres, harvested_acres, yields, production, ppu, value) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""".format(table), 
                  (commodity[i], planted_acres[i], harvested_acres[i], yields[i], production[i], ppu[i], value[i]))

    conn.commit()
    conn.close()

def convert_to_common_unit(value, unit):
    # Define conversion factors for different units
    conversion_factors = {
        "CWT": 1,  # Common Weight
        "BU": 40,  # Bushels to pounds
        "TON": 2000,  # Tons to pounds
        "LB": 1,  # Pounds
        "BOXES": 20  # Boxes to pounds
    }

    # Handle empty or invalid input values
    if not value or not unit:
        return 0  # Return 0 for empty or invalid values

    # Extract numeric value and unit from the input string
    numeric_value = ''.join(filter(str.isdigit, value))
    if not numeric_value:
        return 0  # Return 0 if numeric value is empty
    numeric_value = float(numeric_value)
    
    unit = unit.strip().split('/')[0].strip()  # Extract unit before '/'

    # Convert value to common unit for comparison
    if unit in conversion_factors:
        return numeric_value * conversion_factors[unit]
    else:
        return numeric_value  # Return original value if unit not found


def findMostProfitable(table):
    conn = sqlite3.connect('agriculture.db')
    c = conn.cursor()

    # Fetch all rows from the specified table
    c.execute("SELECT commodity, yields, ppu FROM {}".format(table))
    rows = c.fetchall()

    # Initialize variables to store the highest profit and corresponding commodity
    highest_profit = 0
    most_profitable_commodity = None

    # Iterate through each row to calculate profit and find the most profitable commodity
    for row in rows:
        commodity, yield_str, ppu_str = row

        # Convert yield and ppu to common units for comparison
        yield_value = convert_to_common_unit(yield_str, ppu_str)
        ppu_value = convert_to_common_unit(ppu_str, ppu_str)

        # Calculate the profit by multiplying yield and ppu
        profit = yield_value * ppu_value

        # Update highest_profit and most_profitable_commodity if current row's profit is higher
        if profit > highest_profit:
            highest_profit = profit
            most_profitable_commodity = commodity

    conn.close()

    # Return the most profitable commodity and its profit
    return most_profitable_commodity, highest_profit

def findProfitPerAcre(table, commodity):
    conn = sqlite3.connect('agriculture.db')
    c = conn.cursor()

    # Fetch the row corresponding to the given commodity
    c.execute("SELECT yields, ppu FROM {} WHERE commodity = ?".format(table), (commodity,))
    row = c.fetchone()

    if row:
        # Extract yield and ppu values from the row
        yield_str, ppu_str = row

        # Check if yield_str or ppu_str is None or empty
        if yield_str is None or ppu_str is None:
            conn.close()
            return None, None

        # Extract numeric values from yield and ppu strings
        yield_value = 0 if yield_str == 'None' else float(''.join(filter(str.isdigit, yield_str)))
        ppu_value = 0 if ppu_str == 'None' else float(''.join(filter(lambda x: x.isdigit() or x == '.', ppu_str)))

        conn.close()

        # Calculate the profit per acre by multiplying yield and ppu
        profit_per_acre = yield_value * ppu_value

        # Return the profit per acre and the ppu value
        return profit_per_acre, ppu_str
    else:
        conn.close()
        return None, None

def marginOfError(table, commodity):
    conn = sqlite3.connect('agriculture.db')
    c = conn.cursor()

    # Fetch the planted and harvested acres for the given commodity
    c.execute("SELECT planted_acres, harvested_acres FROM {} WHERE commodity = ?".format(table), (commodity,))
    row = c.fetchone()

    if row:
        planted_acres, harvested_acres = row
        if planted_acres == 'None' or harvested_acres == 'None':
            conn.close()
            return None
        else:
            # Remove commas from the strings and then convert to integers
            planted_acres = int(planted_acres.replace(',', ''))
            harvested_acres = int(harvested_acres.replace(',', ''))

            # Calculate the margin of error as a percentage
            margin_error_percentage = ((planted_acres - harvested_acres) / planted_acres) * 100

            # Round the margin error to two decimal places
            margin_error_percentage = round(margin_error_percentage, 2)

            conn.close()
            return margin_error_percentage
    else:
        conn.close()
        return None

def getState():
    conn = sqlite3.connect('agriculture.db')
    c = conn.cursor()

    # Fetch all table names from the sqlite_master table
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = c.fetchall()

    conn.close()

    # Extract table names from the result set
    table_names = [name[0] for name in table_names]

    return table_names

def getCommodities(table):
    conn = sqlite3.connect('agriculture.db')
    c = conn.cursor()

    # Fetch all distinct commodities from the specified table
    c.execute("SELECT DISTINCT commodity FROM {}".format(table))
    commodities = c.fetchall()

    conn.close()

    # Extract commodity names from the result set
    commodities = [commodity[0] for commodity in commodities]

    return commodities








