# getting data from yahoo finance, for the stock that I am interested in, for the last 5 years

import yfinance as yf
import pandas as pd

def get_stock_data(stock_symbol):
    # Define the ticker symbol
    ticker_symbol = stock_symbol

    # Get the data for the last 5 years
    stock_data = yf.download(ticker_symbol, period='2y')

    return stock_data

df_tsla = get_stock_data('TSLA')  # Example usage for Tesla

# get the open price from the first day
positions_open = []
positions_closed = []
first_stock_price = df_tsla.loc[df_tsla.index.min(),'Open'].item()
positions_open.append(first_stock_price)
for day_num in range(len(df_tsla.index)-1):
    # if the price * 10% is between the next day's low and high price, then add the new price to a list, as a list, with the price and date. same if it's lower with 10%, add it to a list
    next_day_low_price = df_tsla.iloc[day_num+1, 2].item()
    next_day_high_price = df_tsla.iloc[day_num+1, 1].item()
    #print(f"Day is: {day_num}, next day low price is: {next_day_low_price}, next day high price is: {next_day_high_price}")
    for position in positions_open:
        #print(f"trade open: {position}, total positions open: {positions_open}, position*1.1: {position*1.1}, position*0.9: {position*0.9} ")
        if position*1.1 >= next_day_low_price and position*1.1 <= next_day_high_price:
            #sell and add in list
            positions_closed.append(position*1.1)
            #print(f"positions closed list: {positions_closed}")
            positions_open.append(position*1.1)
            #print(f"positions open list: {positions_open}")
            positions_open.remove(position)
        if min(positions_open)*0.9 >= next_day_low_price and min(positions_open)*0.9 <= next_day_high_price:
        # these will become two dataframes, with the date and value of taking profit and buying
            if min(positions_open)*0.9 not in positions_open: 
                positions_open.append(min(positions_open)*0.9)
        if position*1.1 < next_day_low_price:
            positions_closed.append(position*1.1)
            positions_open.append(next_day_low_price)
            positions_open.remove(position)