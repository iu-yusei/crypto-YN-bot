from os import environ
from api import *

# CoinCheck.DEBUG = True
# CoinCheck.DEBUG_LEVEL = logging.DEBUG
coinCheck = CoinCheck(os.environ['ACCESS_KEY'], os.environ['API_SECRET'])

import requests

url = "https://notify-api.line.me/api/notify" 
token = "kPc4ak612IeFM3YCQ4SwOUeNGE4aktN2Sejxel81H29"
print(token)
headers = {"Authorization" : "Bearer "+ token} 
# message =  "FIRST MESSAGE" 
# payload = {"message" :  message} 
# r = requests.post(url, headers = headers, params=payload)
print(environment.AMOUNT)
print(get_status())


print(environment.market_buy_amount * 0.01)
print(environment.market_buy_amount )

# Public API
# res = coinCheck.ticker.all()
# res = coinCheck.trade.all()
# res = coinCheck.order_book.all()

# Private API
# params = {}
# params = {
#     'pair': 'btc_jpy', # ビットコインが
#     'stop_loss_rate': 2850, # この価格以上になったら
#     'rate': 2850, # この価格で
#     'amount': 0.00508771, # この口数で
#     'order_type': 'buy' # 買いを入れる
# }

# 新規注文
# res = coinCheck.order.create(params);
# 未決済の注文一覧
# res = coinCheck.order.opens(params);


# params = {
#     'id': '2953613'
# }

# 注文のキャンセル
# res = coinCheck.order.cancel(params);
# 取引履歴
# res = coinCheck.order.transactions(params);

# res = coinCheck.leverage.positions();
# params = {'status': 'open'}
# res = coinCheck.leverage.positions(params);

# res = coinCheck.account.balance(params);
# res = coinCheck.account.leverage_balance(params);
# res = coinCheck.account.info(params);

# params = {
#     'address': '1Gp9MCp7FWqNgaUWdiUiRPjGqNVdqug2hY',
#     'amount': '0.0002'
# };
# res = coinCheck.send.create(params);
# params = {
#     'currency': "BTC"
# };
# res = coinCheck.send.all(params);

# params = {
#     'currency': 'BTC'
# };
# res = coinCheck.deposit.all(params);
# params = {
#     'id': 2222
# };
# res = coinCheck.deposit.fast(params);

# res = coinCheck.bank_account.all(params);
# params = {
#     'bank_name': "田中 田中",
#     'branch_name': "田中 田中",
#     'bank_account_type': "futsu",
#     'number': "1234567",
#     'name': "田中 田中"
# };
# res = coinCheck.bank_account.create(params);
# params = {
#     'id': 2222
# };
# res = coinCheck.bank_account.delete(params);

# res = coinCheck.withdraw.all(params);
# params = {
#     'bank_account_id': 2222,
#     'amount': 50000,
#     'currency': 'JPY',
#     'is_fast': False
# };
# res = coinCheck.withdraw.create(params);
# params = {
#     'id': 2222
# };
# res = coinCheck.withdraw.cancel(params);

# params = {
#     'amount': '0.01',
#     'currency': 'BTC'
# };
# res = coinCheck.borrow.create(params);
# res = coinCheck.borrow.matches(params);
# params = {
#     'id': '1135'
# };
# res = coinCheck.borrow.repay(params);

# params = {
#     'amount': 100,
#     'currency': 'JPY'
# };
# res = coinCheck.transfer.to_leverage(params);
# params = {
#     'amount': 100,
#     'currency': 'JPY'
# };
# res = coinCheck.transfer.from_leverage(params);
# print('profit: ' + str(environment.profit))
# profit = environment.profit
# df_profit = pd.DataFrame() \
#     .append({'profit': 1, }, ignore_index=True) \
#     .append({'profit': 2, }, ignore_index=True) \
#     .append({'profit': 4, }, ignore_index=True) \
    # .append({'profit': 6, }, ignore_index=True) \
    # .append({'profit': 12, }, ignore_index=True) \
    # .append({'profit': 14, }, ignore_index=True) \
    # .append({'profit': 20, }, ignore_index=True) 

# if len(df_profit.index) > 4:
#     df_profit = df_profit.drop(df_profit.index[0])
            
# df_profit['diff'] = df_profit.diff()
# print(df_profit)


# account_balance = coinCheck.account.balance()
# account_balance_json = json.loads(account_balance)
# print(account_balance_json)
# print(account_balance_json['jpy'])
# print(environment.COIN)
# print("売却したbtc :" + str(account_balance_json[environment.COIN]) +"BTC\n("+ str(environment.market_buy_amount) + '円分')
# last = json.loads(coinCheck.ticker.all())['last']
# res = get_latest_trading_rate()
# print('\nThe result:')
# print(last)
# print(res)



# transactions = coinCheck.order.transactions()
# for transaction in json.loads(transactions)['transactions']:
#     print(transaction['funds'][environment.COIN])