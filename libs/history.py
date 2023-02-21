import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

WAF_AVERAGE_PERIOD = int(os.getenv('WAF_AVERAGE_PERIOD'))

class WAFHistory:
    def __init__(self):
        self.episodes = []
        self.wafs = []

    def AddHistory(self, episode, waf):
        self.episodes.append(episode)
        self.wafs.append(waf)

    @staticmethod
    def _moving_average(x, periods=WAF_AVERAGE_PERIOD):
        if len(x) < periods:
            return x
        cumsum = np.cumsum(np.insert(x, 0, 0)) 
        res = (cumsum[periods:] - cumsum[:-periods]) / periods
        return np.hstack([x[:periods-1], res])

    def ShowHistory(self, path):
        fig = plt.figure(1, figsize=(15, 7))
        plt.clf()
        ax1 = fig.add_subplot(111)
        lines = []
        fig = plt.figure(1, figsize=(15, 7))
        plt.clf()
        ax1 = fig.add_subplot(111)
        #ax1.set_ylim(0, 10)
        ax1.plot(self.wafs, color="C2", alpha=0.2)
        plt.title('Simulate')
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('WAFS')
        mean_waf = self._moving_average(self.wafs)
        lines.append(ax1.plot(mean_waf, label="WAFS", color="C2")[0])    
        labs = [l.get_label() for l in lines]
        ax1.legend(lines, labs, loc=3)
        plt.savefig(path)
        plt.clf()