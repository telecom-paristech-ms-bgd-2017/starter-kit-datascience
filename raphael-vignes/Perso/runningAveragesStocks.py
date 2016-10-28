#!/usr/bin/env python

import yahoo_finance as yf
import pandas as pd
import datetime
from matplotlib import pyplot
from bdateutil import isbday

def updatePrices(stocks):
    value = []
    print("============Updating Prices===========")
    for stock in stocks :
        print("Updating : " + stock)
        try :
            val = yf.Share(stock).get_price()
        except :
            for _ in range(100):
                try :
                    val = yf.Share(stock).get_price()
                    break
                except:
                    continue
        value.append(float(val))
    return  value

def updateChanges(stocks):
    print("============Updating changes===========")
    prev_value = []
    for stock in stocks:
        print("Updating : " + stock)
        try :
            prev_val = yf.Share(stock).get_change()
        except :
            for _ in range(100):
                try :
                    prev_val = yf.Share(stock).get_change()
                    break
                except:
                    continue
        prev_value.append(float(prev_val))
    return prev_value

def updateBNPA(stocks):
    print("============Updating BNPA===========")
    bnpa = []
    for stock in stocks:
        print("Updating : " + stock)
        try :
            b = yf.Share(stock).get_earnings_share()
        except :
            for _ in range(100):
                try :
                    b = yf.Share(stock).get_earnings_share()
                    break
                except:
                    continue
        bnpa.append(float(b))
    return bnpa

def updatePER(stocks):
    print("============Updating PER===========")
    PER = []
    for stock in stocks:
        print("Updating : " + stock)
        try :
            b = yf.Share(stock).get_price_earnings_ratio()
        except :
            for _ in range(100):
                try :
                    b = yf.Share(stock).get_price_earnings_ratio()
                    break
                except:
                    continue
        PER.append(b)
    return PER

def updateDividend(stocks) :
    print("============Updating Dividend===========")
    div =[]
    for stock in stocks:
        print("Updating : " + stock)
        try :
            d = yf.Share(stock).get_dividend_yield()
        except :
            for _ in range(100):
                try :
                    d = yf.Share(stock).get_dividend_yield()
                    break
                except:
                    continue
        div.append(d)
    return div

def updateTrend(stock_and_price):
    print("============Updating Graphical Trend===========")
    tend = []
    for price, stock in zip(stock_and_price['stock value'],stock_and_price['Stock']):
        print("Updating : " + stock)
        try :
            mm50 = yf.Share(stock).get_50day_moving_avg()
            mm200 = yf.Share(stock).get_200day_moving_avg()
        except :
            for _ in range(100):
                try :
                    mm50 = yf.Share(stock).get_50day_moving_avg()
                    mm200 = yf.Share(stock).get_200day_moving_avg()
                    break
                except:
                    continue
        mm50 = float(mm50)
        mm200 = float(mm200)
        price = float(price)
        if price > mm50 and price > mm200: tend.append('up')
        elif price < mm50 and price < mm200 : tend.append('down')
        elif price < mm50 and price > mm200 : tend.append('neutral up')
        elif price > mm50 and price < mm200 : tend.append('neutral down')
    return tend

def updatePortfolio(initial, portfolio) :
    now = datetime.datetime.now()
    portfolio['Date'] = now.date()
    portfolio = pd.DataFrame(portfolio, columns = ['Date', 'Stock','PRU', 'Nb Action'])
    portfolio['initial amount'] = portfolio['PRU'] * portfolio['Nb Action']
    portfolio['stock value'] = updatePrices(portfolio['Stock'])
    portfolio['Current cap'] = portfolio['Nb Action'] * portfolio['stock value']
    portfolio['plusvalue'] = portfolio['Current cap'] - portfolio['initial amount']
    l = []
    for s in range(len(portfolio['Stock'])) :
        if portfolio.ix[s]['plusvalue'] > 0 : l.append((portfolio.ix[s]['Current cap'] / portfolio.ix[s]['initial amount'] - 1) * 100)
        else : l.append(-((1 - (portfolio.ix[s]['Current cap'] / portfolio.ix[s]['initial amount'])) * 100))
    portfolio['plusvalue_pct'] = l
    portfolio['Variation veille'] = updateChanges(portfolio['Stock'])
    portfolio['pct_portfolio'] = portfolio['Current cap'] / portfolio['Current cap'].sum() * 100
    portfolio['BNPA'] = updateBNPA(portfolio['Stock'])
    portfolio['PER'] = updatePER(portfolio['Stock'])
    #portfolio['Rdt Dividende'] = updateDividend(portfolio['Stock'])
    portfolio['Trend'] = updateTrend(portfolio)
    print(portfolio)
    return  portfolio

