import csv
import matplotlib.pyplot as plt
import talib
import numpy as np

csvfile = file('../data/originalData/'+'000905_close'+'.csv', 'rb')
reader = csv.reader(csvfile)

close = []
for line in reader:
    close.append(float(line[1]))

date = range(len(close))

macd,macdsignal,x = talib.MACD(np.array(close))

plt.plot(date,macd)
plt.plot(date,macdsignal)
plt.plot(date,close)

plt.show()