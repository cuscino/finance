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
      - dates: a list of the dates (date object)
      - values: a list of values. Each value is a list: Open, High, Low,
        Close, Volume, Adj. Close
    """
    
    url = ('http://real-chart.finance.yahoo.com/table.csv?s=' + symbol +
           "&a=%0d&b=%d&c=%d&d=08&e=6&f=2015&g=d&ignore=.csv" % (timestart.month - 1, timestart.day, timestart.year) +
           "&d=%0d&e=%d&f=%d&g=d&ignore=.csv" % (timestart.month - 1, timestart.day, timestart.year))
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    lines = htmltext.split('\n')
    dates = []
    values = []
    for line in lines[1:]:
        pieces = line[0].split('-')
        d = datetime.date(pieces[0], pieces[1], pieces[2])
        dates.append(d)
        values.append(line[1:])
    return (dates, values)


