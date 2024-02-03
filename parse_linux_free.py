import argparse
from pathlib import Path
from free_logging.FreeLogging import FreeLogging

def main():
    parser = argparse.ArgumentParser(prog='Free Log Parsing',
        description='Parse a free log file.', epilog='TBD')
    parser.add_argument('filename')
    parser.add_argument('-p', '--plot', action='store_true') 
    parser.add_argument('--plots-path')

    args = parser.parse_args()

    flog = FreeLogging()
    flog.setFilename(args.filename)
    flog.readInFreeLog()

    flog.createSwapDf()
    flog.createMemoryDf()

    if (args.plots_path):
        if (args.plots_path[-1] != "/"):
            args.plots_path = args.plots_path + "/"
        flog.setPlotsPath(args.plots_path)

    if (args.plot or args.plots_path):
        Path(flog.getPlotsPath()).mkdir(exist_ok=True)
        flog.plotSwap()
        flog.plotMemory()
        flog.plotDf()

if __name__ == "__main__":
    main()


