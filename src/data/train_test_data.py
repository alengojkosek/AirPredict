import pandas as pd
import numpy as np

# Preberemo podatke iz datoteke
data = pd.read_csv("current_data.csv")

# Ustvarimo stolpec s časovnimi oznakami
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Razvrstimo podatke po času
data = data.sort_values('timestamp')

# Izračunamo število primerkov v testni množici
test_size = int(len(data) * 0.1)

# Izberemo najstarejše primere za testno množico
test_data = data[:test_size]

# Preostale primere shranimo v učno množico
train_data = data[test_size:]

# Shranimo podatke v datoteki
test_data.to_csv("test.csv", index=False)
train_data.to_csv("train.csv", index=False)