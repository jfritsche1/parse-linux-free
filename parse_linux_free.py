import argparse
import pandas as pd
import matplotlib.pyplot as plt
import logging as lg

class FreeLogging:
    def __init__(self):
        self.filename = None
        self.df = None
        self.memoryDf = None
        self.swapDf = None

    def readInFreeLog(self):
        if (self.filename):
            self.df = pd.read_fwf(self.filename)
            self.cleanUpLogs()
            lg.info('%s file was read into a dataframe.' % self.filename)
        else:
            lg.warning("The filename has not been set. Please use setFilename(str: filename)")

    def setFilename(self, filename: str) -> None:
        self.filename = filename
        lg.info("Filename set to %s" % filename)

    def cleanUpLogs(self):
        self.df.columns = ["time", "type", *self.df.columns[2:]]
        self.df = self.df.dropna(how='all') 
        self.df = self.df.dropna(subset=['type'])
        self.df = self.df.set_index("time")
        for col in self.df.columns:
            if (col != "type"):
                self.df[col] = pd.to_numeric(self.df[col], downcast='unsigned')
                lg.debug("Converting column %s to an unsigned integer." % col)

    def createDataframeType(self, typ: str) -> pd.DataFrame:
        df = self.df.where(self.df['type'] == typ) 
        df = df.dropna(how='all') 
        df = df.dropna(axis=1)
        return df
    
    def createSwapDf(self):
        self.swapDf = self.createDataframeType("Swap:")

    def createMemoryDf(self):
        self.memoryDf = self.createDataframeType("Mem:")

    def plotSwap(self):
        title = "Swap"
        fpath = "plots/" + title + ".png"
        self.swapDf.plot.line(title=title, figsize=(15,8))
        plt.savefig(fpath)
        lg.info("Saved the %s file to %s" % (title, fpath))

    def plotMemory(self):
        title = "Memory"
        fpath = "plots/" + title + ".png"
        self.memoryDf.plot.line(title=title, figsize=(15,8))
        plt.savefig(fpath)
        lg.info("Saved the %s file to %s" % (title, fpath))

    def plotDf(self):
        title = "Free-Plot"
        fpath = "plots/" + title + ".png"
        sp = self.swapDf.plot.line()
        self.memoryDf.plot.line(title=title, ax=sp, figsize=(15,8))
        plt.savefig(fpath)
        lg.info("Saved the %s file to %s" % (title, fpath))

def main():
    parser = argparse.ArgumentParser(prog='Free Log Parsing',
        description='Parse a free log file.', epilog='TBD')
    parser.add_argument('filename')
    parser.add_argument('-p', '--plot', action='store_true') 
    args = parser.parse_args()

    flog = FreeLogging()
    flog.setFilename(args.filename)
    flog.readInFreeLog()

    flog.createSwapDf()
    flog.createMemoryDf()

    if (args.plot):
        flog.plotSwap()
        flog.plotMemory()
        flog.plotDf()

if __name__ == "__main__":
    main()


