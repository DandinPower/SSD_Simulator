import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

WAF_AVERAGE_PERIOD = int(os.getenv('WAF_AVERAGE_PERIOD'))

class WAFHistory:
    def __init__(self):
        self.episodes = []
        self.writeBytes = []
        self.actualWriteBytes = []

    def AddHistory(self, episode, writeByte, actualWriteByte):
        self.episodes.append(episode)
        self.writeBytes.append(writeByte)
        self.actualWriteBytes.append(actualWriteByte)

    @staticmethod
    def _moving_average(x_1, x_2, periods=WAF_AVERAGE_PERIOD):
        if len(x_1) < periods:
            return np.nan
        x = np.sum(x_2[-periods:]) / np.sum(x_1[-periods:])
        return x

    def ShowHistory(self, path):
        ma_periods = WAF_AVERAGE_PERIOD
        ma = [self._moving_average(self.writeBytes, self.actualWriteBytes, periods=ma_periods) for self.writeBytes, self.actualWriteBytes in zip(np.array_split(self.writeBytes, len(self.writeBytes) / ma_periods), np.array_split(self.actualWriteBytes, len(self.actualWriteBytes) / ma_periods))]
        plt.title(f'Simulate Period: {ma_periods}')
        plt.plot(np.repeat(ma, ma_periods), label='WAF')
        plt.legend()
        plt.savefig(path)
        plt.clf()

