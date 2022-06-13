from datetime import datetime
import ccxt
import numpy as np
import pandas as pd

import schedule
import time


exchangesData = {
    "hitbtc": {
        "apiKey": "x1znbG2VSBnkkUQPfW2TCiyGw8v4Worc",
        "secret": "eEi3tzRpRcptRH3C1LRw5bpYXP6UlzJW",
        "transactionFee": 0.001
    },
    "binance": {
        "apiKey": "Xx4SFzJwRWC2VdRy055JzCYsrLoBFccp1akEPXuImuapcnrbgVuvlZHJXGbIsB9a",
        "secret": "a7Annf1tu6xqU1Y4eHUcTyH5zqAkxrg4SsorNnCEzbFIQMuaJtrhSgjb6idCLt2E",
        "transactionFee": 0.001
    },
    "kucoin": {
        "apiKey": "6287e8b93d6fab00017e4a01",
        "secret": "ac2858ba-9044-411d-8311-945d8a02f106",
        "password": "4aqMU56dKixFe6y",
        "transactionFee": 0.0025
    },

    "bitmart": {
        "apiKey": "497e745aaa507c1ed800644a8b3f62e9f4352065",
        "secret": "125528a6732c4855bdd27bf0ec4130aa85adab057e911fa73096eb09bde3e31f",
        "transactionFee": 0.002
    },

    #  "coinbase": {
    #     "apiKey": "frB5zzPZDgvHnZo1",
    #     "secret": "S0kFDaKX3Uopa5yfgY2Job5vhxxVR2OU",
    #     "transactionFee": 0.0025
    # },

    #    "Coinbase Pro": {
    #     "apiKey": "",
    #     "secret": "",
    #     "transactionFee": 0.002
    # },
}

binance_balance = ccxt.binance({
    "apiKey": "Xx4SFzJwRWC2VdRy055JzCYsrLoBFccp1akEPXuImuapcnrbgVuvlZHJXGbIsB9a",
    "secret": "a7Annf1tu6xqU1Y4eHUcTyH5zqAkxrg4SsorNnCEzbFIQMuaJtrhSgjb6idCLt2E",
})

kucoin_balance = ccxt.kucoin({
    "apiKey": "6287e8b93d6fab00017e4a01",
    "secret": "ac2858ba-9044-411d-8311-945d8a02f106",
    "password": "4aqMU56dKixFe6y",
})

hitbtc_balance = ccxt.hitbtc({
    "apiKey": "x1znbG2VSBnkkUQPfW2TCiyGw8v4Worc",
    "secret": "eEi3tzRpRcptRH3C1LRw5bpYXP6UlzJW",
})

bitmart_balance = ccxt.bitmart({
        "apiKey": "497e745aaa507c1ed800644a8b3f62e9f4352065",
        "secret": "125528a6732c4855bdd27bf0ec4130aa85adab057e911fa73096eb09bde3e31f",
})
min_spread = 1
min_profit = 1


