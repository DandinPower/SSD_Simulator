import numpy as np
import matplotlib.pyplot as plt

def moving_average(x_1, x_2, periods=10):
    if len(x_1) < periods:
        return np.nan
    x = np.sum(x_2[-periods:]) / np.sum(x_1[-periods:])
    return x

# Generate some sample data
x_1 = np.random.rand(100)
x_2 = np.random.rand(100)

# Compute moving averages
ma_periods = 10
ma = [moving_average(x_1, x_2, periods=ma_periods) for x_1, x_2 in zip(np.array_split(x_1, len(x_1) / ma_periods), np.array_split(x_2, len(x_2) / ma_periods))]

# Plot data and moving average
plt.plot(x_1, label='x_1')
plt.plot(x_2, label='x_2')
plt.plot(np.repeat(ma, ma_periods), label='Moving average')
plt.legend()
plt.savefig('test2.png')
plt.clf()