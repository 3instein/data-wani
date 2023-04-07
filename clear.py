import gspread

sa = gspread.service_account(filename='geprek-wani-c700b4b8002f.json')

sheet = sa.open('Wani Spreadsheet')

worksheet = sheet.worksheet('Pesanan')

worksheet.clear()