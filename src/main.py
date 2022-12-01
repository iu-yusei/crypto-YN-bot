import datetime
from email import message
from os import environ
import sys

from api import *
from algorithm import *
from dynamodb import *
import requests
##############################
# 環境変数チェック
##############################

# LINE NOTIFY
url = "https://notify-api.line.me/api/notify"
token = "LINE Notifyで発行したAPIトークン"
headers = {"Authorization": "Bearer " + token}


# 暗号通貨の判定
if not (environment.COIN == 'btc' or
        environment.COIN == 'etc' or
        environment.COIN == 'fct' or
        environment.COIN == 'mona'):
    print('Invalid coin.')
    sys.exit()

# アルゴリズムの判定
if not (environment.ALGORITHM == 'DIFFERENCE' or
        environment.ALGORITHM == 'BOLLINGER_BANDS' or
        environment.ALGORITHM == 'MACD' or
        environment.ALGORITHM == 'HYBRID' or
        environment.ALGORITHM == 'RSI' or
        environment.ALGORITHM == 'MIX'):
    print('Invalid algorithm.')
    sys.exit()

# レートを取得してみる(最低購入btcを設定)
res_json = get_rate('sell', 0.005, None)

# キーが有効であるか
is_valid_key = res_json['success']

# APIキーの判定
if not is_valid_key:
    print('Invalid API key.')
    sys.exit()

# 最小注文数量（円）
min_amount = 500
# BTCの場合は0.005以上からしか購入できない
if environment.COIN == 'btc':
    min_amount = float(res_json['price'])
    print('0.005btc=' + str(min_amount) + 'Yen')
    print('setting_jpy: ' + str(environment.simulation_jpy))
    print(environment.simulation)
    print('profit: ' + str(environment.profit))

if environment.simulation:
    print('------------------------------')
    print('####                      ####')
    print('####   Simulation Mode!   ####')
    print('####                      ####')
    print('------------------------------')
    print(environment.simulation_jpy)


# 購入金額の判定
amount = get_amount()
if amount < min_amount:
    print('Please specify more than ' + str(min_amount) + ' Yen')
    sys.exit()

print('ALGORITHM: ' + environment.ALGORITHM)
print('Buy ' + environment.COIN + ' for ' + str(amount) + ' Yen')

# シミュレーションではない場合
if not environment.simulation:
    print('##############################')
    print('####                      ####')
    print('####   Production Mode!   ####')
    print('####                      ####')
    print('##############################')

##############################
# メイン処理
##############################

# LINE 送信
message = 'START BOT\nALGORITHM:' + str(environment.ALGORITHM)
payload = {"message":  message}
r = requests.post(url, headers=headers, params=payload)
# 空のデータフレーム作り、サンプルデータを入れる
df = data_collecting(2 if environment.ALGORITHM == 'DIFFERENCE' else 25)

