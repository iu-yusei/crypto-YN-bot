# crypto-YN-bot

Coincheck API と LINE Notify を利用した
仮想通貨自動売買 bot です。

取引履歴が LINE と trade.txt に出力されます。

## 環境

```shell
$ python -V
Python 3.9.1
```

## 準備

### API キーの発行

①[Coincheck](https://h.accesstrade.net/sp/cc?rk=0100nerr00l6g9)で API キーを発行する。

パーミッションは以下を選択。

- 新規注文
- 取引履歴
- 残高

※本人確認が必要です。

②[LINE Notify](https://notify-bot.line.me/ja/) トークンの発行

LINE トークンで発行したトークンを`main.py`に貼り付ける。

```python
token = "LINE Notifyで発行したAPIトークン"
```

### .env の配置

このリポジトリのルートディレクトリに.env を作成します。

以下のように os の環境変数を設定して.env というファイル名で配置します。

ここで設定した環境変数の値は、`environment.py`の`os.getenv('変数名')`で、取得します。

```
AMOUNT=
PROFIT=0.0
```

### システム環境変数の設定（Windows）

以下の項目をシステム環境変数として設定します。

ここで設定した環境変数の値は、`environment.py`の`os.environ['項目名']`で、取得します。

```
ACCESS_KEY=XXXXXXXXXXXXXXXX
API_SECRET=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
COIN=btc
INTERVAL=60
ALGORITHM=DIFFERENCE
SIMULATION=true
```

## 実行

```shell
./main.py
```

## 参考

下記ブログ記事を参考にして作成しました。

https://hikari-blog.com/coincheck-auto-trade/
