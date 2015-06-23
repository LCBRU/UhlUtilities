#!/usr/bin/env python

import csv, sys, getopt, argparse, pymssql

COLUMN_LOCAL_ID = 'LocalId'
COLUMN_UHL_SYSTEM_NUMBER = 'UhlSystemNumber'

import dbSettings

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', nargs='?')
  parser.add_argument("-o", "--outputfilename", nargs='?', help="Output filename", default="uhlSystemNumbers.csv")
  args = parser.parse_args()

  with open(args.outputfilename, 'w') as outputFile:

    fieldnames = [
      COLUMN_LOCAL_ID,
      COLUMN_UHL_SYSTEM_NUMBER]

    output = csv.DictWriter(outputFile, fieldnames=fieldnames)

    output.writeheader()

    with pymssql.connect(dbSettings.DB_SERVER_NAME, dbSettings.DB_USERNAME, dbSettings.DB_PASSWORD, dbSettings.DB_DATABASE) as conn:
      with open(args.infile, 'r') as infile:
        for identifier in infile:
          strippedId = identifier.strip()

          systemId = getUhlSystemNumber(conn, strippedId)

          output.writerow({
            COLUMN_LOCAL_ID : strippedId,
            COLUMN_UHL_SYSTEM_NUMBER : '' if systemId is None else systemId
            })

def getUhlSystemNumber(pmiConnection, identifier):
    if (identifier.strip() == ""):
      return None

    with pmiConnection.cursor() as cursor:
        cursor.execute('SELECT [dbo].[USYN_UFN_GET_CURRENT_PATIENT_ID] (%s)', identifier)
        row = cursor.fetchone()

        if row:
          return row[0]
        else:
          return None

if __name__ == "__main__":
   main()

