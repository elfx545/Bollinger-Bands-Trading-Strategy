"""
    Title: Buy and Hold (NYSE)
    Description: This is a Bollinger Bands Trading Strategy. When the equity goes below the Bollinger Lower bond, we buy it. 
    When the equity goes above the Bollinger Upper bond, we sell it.
    Style tags: Systematic
    Asset class: Equities, 
    Dataset: US Equities
"""
from blueshift.api import(    symbol,
                            order_target_percent,
                            schedule_function,
                            date_rules,
                            time_rules,
                            record,
                       )

import numpy as np

def initialize(context):
    context.nflx = symbol('NFLX')


    
    # Call rebalance function on the first trading day of each month after 2.5 hours from market open
    schedule_function(check_bands,
                    date_rules.month_start(days_offset=0),
                    time_rules.market_close(hours=1, minutes=0))


def check_bands(context,data):
    nflx = context.nflx

    cur_price = data.current(nflx, columns='close')
    prices = data.history(nflx, 'close', 20, '1d')


    mavg_20 = np.mean(prices)
    std_20 = np.std(prices)

    bollinger_upper = mavg_20 + 2*std_20
    bollinger_lower = mavg_20 - 2*std_20
        

    if cur_price > bollinger_upper :
        order_target_percent(nflx, -1)
        print('Shorting')
        print('Current price is : '+ str(cur_price))
        print('Lower band is : '+ str(bollinger_upper))
    elif cur_price < bollinger_lower :
        order_target_percent(nflx, 1)
        print('Buying')
        print('Current price is : '+ str(cur_price))
        print('Lower band is : '+ str(bollinger_lower))
    else : 
        pass


    record(upper=bollinger_upper,
           lower=bollinger_lower,
           mavg_20=mavg_20,
           price=cur_price)


     
