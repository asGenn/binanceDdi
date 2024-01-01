import asyncio
from binance import AsyncClient
import pandas as pd
from datetime import datetime, timedelta
import pytz


async def get_data_price(symbol, timestamp):
    client = await AsyncClient.create("y40aH01LqjVLosfHyBpJtJQ2vQ3bRAvdSa7a2GylqUNH1TPbN7937PyD6GSKnrRS", "yIqvbp3s7yHumADQLyYznsxGVBD4eVSDzrxdPxfQGmQbQKpR5WOOtoRrdqme19H0")
    try:
        interval = AsyncClient.KLINE_INTERVAL_12HOUR
        timestamp_unix = int(timestamp.timestamp())
        start_time = datetime.fromtimestamp(timestamp_unix)
        local_tz = pytz.timezone("Europe/Istanbul")
        start_time_utc = (local_tz.localize(start_time) -
                          timedelta(hours=12)).astimezone(pytz.utc)
        end_time_utc = (local_tz.localize(start_time) +
                        timedelta(hours=12)).astimezone(pytz.utc)
        start_time_utc_str = start_time_utc.strftime("%Y-%m-%d %H:%M:%S")
        end_time_utc_str = end_time_utc.strftime("%Y-%m-%d %H:%M:%S")
        lines = await client.get_historical_klines(symbol, interval, start_time_utc_str, end_time_utc_str)
        df = pd.DataFrame(lines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time",
                                          "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
        toplam = float(df["close"].iloc[1]) - float(df["close"].iloc[0])
        return toplam
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        await client.close_connection()


def convert_to_list(string):
    if string == "[]":
        return []
    temizlenmis_ifade = string.replace(
        "[", "").replace("]", "").replace("'", "")
    liste = temizlenmis_ifade.split(", ")
    return liste


async def tag_data(row):
    symbol_list = convert_to_list(row["symbols"])
    tagList = []

    if len(symbol_list) > 0:

        for symbol in symbol_list:
            newSymbol = symbol + "USDT"
            toplam = await get_data_price(newSymbol, row["date"])

            if toplam < 0:
                tagList.append(-1)
            elif toplam > 0:
                tagList.append(1)

    elif len(symbol_list) == 0:
        symbol_list.extend(["BTC", "ETH", "FDUSD"])
        for idx, symbol in enumerate(symbol_list):
            newSymbol = symbol + "USDT"
            toplam = await get_data_price(newSymbol, row["date"])
            if toplam < 0:
                tagList.append(-1)
            elif toplam > 0:
                tagList.append(1)
    tagValue = sum(tagList)
    if tagValue < 0:
        return -1
    elif tagValue > 0:
        return 1
    else:
        return 0

index = 0


async def add_tag_to_exel():

    df = pd.read_excel('excelFiles/newsData2.xlsx')
    for index, row in df.iterrows():
        try:
            if row["new_tag"] == 0:
                df.at[index, "new_tag"] = await tag_data(row)
                print(f"index: {index}, Tag: {df['new_tag'].iloc[index]} old tag :{
                    df['tag'].iloc[index]},symbols: {df['symbols'].iloc[index]}"
                )
                await asyncio.sleep(1.5)
                if index == len(df) - 1:
                    break
        except Exception as e:
            print(f"Hata: {e}")

    df.to_excel('excelFiles/newsData2.xlsx', index=False)


if __name__ == "__main__":
    asyncio.run(add_tag_to_exel())
