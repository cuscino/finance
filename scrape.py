import csv
import datetime
import urllib
import re

def HistoricData(symbol, timestart, timeend):
    """Return historic data for a symbol.

    Args:
      - symbol: the symbol
      - timestart: start time (date object.)
      - timeend: end time (date object.)
    Returns:
      - a list of pairs [date, prices] where date is a date object and prices is
        a list of the form [open, high, low, close, volume, adj. close,
        dividend] dividend is paied before the date.
    """
    
    url = ('http://real-chart.finance.yahoo.com/table.csv?s=' + symbol +
           "&a=%0d&b=%d&c=%d" % (timestart.month - 1, timestart.day, timestart.year) +
           "&d=%0d&e=%d&f=%d&g=d&ignore=.csv" % (timeend.month - 1, timeend.day, timeend.year))
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    lines = htmltext.split('\n')
    values = []
    for line in lines[1:-1]:
        pieces = line.split(',')
        date_pieces = [int(x) for x in pieces[0].split('-')]
        d = datetime.date(date_pieces[0], date_pieces[1], date_pieces[2])
        v = [float(x) for x in pieces[1:]]
        values.append([d, v])
    values.sort(key=lambda value: value[0])
    print values[-1][1]
    values[0][1].append(0)
    for i in range(len(values) - 2, 0, -1):
        qtp = values[i + 1][1][5] / values[i + 1][1][3]
        qt = values[i][1][5] / values[i][1][3]
        close_price = values[i][1][3]
        ratio = qtp / qt
        if ratio == 1:
            dividend = 0
        else:
            dividend = round((ratio - 1) / ratio * close_price, 2)
        if dividend < 1e-3:
            dividend = 0
        if dividend != 0:
            print 'Dividend ', str(values[i + 1][0]), dividend
        values[i + 1][1].append(dividend)
    return values

def SaveData(path, symbol, values):
    """Save data to a csv file.

    Args:
      - path: path where the file is created.
      - symbol: symbol for which the file is created,
      - values: values to save. We expect this be a list of pairs
        [date, prices] 
    Returns:
      - None
    """
    filename = path + '/' + symbol + '.data' 
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='#', quoting=csv.QUOTE_MINIMAL)
        for value in values:
            csvwriter.writerow([str(value[0])] +  value[1])

def LoadData(path, symbol):
    """Load data from a csv file.

    Args:
      - path: path where the file is located.
      - symbol: symbol for which the file is created,
    Returns:
      - values: values to load. This be a list of pairs
        [date, prices] 
    """
    filename = path + '/' + symbol + '.data' 
    values = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',',
                               quotechar='#', quoting=csv.QUOTE_MINIMAL)
        for line in csvreader:
            date_pieces = [int(x) for x in line[0].split('-')]
            d = datetime.date(date_pieces[0], date_pieces[1], date_pieces[2])
            value = [d, [float(x) for x in line[1:]]]
            values.append(value)
    return values

def MergeData(values, values_add):
    values.sort(key=lambda value: value[0])
    values_add.sort(key=lambda value: value[0])
    i = 0
    for value_add in values_add:
        while i < len(values) and values[i][0] < value_add[0]:
            i += 1
        if i >= len(values):
            values.append(value_add)
            i += 1
            continue
        if values[i][0] > value_add[0]:
            values.insert(i, value_add)
            continue
        if values[i][0] == value_add[0]:
            if values[i][1] == value_add[1]:
                continue
            else:
                print 'Mismatch in MergeData for date ', str(value_add[0])
                print 'Original :', values[i][1]
                print 'Added :', value_add[1]

def Test():
    symbol = 'SCMN.VX'
    timestart = datetime.date(2008, 1, 1)
    timeend = datetime.date.today()
    values = HistoricData(symbol, timestart, timeend)
    values_ori = LoadData('/home/sbaiz/finance', symbol)
    MergeData(values_ori, values)
#    for value in values:
#        print str(value[0]), value[1]

