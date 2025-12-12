"""Grid strategy
1. comparing tech stock between them
2. comparing tech stocks with crypto
3. comparing results with S&P500 index

Analyze indicators for stocks. PE ratio, volume, revenue reports

Tasks:
1. add the grid percentage into the function
2. add the stock name into the function. Goal is to have a function that requires two arguments, one for the ticker, one for the grid distance
3. use airflow to get using beautiful soup, the intra data, and add it in our

libraries to use:
1. pandas
2. matplotlib/seaborn
3. airflow
"""
# getting data from yahoo finance, for the stock that I am interested in, for the last 5 years

import yfinance as yf
import pandas as pd

#Analysis steps:
# for each day, if the price in in the current_stock_price +- 10%, then eiter sell, or buy. 
# if not, the go to next day

#Defining main function
def grid_strategy_closed_positions(stock_symbol, grid_space_percentage, ticker_year_history):
     # Define the ticker symbol
    ticker_symbol = stock_symbol

    # Get the data for the last 5 years
    stock_data = yf.download(ticker_symbol, period=ticker_year_history)

    #changing index from timestamp to date
    stock_data.index = stock_data.index.date
    
    # get the open price from the first day
    positions_open = []
    positions_closed = []
    first_stock_price = stock_data.loc[stock_data.index.min(),'Open'].item()
    positions_open.append(first_stock_price)
    upper_grid_percentage = 1*grid_space_percentage
    lower_grid_percentage = 1*(1-grid_space_percentage)
    for day_num in range(len(stock_data.index)-1):
        # if the price * 10% is between the next day's low and high price, then add the new price to a list, as a list, with the price and date. same if it's lower with 10%, add it to a list
        next_day_low_price = stock_data.iloc[day_num+1, 2].item()
        next_day_high_price = stock_data.iloc[day_num+1, 1].item()
        #print(f"Day is: {day_num}, next day low price is: {next_day_low_price}, next day high price is: {next_day_high_price}")
        for position in positions_open:
            #print(f"trade open: {position}, total positions open: {positions_open}, position*1.1: {position*1.1}, position*0.9: {position*0.9} ")
            if position*1.1 >= next_day_low_price and position*upper_grid_percentage <= next_day_high_price:
                #sell and add in list
                positions_closed.append(position*upper_grid_percentage)
                #print(f"positions closed list: {positions_closed}")
                positions_open.append(position*upper_grid_percentage)
                #print(f"positions open list: {positions_open}")
                positions_open.remove(position)
            if min(positions_open)*lower_grid_percentage >= next_day_low_price and min(positions_open)*lower_grid_percentage <= next_day_high_price:
            # these will become two dataframes, with the date and value of taking profit and buying
                if min(positions_open)*0.9 not in positions_open: 
                    positions_open.append(min(positions_open)*lower_grid_percentage)
            if position*1.1 < next_day_low_price:
                positions_closed.append(position*upper_grid_percentage)
                positions_open.append(next_day_low_price)
                positions_open.remove(position)
    print(f"number of positions closed:{len(positions_closed)}")
    return len(positions_closed)

tsla_grid = grid_strategy_closed_positions('TSLA', 0.1, '1y')