message = 'START TRADE\nALGORITHM:' + str(environment.ALGORITHM)
payload = {"message":  message}
r = requests.post(url, headers=headers, params=payload)
# 以下無限ループ
try:
    while True:
        # 最新の価格を取ってくる
        candle_stick = get_candle_stick()
        df = df.append({'open': candle_stick['open'], 'high': candle_stick['high'],
                       'low': candle_stick['low'], 'close': candle_stick['close'], }, ignore_index=True)

        buy_flg = False
        sell_flg = False

        if environment.ALGORITHM == 'DIFFERENCE':
            result = difference(df)
            buy_flg = result['buy_flg']
            sell_flg = result['sell_flg']
        elif environment.ALGORITHM == 'BOLLINGER_BANDS':
            result = bollinger_bands(df)
            buy_flg = result['buy_flg']
            sell_flg = result['sell_flg']
        elif environment.ALGORITHM == 'MACD':
            result = macd(df)
            buy_flg = result['buy_flg']
            sell_flg = result['sell_flg']
        elif environment.ALGORITHM == 'HYBRID':
            result = hybrid(df)
            buy_flg = result['buy_flg']
            sell_flg = result['sell_flg']
        elif environment.ALGORITHM == 'RSI':
            result = rsi(df)
            buy_flg = result['buy_flg']
            sell_flg = result['sell_flg']
        elif environment.ALGORITHM == 'MIX':
            result = mix(df)
            buy_flg = result['buy_flg']
            sell_flg = result['sell_flg']
        else:
            print('Invalid algorithm.')
            sys.exit()

        coin_amount = get_status()[environment.COIN]
        now_amount = df.iloc[-1]['close'] * coin_amount

        # ロスカット判定（購入金額と現在のBTCの価格の差が0より大きい場合）
        # loss_cut_flg =  0 < environment.market_buy_amount - now_amount
        # ロスカット判定（購入金額の1%を下回った場合）
        loss_cut_flg = environment.market_buy_amount * \
            0.01 < environment.market_buy_amount - now_amount

        print('////////////////')
        print('market_buy_amount:' + str(environment.market_buy_amount))
        print(now_amount)
        print('Buy amount(btc to jpy) - Now amount(btc to jpy) =')
        print(str(environment.market_buy_amount - now_amount) + '(btc to jpy)')
        print('SEll FLAG:')
        print(sell_flg)
        print('LOSS_CUT_FLAG:')
        print(loss_cut_flg)
        print('////////////////')

        # 買い注文実施判定
        buying = environment.order_id is None and buy_flg
        # 売り注文実施判定
        selling = environment.order_id is not None and (
            sell_flg or loss_cut_flg)

        if buying:
            # 買い注文実施
            with open('trade.txt', 'a') as f:
                print('', file=f)
                print("(っ'-')っ = 金金金 /  btc へ(^-^へ)", file=f)
                print('Execute a buy order!', file=f)
                print("(っ'-')っ = 金金金 /  btc へ(^-^へ)", file=f)
                print('', file=f)
                order_json = simulation_buy(
                    get_amount()) if environment.simulation else buy(get_amount())

                # 買い注文成功の場合
                if order_json is not None:
                    # オーダーIDをセット
                    environment.order_id = order_json['id']
                    # 購入金額をセット
                    environment.market_buy_amount = float(
                        order_json['market_buy_amount'])
                    # シミュレーションの場合
                    if environment.simulation:
                        environment.simulation_jpy -= get_amount()
                        environment.simulation_coin += float(
                            order_json['amount'])
                        # LINE送信
                        message = "\n(っ'-')っ = 金金金 /  btc へ(^-^へ)\nビットコインを購入!\n" + str(environment.simulation_coin) + \
                            "BTC\n(" + str(environment.market_buy_amount) + \
                            "円分)\n(っ'-')っ = 金金金 /  btc へ(^-^へ)"
                        payload = {"message": message}
                        r = requests.post(url, headers=headers, params=payload)

                    # 現在の時刻・金額を表示
                    print('', file=f)
                    print('/////// RECORDING D&T ////////', file=f)
                    dt_now = datetime.datetime.now()
                    time = dt_now.strftime('%Y/%m/%d %H:%M:%S')
                    status = get_status()
                    print(time + ' ' + str(status), file=f)
                    print('//////////////////////////////', file=f)
                    print('', file=f)

                    # LINE送信(シュミレーションモードじゃないとき)
                    account_balance = coinCheck.account.balance()
                    account_balance_json = json.loads(account_balance)
                    if not environment.simulation:
                        contract_btc = str(
                            account_balance_json[environment.COIN])
                        message = "\n(っ'-')っ = 金金金 /  btc へ(^-^へ)\nビットコインを購入!\n" + str(contract_btc) + \
                            "BTC\n(" + str(environment.market_buy_amount) + \
                            "円分)\n(っ'-')っ = 金金金 /  btc へ(^-^へ)"
                        payload = {"message": message}
                        r = requests.post(url, headers=headers, params=payload)

        elif selling:
            with open('trade.txt', 'a') as f:

                # loss_cut_flg =  0 < environment.market_buy_amount - now_amount
                print('////////////////')
                print('market_buy_amount:' +
                      str(environment.market_buy_amount), file=f)
                print(now_amount, file=f)
                print('Buy amount(btc to jpy) - Now amount(btc to jpy) =', file=f)
                print(str(environment.market_buy_amount -
                      now_amount) + '(btc to jpy)', file=f)
                print('SEll FLAG:', file=f)
                print(sell_flg, file=f)
                print('LOSS_CUT_FLAG(-1%):', file=f)
                print(loss_cut_flg, file=f)
                print('////////////////', file=f)

                # 売り注文実施
                print('', file=f)
                print("(っ'-')っ =btc /   金金金 へ(^-^へ)", file=f)
                print('Execute a sell order!', file=f)
                print("(っ'-')っ =btc /   金金金 へ(^-^へ)", file=f)
                print('', file=f)

                # 売る前に所有済みBTCを取得
                account_balance = coinCheck.account.balance()
                account_balance_json = json.loads(account_balance)
                before_sell_btc = account_balance_json[environment.COIN]

                order_json = simulation_sell() if environment.simulation else sell(environment.order_id)

                # 売り注文成功の場合
                if order_json is not None:
                    # オーダーIDを初期化
                    environment.order_id = None

                    # 利益を計算するためにレートを取得
                    order_rate_json = get_rate(
                        'sell', order_json['amount'], None)
                    # 今回の取引の利益
                    profit = float(
                        order_rate_json['price']) - environment.market_buy_amount
                    environment.profit += profit
                    environment.df_profit = environment.df_profit.append(
                        {'profit': profit}, ignore_index=True)

                    # DynamoDBに連携
                    set_result(environment.simulation,
                               environment.ALGORITHM, environment.INTERVAL, profit)

                    #  df_profitのlength調整
                    if len(environment.df_profit.index) > 4:
                        environment.df_profit = environment.df_profit.drop(
                            environment.df_profit.index[0])

                    print(environment.df_profit, file=f)
                    # 0.5%以上の損失を出しているか
                    loss = environment.market_buy_amount * 0.005 + profit
                    loss_flg = loss < 0
                    # 売上
                    result = environment.market_buy_amount + profit
                    # 基準量
                    base = environment.market_buy_amount

                    print('*********************************************', file=f)
                    print('market_buy_amount:' + str(environment.market_buy_amount) +
                          ', profit:' + str(profit), file=f)
                    print('*********************************************', file=f)

                    profit_rate = ((result / base) - 1) * 100
                    print('////------------------------------------////', file=f)
                    if(result < base):
                        print('profit_rate:' + '(-)' +
                              str(profit_rate) + '%', file=f)
                    else:
                        print('profit_rate:' + '(+)' +
                              str(profit_rate) + '%', file=f)
                    print('////------------------------------------////', file=f)

                    # シミュレーションの場合
                    if environment.simulation:
                        environment.simulation_jpy += float(
                            order_rate_json['price'])
                        message = "\n(っ'-')っ =btc /   金金金 へ(^-^へ)\nビットコインを売却!\n(っ'-')っ =btc /   金金金 へ(^-^へ)\n売却したbtc :" + str(environment.simulation_coin) + "BTC\n(" + str(environment.market_buy_amount) + \
                            '円分)\n当取引利益 :\n' + str(profit) + '円\n利益率: ' + str(profit_rate) + '%\n現在所持額:' + str(
                                environment.market_buy_amount) + '円\n総利益:' + str(environment.profit) + '円'
                        payload = {"message":  message}
                        r = requests.post(url, headers=headers, params=payload)

                        environment.simulation_coin = 0

                    # LINE送信(シュミレーションモードじゃないとき)

                    if not environment.simulation:
                        message = "\n(っ'-')っ =btc /   金金金 へ(^-^へ)\nビットコインを売却!\n(っ'-')っ =btc /   金金金 へ(^-^へ)\n\n売却したbtc :" + str(before_sell_btc) + "BTC\n(" + str(environment.market_buy_amount) + \
                            '円分)\n当取引利益 :\n' + str(profit) + '円\n利益率: ' + str(profit_rate) + '%\n現在所持額:' + str(
                                environment.market_buy_amount) + '円\n総利益:' + str(environment.profit) + '円'
                        payload = {"message": message}
                        r = requests.post(url, headers=headers, params=payload)

                    # 3連続の損失か
                    # https://note.nkmk.me/python-pandas-diff-pct-change/   b_diff
                    # 以下、Errorの原因
                    # environment.df_profit['diff'] = environment.df_profit.diff()
                    # print(environment.df_profit)
                    # down_flg = (environment.df_profit.iloc[-3]['diff'] < 0 and
                    #             environment.df_profit.iloc[-2]['diff'] < 0 and
                    #             environment.df_profit.iloc[-1]['diff'] < 0)
                    # print(down_flg)

                    # 購入金額初期化
                    environment.market_buy_amount = 0

                    # 1%以上の損失を出している、もしくは2連続で損失が出たら暴落の可能性があるので一時停止する
                    # if loss_flg or down_flg:
                    #     print('loss_flg: ' + str(loss_flg))
                    #     print(loss)
                    #     print('down_flg: ' + str(down_flg))
                    #     print(environment.df_profit)
                    stop_hour = 1
                    if loss_flg:
                        print('loss_flg: ' + str(loss_flg), file=f)
                        print(loss, file=f)
                        # print('down_flg: ' + str(down_flg))
                        print(environment.df_profit, file=f)

                        # LINE送信
                        message = '\n0.5%以上の損失！ (* □ *;)!!\n' + \
                            str(environment.INTERVAL) + 'min 取引を停止します'
                        payload = {"message": message}
                        r = requests.post(url, headers=headers, params=payload)

                        # シュミレーションモードではないとき（一時停止）
                        if not environment.simulation:
                            # 1時間停止
                            sleep(stop_hour)
                            # 一時停止した後なので初期化
                            environment.df_profit = pd.DataFrame() \
                                .append({'profit': profit, }, ignore_index=True) \
                                .append({'profit': profit, }, ignore_index=True) \
                                .append({'profit': profit, }, ignore_index=True)
                            # サンプルデータ作り直し（この後、先頭行を削除されるので+1）
                            df = data_collecting(
                                2 + 1 if environment.ALGORITHM == 'DIFFERENCE' else 25 + 1)
                            message = 'RESTART BOT'
                            payload = {"message": message}
                            r = requests.post(
                                url, headers=headers, params=payload)

                    # 現在の時刻・金額を表示
                    print('', file=f)
                    print('/////// RECORDING D&T ////////', file=f)
                    dt_now = datetime.datetime.now()
                    time = dt_now.strftime('%Y/%m/%d %H:%M:%S')
                    status = get_status()
                    print(time + ' ' + str(status), file=f)
                    print('//////////////////////////////', file=f)
                    print('', file=f)

        # 現在の時刻・金額を表示

        print('')
        print('/////// NOW Date & Time ////////')
        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y/%m/%d %H:%M:%S')
        status = get_status()
        print(time + ' ' + str(status))
        print('//////////////////////////////')
        print('')
        # 先頭行を削除してdfの長さを一定に保つ（長時間の運用時のメモリ対策）
        df = df.drop(df.index[0])

except KeyboardInterrupt:   # exceptに例外処理を書く
    # LINE送信
    message = 'PCで取引を中止しました'
    payload = {"message": message}
    r = requests.post(url, headers=headers, params=payload)