def main():
    exchanges = [
        "hitbtc",
        "binance",
        "kucoin",
        "bitmart",

        # "coinbase",
        # "coinbase pro",
        # "bittrex",
        # "poloniex",
        # # "exmo",
        # # "bitmex",
        # # "huobi",
    ]

    symbols = [
        "GST/USDT",
        "SAITAMA/USDT",
        "TRX/USDT",
        "BTC/USDT",
        "ETH/USDT",
        # "BNB/USDT",
        "SOL/USDT",
        "XRP/USDT",
        # "ADA/USDT",
        "AVAX/USDT",
        "APE/USDT",
        "FMT/USDT",
        "ETC/USDT",
        "NEAR/USDT",
        "BETA/USDT",
        # "CHAIN LINK/USDT",
    ]

    min_ask_exchange_id = ""
    min_ask_price = 99999999

    max_bid_exchange_id = ""
    max_bid_price = 5

    exchange_symbol = ""
    max_increase_percentage = 0.0

    for symbol in symbols:
        print("------------------------------")
        print("***WELCOME TO Fastarbit-ModTrizyx BOT***")
        print("------------------------------")
        balance_binance = binance_balance.fetch_balance()
        balance_kucoin = kucoin_balance.fetch_balance()
        balance_hitbtc = hitbtc_balance.fetch_balance()
        exchange = ccxt.hitbtc()
        print('USDT, Binance:', (balance_binance['total']['USDT']))
        print('USDT, Kucoin:', (balance_kucoin['total']['USDT']))
        print('USDT, HITBTC:', (balance_hitbtc['total']['USDT']))
        # print('ETH:',(balance['total']['ETH']))
        # print('BCH:',(balance['total']['BCH']))
        # # print('NFT:',(balance['total']['NFT']))
        # print('LTC:',(balance['total']['LTC']))
        # print('BTC:',(balance['total']['BTC']))
        # print('SOL:',(balance['total']['SOL']))
        # print('VET:',(balance['total']['VET']))
        # print('BTS:',(balance['total']['BTS']))
        # print('SHIB:',(balance['total']['SHIB']))
        # bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='1m', limit=30)
        # print(bars)
        # print(ccxt.exchanges)
        print("Searching for the best opportunity for {0} on {1}".format(
            symbol, exchanges))

        ask_exchange_id, ask_price, bid_exchange_id, bid_price = get_biggest_spread_by_symbol(
            exchanges, symbol)
        increase_percentage = (bid_price - ask_price) / ask_price * 100

        print("[{0} - {1}] - [{2}] - Price Spread: {3:.2}%".format(ask_exchange_id,
                                                                   bid_exchange_id, symbol, increase_percentage))

        if increase_percentage > max_increase_percentage:
            exchange_symbol = symbol
            max_increase_percentage = increase_percentage
            min_ask_exchange_id = ask_exchange_id
            min_ask_price = ask_price
            max_bid_exchange_id = bid_exchange_id
            max_bid_price = bid_price

        if increase_percentage >= min_spread:
            break
    print("-----------------------------")

    if max_increase_percentage > 0:
        print("\n----------Settings-----------")
        ask_amount = get_min_amount(min_ask_exchange_id, exchange_symbol)
        print("Min Ask amount: {0}".format(ask_amount))
        bid_amount = get_min_amount(max_bid_exchange_id, exchange_symbol)
        print("Min Bid amount: {0}".format(bid_amount))
        amount = max(ask_amount, bid_amount)
        print("Actual amount: {0}".format(amount))
        print("Min spread percentage: {0}%".format(min_spread))
        print("Min profit: {0}%".format(min_profit))

        print("\n--------Best Spread----------")
        print("[{0} - {1}] - [{2}]: Spread percentage: {3:.2}%".format(min_ask_exchange_id,
                                                                       max_bid_exchange_id, exchange_symbol,
                                                                       max_increase_percentage))

        print("\n-----Market Opportunity------")
        print("Buy {0} {1} from {2} at {3} {4}".format(amount, exchange_symbol.split(
            "/")[0], min_ask_exchange_id, min_ask_price, exchange_symbol.split("/")[0]))
        print("Sell {0} {1} on {2} at {3} {4}".format(amount, exchange_symbol.split(
            "/")[0], max_bid_exchange_id, max_bid_price, exchange_symbol.split("/")[0]))

        print("\n-------------Fees------------")
        min_ask_fee = min_ask_price * amount * \
                      exchangesData[min_ask_exchange_id]["transactionFee"]
        print("[{0}] - Trading Fee: {1}% = {2:.4} {3}".format(min_ask_exchange_id,
                                                              exchangesData[min_ask_exchange_id][
                                                                  "transactionFee"] * 100, min_ask_fee,
                                                              exchange_symbol.split("/")[0]))
        max_bid_fee = max_bid_price * amount * \
                      exchangesData[max_bid_exchange_id]["transactionFee"]
        print("[{0}] - Trading Fee: {1}% = {2:.4} {3}".format(max_bid_exchange_id,
                                                              exchangesData[max_bid_exchange_id][
                                                                  "transactionFee"] * 100, max_bid_fee,
                                                              exchange_symbol.split("/")[0]))

        print("\n-----------Profit------------")
        cost = amount * min_ask_price
        print("You will have to spend: {0:.4} {1}".format(
            cost, exchange_symbol.split("/")[1]))
        profit = ((max_bid_price - min_ask_price) * amount) - \
                 (max_bid_fee + min_ask_fee)
        print("You will make {0:.4} {1} profit(including fees)".format(
            profit, exchange_symbol.split("/")[1]))

        print("\n-----------Buy/Sell----------")
        if profit >= min_profit:
            place_buy_sell_order(min_ask_exchange_id, min_ask_price,
                                 max_bid_exchange_id, max_bid_price, exchange_symbol, amount)
        else:
            print("It seems like you won't make enough profit :(")
    else:
        print("It seems like there are no opportunities at the moment :(")


