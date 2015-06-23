import csv, sys, getopt, argparse, pymssql, os

import dbSettings

COLUMN_LOCAL_ID = 'LocalId'
COLUMN_UHL_SYSTEM_NUMBER = 'Uhl System Number'
COLUMN_NHS_NUMBER = 'NHS Number'
COLUMN_TITLE = 'Title'
COLUMN_LAST_NAME = 'Last Name'
COLUMN_FIRST_NAME = 'First Name'
COLUMN_DOB = 'Date of Birth'
COLUMN_GENDER = 'Gender'
COLUMN_ADDRESS_1 = 'Address 1'
COLUMN_ADDRESS_2 = 'Address 2'
COLUMN_ADDRESS_3 = 'Address 3'
COLUMN_ADDRESS_4 = 'Address 4'
COLUMN_POST_CODE = 'Post Code'

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', nargs='?')
  parser.add_argument("-o", "--outputfilename", nargs='?', help="Output filename", default="uhlSystemNumbers.csv")
  parser.add_argument("-c", "--idColumn", required=True, help="ID Column Name")
  args = parser.parse_args()

  with open(args.outputfilename, 'w') as outputFile:

    fieldnames = [
      COLUMN_LOCAL_ID,
      COLUMN_UHL_SYSTEM_NUMBER,
      COLUMN_NHS_NUMBER,
      COLUMN_TITLE,
      COLUMN_LAST_NAME,
      COLUMN_FIRST_NAME,
      COLUMN_DOB,
      COLUMN_GENDER,
      COLUMN_ADDRESS_1,
      COLUMN_ADDRESS_2,
      COLUMN_ADDRESS_3,
      COLUMN_ADDRESS_4,
      COLUMN_POST_CODE]

    output = csv.DictWriter(outputFile, fieldnames=fieldnames)

    output.writeheader()

    with pymssql.connect(dbSettings.DB_SERVER_NAME, dbSettings.DB_USERNAME, dbSettings.DB_PASSWORD, dbSettings.DB_DATABASE) as conn:
      with open(args.infile, 'r') as infile:
        spamreader = csv.DictReader(infile, delimiter=',', quotechar='"')
        for row in spamreader:
          if row[args.idColumn]:
            details = getUhlSystemNumber(conn, row[args.idColumn])

            output.writerow({
              COLUMN_LOCAL_ID : row[args.idColumn],
              COLUMN_UHL_SYSTEM_NUMBER : '' if details['main_pat_id'] is None else details['main_pat_id'].upper(),
              COLUMN_NHS_NUMBER : '' if details['nhs_number'] is None else details['nhs_number'].replace(' ', ''),
              COLUMN_TITLE : '' if details['title'] is None else details['title'].title(),
              COLUMN_LAST_NAME : '' if details['last_name'] is None else details['last_name'].title(),
              COLUMN_FIRST_NAME : '' if details['first_name'] is None else details['first_name'].title(),
              COLUMN_DOB : '' if details['dob'] is None else details['dob'],
              COLUMN_GENDER : '' if details['gender'] is None else details['gender'],
              COLUMN_ADDRESS_1 : '' if details['pat_addr1'] is None else details['pat_addr1'].title(),
              COLUMN_ADDRESS_2 : '' if details['pat_addr2'] is None else details['pat_addr2'].title(),
              COLUMN_ADDRESS_3 : '' if details['pat_addr3'] is None else details['pat_addr3'].title(),
              COLUMN_ADDRESS_4 : '' if details['pat_addr4'] is None else details['pat_addr4'].title(),
              COLUMN_POST_CODE : '' if details['postcode'] is None else details['postcode'].upper()
              })

def getUhlSystemNumber(pmiConnection, identifier):
    if (identifier.strip() == ""):
      return None

    with pmiConnection.cursor(as_dict=True) as cursor:
        cursor.execute('SELECT * FROM [PMIS_LIVE].[dbo].[UHL_PMI_QUERY_BY_ID] (%s)', identifier)
        return cursor.fetchone()

if __name__ == "__main__":
   main()

