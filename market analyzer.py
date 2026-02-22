import os
import csv
from datetime import date

# Required columns for indicator calculations
column = ["DATE", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]

def loop_over_files(folder_path):
    """
    Iterates over all raw CSV files in the given folder,
    cleans them, validates numeric data, and computes RSI.
    """
    try:
        file_list = os.listdir(folder_path)
    except FileNotFoundError:
        print("\nFolder Path Doesn't Exist:")
        return

    for file_name in file_list:
        if file_name.lower().endswith(".csv"):
            stock = file_name.split("-")[2]   # extract stock name from filename
            full_path = os.path.join(folder_path, file_name)

            clean_file_path = process_raw_file(full_path, stock)
            validate_rows = process_clean_file(clean_file_path)

            gain, loss = profit_loss(validate_rows)
            rsi_value = rsi_ma_calculation(gain, loss)

            if rsi_value is not None:
                print(stock, rsi_value)


def process_raw_file(file_path, stock):
    """
    Reads raw CSV, selects required columns,
    removes missing/invalid values, and writes a clean CSV.
    """
    today_date = date.today().isoformat()
    folder = r"DATA\CLEAN"
    os.makedirs(folder, exist_ok=True)

    clean_file_path = f"{stock}_{today_date}.csv"
    full_clean_file_path = os.path.join(folder, clean_file_path)

    with open(file_path, "r", encoding="utf-8-sig", newline="") as f, \
         open(full_clean_file_path, "w", newline="") as g:

        reader = csv.reader(f)
        writer = csv.writer(g)

        header = next(reader)  # read header row
        index = []

        # Identify column indices needed for analysis
        for i, val in enumerate(header):
            if val in column:
                index.append(i)

        # Write cleaned header
        writer.writerow([header[i] for i in index])

        # Write cleaned data rows
        for row in reader:
            if not row:
                continue

            clean_row = []
            for i in index:
                if row[i] and row[i] != "NA" and row[i] != "-":
                    value = row[i].replace(",", "")  # remove numeric separators
                    clean_row.append(value)

            # Ensure row completeness
            if len(clean_row) == 6:
                writer.writerow(clean_row)

    return full_clean_file_path


def process_clean_file(clean_file_path):
    """
    Reads cleaned CSV and converts numeric fields
    to proper data types for indicator computation.
    """
    with open(clean_file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        validate_rows = []

        next(reader)  # explicitly skip header

        for row in reader:
            try:
                row[0] = str(row[0])       # DATE
                row[1] = float(row[1])     # OPEN
                row[2] = float(row[2])     # HIGH
                row[3] = float(row[3])     # LOW
                row[4] = float(row[4])     # CLOSE
                row[5] = int(row[5])       # VOLUME
                validate_rows.append(row)
            except ValueError:
                # Skip rows with invalid numeric conversion
                continue

    return validate_rows


def profit_loss(validate_rows):
    """
    Computes daily gains and losses based on closing prices.
    """
    closing_data = []
    gain = []
    loss = []

    for row in validate_rows:
        closing_data.append(row[4])  # CLOSE price

    for i in range(len(closing_data) - 1):
        change = closing_data[i + 1] - closing_data[i]

        if change > 0:
            gain.append(change)
            loss.append(0)
        elif change < 0:
            gain.append(0)
            loss.append(abs(change))
        else:
            gain.append(0)
            loss.append(0)

    return gain, loss


def rsi_ma_calculation(gain, loss):
    """
    Computes the FIRST RSI value using simple average
    (not Wilder-smoothed RSI).
    """
    if len(gain) < 14 or len(loss) < 14:
        return None

    total_gain = 0
    total_loss = 0

    for i in range(14):
        total_gain += gain[i]
        total_loss += loss[i]

    avg_gain = total_gain / 14
    avg_loss = total_loss / 14

    if avg_loss != 0:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    else:
        return 100


folder_path = input("Enter Folder Path: ")
loop_over_files(folder_path)