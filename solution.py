from binance.spot import Spot
import json
from prometheus_client import start_http_server, Summary, Gauge
import time

# global vars
delta_calculation_count = 0
prev_spread = {}
init_obj = []

def five_assest_cat(q_asset, f_type):
    client = Spot()
    l_sym = []
    d_sym = {}
    exinfo_response = json.loads(json.dumps(client.exchange_info()))
    t24hr_response = client.ticker_24hr()
    for sym in exinfo_response["symbols"]:
        if sym["quoteAsset"] == q_asset:
            l_sym.append(sym["symbol"])
    for asst in t24hr_response:
        if (asst['symbol'] in l_sym):
            d_sym[asst['symbol']] = asst[f_type]
    return sorted(d_sym.items(), key=lambda x: float(x[1]), reverse=True)[:5]

def nation_value_200(dict_sym):
    client = Spot()
    total_national_bids = 0
    total_national_asks = 0
    d_nation_bids_sum = {}
    d_nation_asks_sum = {}
    for i in dict_sym:
        depth = client.depth(i[0],limit=200)
        for item in depth['bids']:
            nation_value = float(item[0]) * float(item[1])
            total_national_bids += nation_value
        d_nation_bids_sum[i[0]] = total_national_bids
        for item in depth['asks']:
            nation_value = float(item[0]) * float(item[1])
            total_national_asks += nation_value
        d_nation_asks_sum[i[0]] = total_national_asks
    return (d_nation_bids_sum, d_nation_asks_sum)

def price_spread(dict_sym):
    client = Spot()
    d_price_spread = {}
    for i in dict_sym:
        d_price_spread[i[0]] = float(client.book_ticker(i[0])["askPrice"]) - float(client.book_ticker(i[0])["bidPrice"])
    return d_price_spread

def q4_detla_every_n(price_spread_op):
    global delta_calculation_count
    d_delta = {}
    global prev_spread
    current_spread = price_spread_op
    if delta_calculation_count == 0:
        prev_spread = current_spread
    for key in current_spread:
        d_delta[key] = float(current_spread[key]) - float(prev_spread[key])
    prev_spread = current_spread
    delta_calculation_count += 1
    return d_delta

def gauge_for_sym(delta_dict):
    global init_obj
    for key in delta_dict:
        init_obj.append(Gauge("delta_symbol_"+key,"Absolute delta from previous values for the symbol: "+key,[key]))
    return init_obj

def prom_func(delta_dict, l_init_obj):
    update_counter = 0
    for key in delta_dict:
        l_init_obj[update_counter].labels(key).set(delta_dict[key])
        update_counter+=1

if __name__ == '__main__':
    try:
        # ans Q1
        q1_ans = five_assest_cat("BTC", "volume")
        print("q1_ans")
        print(q1_ans)
        # ans Q2
        q2_ans = five_assest_cat("USDT", "count")
        print("q2_ans")
        print(q2_ans)
        # ans Q3 (retruns the two dicts of nation value for bid and ask)
        q3_ans = nation_value_200(q1_ans)
        print("q3_ans")
        print(q3_ans)
        # ans Q4
        q4_ans = price_spread(q2_ans)
        print("q4_ans")
        print(q4_ans)
        # metrics exporter for Q6
        start_http_server(8080)
        gauge_for_sym(q4_detla_every_n(q4_ans))
        while True:
            # ans Q5 (we can not pass q4_ans directlya s it has to check delta with a current price spread)
            q5_ans = q4_detla_every_n(price_spread(q2_ans))
            print("q5_ans")
            print(q5_ans)
            # ans Q6 (does not print anything but exports metrics over port 8080)
            prom_func(q5_ans,init_obj)
            time.sleep(10)
    except:
        print("Something around corner cases, please check the crash logs")
