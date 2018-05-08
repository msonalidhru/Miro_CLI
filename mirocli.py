# Import all the dependencies
import json
from pandas.io.json import json_normalize
import os.path, enum, logging, datetime

# Configuration Values
logFileName = os.path.dirname(__file__) + "/log/Err_"+ str(datetime.datetime.now()) + ".log"

# Filter Values(fv) to be used for filter conditions
class fv(enum.Enum):
    gameplay = 'Gameplay'
    cmplt = 'Complete'
    corUnf = 'CorrectUnfriendly'

""" Function Name: loadJson
    Input: fileName -> string, Output => JSON DF
    Description: Checks if the file exists in Filesystem and loads it if it is a valid JSON, else raises exception
""" 
def loadJson(fileName):
    if os.path.isfile(fileName):
        # Get the user input and load the JSON file
        with open(fileName) as f: #'/Miro/Miro_CLI/data/data.json'
            df = json.load(f)
        return df
    else:
        raise Exception("loadJson: JSON file not valid.")

""" Function Name: getGameComplete
    Input: df['ColumnName'] -> Modules column that needs to be normalized, Output => Filtered records
    Description: Normalizes the level and selects only Gameplay and Complete records
""" 
def getGameComplete(dfModules):
    try:
        # Drill to Levels inside modules 
        dfLevel =  json_normalize(data=dfModules, record_path='levels', errors='raise')
        
        # Filter rows where Leveltype = `Gameplay` and Result = `Complete`
        dfGame = (dfLevel[(dfLevel['levelType'] == fv.gameplay.value) & (dfLevel['result'] == fv.cmplt.value)])
        return dfGame
    except KeyError as ke:
        raise ValueError("getGameComplete: Property Missing:" + str(ke))
    except Exception as e:
        raise ValueError("getGameComplete: Exception:" + str(e))

""" Function Name: getTargetUnfriendly
    Input: dfGame -> Filtered records of Game, Output => DF where result=Correctunfriendly
    Description: Normalizes the Targets and selects only CorrectUnfriendly records
"""       
def getTargetUnfriendly(dfGame):
    try:
        # Normalize the trials/targets column as this contains the details
        dfTargets= json_normalize(json.loads(dfGame.to_json(orient='records')), ['trials','targets']) 
        
        # Filter only where Result = "CorrectUnfriendly"
        dfFinal = (dfTargets[(dfTargets['result'] == fv.corUnf.value)])
        return dfFinal
    except KeyError as ke:
        raise ValueError("getTargetUnfriendly: Property Missing:" + str(ke))
    except Exception as e:
        raise ValueError("getTargetUnfriendly: Exception:" + str(e))  

""" Function Name: calculateAvgResponse
    Input: dfFinal -> All Filtered DF, Output => Float(2 decimal places)
    Description: Calculates average response time
"""  
def calculateAvgResponse(dfFinal):
    try:
        # Calculate the Avg = SUM(Difference of Finish & ShowTime) / Total of Records
        avResTime = (dfFinal['finishTime'] - dfFinal['showTime']).mean()
        
        # Time is in Milliseconds convert to seconds and Round it to 2 decimal places
        avResTime = round(avResTime / 1000, 2)
        return avResTime
    except KeyError as ke:
        raise ValueError("calculateAvgResponse: KeyError: " + str(ke))
    except TypeError as te:
        raise ValueError("calculateAvgResponse: TypeError: " + str(te))    
    except Exception as e:
        raise ValueError("calculateAvgResponse: Exception: " + str(e))  

""" Function Name: logMiroError
    Input: e -> Exception, Output => None
    Description: Logs all the errors generated in a log file
"""  
def logMiroError(e):
    #%(asctime)s -> DtTime, %(levelname)s: LoggingLevel, %(name)s: LoggerName
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(logFileName)
    fh.setLevel(logging.ERROR)    
    fh.setFormatter(formatter)
    logger = logging.getLogger("mirocli")
    logger.addHandler(fh)
    logger.error(e)
    print("-- Error Occurred --")
    print(str(e))
    print("-- Exiting --")

# Main Program
if __name__ == '__main__':                                                      
    try:
        # Accept input
        dtFile = input("Please enter JSON File Path: ") #'/Miro/Miro_CLI/data.json'
        
        # Get the user input and load the JSON file
        df = loadJson(dtFile)
        
        # Drill to Levels inside modules 
        # Filter rows where Leveltype = `Gameplay` and Result = `Complete`
        dfGame = getGameComplete(df['modules'])
        
        # Filter only where Result = "CorrectUnfriendly"
        dfFinal = getTargetUnfriendly(dfGame)
        
        # Calculate the Avg = SUM(Difference of Finish & ShowTime) / Total of Records
        avResTime = calculateAvgResponse(dfFinal)
        
        print("Average Response Time:" + str(avResTime))
    except Exception as e:
        logMiroError(e)