from datetime import datetime
import numpy as np
import talib
import alpaca_trade_api as api
import pandas
import time as time
import os


# Creates dataset folders in directory script is run from
try:
    os.stat("./train")
    os.stat("./eval")
except BaseException:
    os.mkdir("./train")
    os.mkdir("./eval")


# api = tradeapi.REST(key_id= < your key id >, secret_key= < your secret
# key > )

barTimeframe = "1D"  # 1Min, 5Min, 15Min, 1H, 1D

assetList = np.loadtxt(
    "assetList.txt",
    comments="#",
    delimiter=",",
    unpack=False,
    dtype="str")

# ISO8601 date format
trainStartDate = "2015-01-01T00:00:00.000Z"
trainEndDate = "2017-06-01T00:00:00.000Z"
evalStartDate = "2017-06-01T00:00:00.000Z"
evalEndDate = "2018-06-01T00:00:00.000Z"

targetLookaheadPeriod = 1
startCutoffPeriod = 50  # Set to length of maximum period indicator


# Tracks position in list of symbols to download
iteratorPos = 0
assetListLen = len(assetList)

while iteratorPos < assetListLen:
    try:
        symbol = assetList[iteratorPos]

        # Returns market data as a pandas dataframe
        returned_data = api.get_bars(
            symbol,
            barTimeframe,
            start_dt=trainStartDate,
            end_dt=evalEndDate).df

        # Processes all data into numpy arrays for use by talib
        timeList = np.array(returned_data.index)
        openList = np.array(returned_data.open, dtype=np.float64)
        highList = np.array(returned_data.high, dtype=np.float64)
        lowList = np.array(returned_data.low, dtype=np.float64)
        closeList = np.array(returned_data.close, dtype=np.float64)
        volumeList = np.array(returned_data.volume, dtype=np.float64)

        # Adjusts data lists due to the reward function look ahead period
        shiftedTimeList = timeList[:-targetLookaheadPeriod]
        shiftedClose = closeList[targetLookaheadPeriod:]
        highList = highList[:-targetLookaheadPeriod]
        lowList = lowList[:-targetLookaheadPeriod]
        closeList = closeList[:-targetLookaheadPeriod]

        # Calculate trading indicators
        RSI14 = talib.RSI(closeList, 14)
        RSI50 = talib.RSI(closeList, 50)
        STOCH14K, STOCH14D = talib.STOCH(
            highList, lowList, closeList, fastk_period=14, slowk_period=3, slowd_period=3)

        # Calulate network target/ reward function for training
        closeDifference = shiftedClose - closeList
        closeDifferenceLen = len(closeDifference)

        # Creates a binary output if the market moves up or down, for use as
        # one-hot labels
        longOutput = np.zeros(closeDifferenceLen)
        longOutput[closeDifference >= 0] = 1
        shortOutput = np.zeros(closeDifferenceLen)
        shortOutput[closeDifference < 0] = 1

        # Constructs the dataframe and writes to CSV file
        outputDF = {
            "close": closeList,  # Not to be included in network training, only for later analysis
            "RSI14": RSI14,
            "RSI50": RSI50,
            "STOCH14K": STOCH14K,
            "STOCH14D": STOCH14D,
            "longOutput": longOutput,
            "shortOutput": shortOutput
        }
        # Makes sure the dataframe columns don't get mixed up
        columnOrder = ["close", "RSI14", "RSI50", "STOCH14K",
                       "STOCH14D", "longOutput", "shortOutput"]
        outputDF = pandas.DataFrame(
            data=outputDF,
            index=shiftedTimeList,
            columns=columnOrder)[
            startCutoffPeriod:]

        # Splits data into training and evaluation sets
        trainingDF = outputDF[outputDF.index < evalStartDate]
        evalDF = outputDF[outputDF.index >= evalStartDate]

        if (len(trainingDF) > 0 and len(evalDF) > 0):
            print("writing " + str(symbol) +
                  ", data len: " + str(len(closeList)))

            trainingDF.to_csv("./train/" + symbol + ".csv", index_label="date")
            evalDF.to_csv("./eval/" + symbol + ".csv", index_label="date")
    except BaseException:
        pass

    time.sleep(5)  # To avoid API rate limits
    iteratorPos += 1