def get_min_amount(exchange_id, symbol):
    exchange = eval("ccxt.{0}()".format(exchange_id))

    exchange.load_markets()

    return float(exchange.markets[symbol]["limits"]["amount"]["min"])


def place_buy_sell_order(ask_exchange_id, ask_price, bid_exchange_id, bid_price, symbol, amount):
    # buy
    ask_exchange = eval("ccxt.{0}()".format(ask_exchange_id))
    ask_exchange.apiKey = exchangesData[ask_exchange_id]["apiKey"]
    ask_exchange.secret = exchangesData[ask_exchange_id]["secret"]
    print("Placing a Buy order on {0} for {1} {2} at price: {3}".format(
        ask_exchange_id, amount, symbol.split("/")[0], ask_price))

    # It will cost you a fee if you want to use `create_market_buy_order`
    ask_exchange.create_market_buy_order(symbol, amount, {'trading_agreement': 'agree'})
    ask_exchange.create_limit_buy_order(symbol, amount, ask_price)

    # sell
    bid_exchange = eval("ccxt.{0}()".format(bid_exchange_id))
    bid_exchange.apiKey = exchangesData[bid_exchange_id]["apiKey"]
    bid_exchange.secret = exchangesData[bid_exchange_id]["secret"]

    # bid_exchange.password = exchangesData[bid_exchange_id]["password"]
    print("Placing a Sell order on {0} for {1} {2} at price: {3}".format(
        bid_exchange_id, amount, symbol.split("/")[0], bid_price))
        
    # It will cost you a fee if you want to use `create_market_buy_order`
    bid_exchange.create_market_buy_order(symbol, amount, {'trading_agreement': 'agree'})
    bid_exchange.create_limit_sell_order(symbol, amount, bid_price)


def get_biggest_spread_by_symbol(exchanges, symbol):
    ask_exchange_id = ""
    min_ask_price = 99999999

    bid_exchange_id = ""
    max_bid_price = 0

    for exchange_id in exchanges:
        exchange = eval("ccxt.{0}()".format(exchange_id))

        try:
            order_book = exchange.fetch_order_book(symbol)
            bid_price = order_book['bids'][0][0] if len(
                order_book['bids']) > 0 else None
            ask_price = order_book['asks'][0][0] if len(
                order_book['asks']) > 0 else None

            if ask_price < min_ask_price:
                ask_exchange_id = exchange_id
                min_ask_price = ask_price
            if bid_price > max_bid_price:
                bid_exchange_id = exchange_id
                max_bid_price = bid_price

            increase_percentage = (bid_price - ask_price) / ask_price * 100
            if increase_percentage >= 1:
                return ask_exchange_id, min_ask_price, bid_exchange_id, max_bid_price
        except:
            # pass
            print("")
            print("{0} - There is an error!".format(exchange_id))

    min_ask_price += 0.235
    max_bid_price -= 0.235

    return ask_exchange_id, min_ask_price, bid_exchange_id, max_bid_price


def get_exchanges_by_symbol(exchanges, symbol_to_find):
    for exchange_id in exchanges:
        exchange = eval("ccxt.{0}()".format(exchange_id))

        exchange.load_markets(True)

        for symbol in exchange.symbols:
            if symbol == symbol_to_find:
                print("{0} - {1} [OK]".format(exchange_id, symbol))
# sleep for 5 seconds the first time linking an account
# time.sleep(5)

if __name__ == "__main__":
    main()
