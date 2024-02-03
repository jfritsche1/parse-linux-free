import pandas as pd
import matplotlib.pyplot as plt
from setup_logging.setup_logging import logger

class FreeLogging:
    def __name__(self):
        return "FreeLogging"

    def __init__(self):
        self.filename = None
        self.df = None
        self.memoryDf = None
        self.swapDf = None
        self.plots_path = "plots/"
    
    def getPlotsPath(self) -> str:
        return self.plots_path

    def setPlotsPath(self, newPath: str) -> None:
        self.plots_path = newPath

    def readInFreeLog(self) -> None:
        if (self.filename):
            self.df = pd.read_fwf(self.filename)
            self.cleanUpLogs()
            logger.info('%s file was read into a dataframe.' % self.filename)
        else:
            logger.error("The filename has not been set. Please use setFilename(str: filename)")

    def setFilename(self, filename: str) -> None:
        self.filename = filename
        logger.info("Filename set to %s" % filename)

    def cleanUpLogs(self) -> None:
        self.df.columns = ["time", "type", *self.df.columns[2:]]
        self.df = self.df.dropna(how='all') 
        self.df = self.df.dropna(subset=['type'])
        self.df = self.df.set_index("time")
        for col in self.df.columns:
            if (col != "type"):
                self.df[col] = pd.to_numeric(self.df[col], downcast='unsigned')
                logger.debug("Converting column %s to an unsigned integer." % col)

    def createDataframeType(self, typ: str) -> pd.DataFrame:
        df = self.df.where(self.df['type'] == typ) 
        df = df.dropna(how='all') 
        df = df.dropna(axis=1)
        return df
    
    def createSwapDf(self) -> None:
        self.swapDf = self.createDataframeType("Swap:")

    def createMemoryDf(self) -> None:
        self.memoryDf = self.createDataframeType("Mem:")

    def plotSwap(self) -> None:
        title = "Swap"
        fpath = self.plots_path + title + ".png"
        self.swapDf.plot.line(title=title, figsize=(15,8))
        plt.savefig(fpath)
        logger.info("Saved the %s file to %s" % (title, fpath))

    def plotMemory(self) -> None:
        title = "Memory"
        fpath = self.getPlotsPath() + title + ".png"
        self.memoryDf.plot.line(title=title, figsize=(15,8))
        plt.savefig(fpath)
        logger.info("Saved the %s file to %s" % (title, fpath))

    def plotDf(self) -> None:
        title = "Free-Plot"
        fpath = self.getPlotsPath() + title + ".png"
        sp = self.swapDf.plot.line()
        self.memoryDf.plot.line(title=title, ax=sp, figsize=(15,8))
        plt.savefig(fpath)
        logger.info("Saved the %s file to %s" % (title, fpath))