def updateStocksCsv(file, portfolio):
    portfolio.to_csv(file, mode = 'a', date_format = '%d%m%Y', index = False, sep = '\t', float_format = '%.2f', header = False)

def computePortfolioYield(portfolio, cash, initial):
    if portfolio['Current cap'].sum() > initial :
        print(portfolio['Current cap'].sum())
        yld = (((portfolio['Current cap'].sum() + cash) / initial) - 1) * 100
    else : yld = - (1 - (portfolio['Current cap'].sum() + cash) / initial) * 100
    indexes = getIndexValues()
    account = {'date': datetime.datetime.now().date(), 'total' : portfolio['Current cap'].sum() + cash, 'yield': yld, 'cac40': indexes['cac40'], 'cacmid': indexes['cacmid'],
               'cacsmall': indexes['cacsmall']}
    df = pd.DataFrame(account, columns = ['date', 'total', 'yield', 'cac40', 'cacmid', 'cacsmall'], index = [0])
    return df

def updateAccountCsv(file, account):
    account.to_csv(file, mode = 'a', date_format = '%d-%m-Y%', index = False, sep = '\t', float_format = '%.2f', header = False)

def getIndexValues():
    try :
        cac40 = yf.Share('PX1GR.PA')
        cacmid = yf.Share('CACMR.PA')
        cacsmall = yf.Share('CACSR.PA')
    except :
        for _ in range(100):
            try:
                cac40 = yf.Share('PX1GR.PA')
                cacmid = yf.Share('CACMR.PA')
                cacsmall = yf.Share('CACSR.PA')
                break
            except:
                continue
    try:
        changecac40 = cac40.get_price()
        changecacmid = cacmid.get_price()
        changecacsmall = cacsmall.get_price()
    except:
        for _ in range(100):
            try:
                changecac40 = cac40.get_price()
                changecacmid = cacmid.get_price()
                changecacsmall = cacsmall.get_price()
                break
            except:
                changecac40 = cac40.get_price()
                changecacmid = cacmid.get_price()
                changecacsmall = cacsmall.get_price()
                continue
    return {'cac40': changecac40, 'cacmid': changecacmid, 'cacsmall': changecacsmall}

def plotPortfolioVsIndexes(file):
    df = pd.read_csv(file,sep = '\t')
    print(df)
    df['date'] = df['date'].apply(lambda X : datetime.datetime.strptime(X, "%Y-%m-%d").date())
    fig = pyplot.figure()
    pyplot.xlabel('time')
    pyplot.ylabel('change')
    pyplot.title('Changes of portfolio vs indexes over time')
    pyplot.plot(df['date'], df['total'], label="Portfolio", color = 'r')
    fig.autofmt_xdate()
    pyplot.plot(df['date'], df['cac40'], color = 'b', label = 'Cac 40 GR')
    pyplot.plot(df['date'], df['cacmid'], color = 'g', label = 'Cac Mid GR')
    pyplot.plot(df['date'], df['cacsmall'], color = 'm', label = 'Cac Small GR')
    fig.autofmt_xdate()
    pyplot.show()
    fig.savefig('accountvsindexes.png')

def main():
    if isbday(datetime.datetime.now()) :
        initial = 17231.72
        cash = 10.03
        stocks = ['SMTPC.PA', 'DG.PA', 'NXI.PA', 'COX.PA', 'ABCA.PA','IPH.PA']
        pru = [33.64054, 65.31130, 47.38463, 11.37695, 6.03034, 10.81]
        nbaction = [148, 61, 84, 46, 673, 64]
        my_port = {'Stock': stocks , 'PRU': pru,'Nb Action': nbaction}
        my_port = updatePortfolio(initial,my_port)
        updateStocksCsv('export_stocks.csv', my_port)
        account = computePortfolioYield(my_port, cash, initial)
        updateAccountCsv('export_account.csv', account)
        try :
            plotPortfolioVsIndexes('export_account.csv')
        except:
            print("Erreur")
            exit(1)
    else:
        print("Jour non-ouvré")
        exit(0)
if __name__ == '__main__':
    main()

