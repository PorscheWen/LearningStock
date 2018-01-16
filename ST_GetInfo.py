import twstock
import ST_MySQLdb
import time
import datetime
#import ST_GetSTData

def CheckEndDay(lstStBasicData, intM):
    strIsEndDay = ""
    strYMD = str(lstStBasicData[0])
    strM = strYMD.split("-")[1]
    if  str(intM) not in strM:
        strIsEndDay = "true"
    return strIsEndDay

def GetBasicData(lstBasicData):
    lstStBasicData = []
    #  Data(date=datetime.datetime(2017, 5, 18, 0, 0), capacity=22490217, turnover=4559780051, 
    #  open=202.5, high=204.0, low=201.5, close=203.5, change=-0.5, transaction=6983)    
    dateYMDT = lstBasicData[0]
    dateYMD = dateYMDT
    intCapacity = lstBasicData[1]
    intTurnover = lstBasicData[2]
    intOpen = lstBasicData[3]
    intHigh = lstBasicData[4]
    intLow = lstBasicData[5]
    intClose = lstBasicData[6]
    intChange = lstBasicData[7]
    intTransaction = lstBasicData[8]
    lstStBasicData = [dateYMD, intCapacity, intTurnover, intOpen, intHigh, intLow, intClose, intTransaction, intChange]
    return lstStBasicData

# Try to get Data by 100 times every j seconds
def GetDataByTry(strST_Number, intY, intM):
    lstST_Data = []
    stock = "No connection"
    for i in range(100):
        #print("Count: "+str(i))
        j = 10*i+160
        try:
            stock = twstock.Stock(strST_Number)
            lstPrice = stock.fetch(intY, intM)
            print (lstPrice)
            if lstPrice!= []:
                #print(str(j) + " seconds: Get data")
                return lstPrice, stock
        except:
            strTxt = (str(j) + " seconds: No data")
            print (strTxt)
        time.sleep(j)
    return lstST_Data, stock  


def  AddDataByMonth(strST_Number, intY, intM, f):
    #lstStBasicDataItem = ["YMD", "Capacity","Turnover","Open","High","Low","Close ","Transaction","Change "]
    lstStBasicDataItem = ["YMD", "capacity","turnover","open","high","low","close ","transaction"]    
    strTable = "st_"+strST_Number
    # Data(date=datetime.datetime(2017, 5, 18, 0, 0), capacity=22490217, turnover=4559780051, 
    # open=202.5, high=204.0, low=201.5, close=203.5, change=-0.5, transaction=6983)
    #lstMonthData = stock.fetch_from(intY, intM )    
    lstMonthData, stock = GetDataByTry(strST_Number, intY, intM)
    if lstMonthData == []:
        strLogInfo = "Cannot get any data."
        print (strLogInfo)
        f.write(strLogInfo)
        return
    #lstBasicData = ["2017-11-1"," 1313748", "111897404"," 85.35", "85.4", "84.95", "85.1", "1.1", "430"]
    #print (lstMonthData)
    for x in range (len(lstMonthData)):
        lstBasicData = stock.data[x]
        lstStBasicData = GetBasicData(lstBasicData)
        strIsEndDay= CheckEndDay(lstStBasicData, intM)
        #print (strEndDay)
        if strIsEndDay == "true":
            strLogInfo = "Get Data  in " +str(intY)+"- "+str(intM)+" done."
            print (strLogInfo)
            f.write(strLogInfo)
            return
        ST_MySQLdb.GoToMySQLdb(strTable, lstStBasicDataItem, lstStBasicData)


def AddDataByStIDInitialYM(strST_Number, initialYear, initialMonth, f):
    # Create Table if it is not exist
    CreateST_Table(strST_Number, f)  
    intCurrentYear = int(time.strftime("%Y"))
    intCurrentMonth = int(time.strftime("%M"))
    strCurrentYM = str(intCurrentYear)+"-"+str(intCurrentMonth)
    #strCurrentYM = datetime.datetime.now().strftime("%Y-%m")
    strCollectInfo = "Collect "+strST_Number+" data from "+str(initialYear)+"-"+str(initialMonth)+" ~ "+str(intCurrentYear)+"-"+str(intCurrentMonth)
    print(strCollectInfo)
    f.write(strCollectInfo)
    # Collect Data from initial year to past 30 years.
    for x in range(30):
        intDataYear = initialYear + x
        # Collect Data each month.
        for y in range(11):
            intDataMonth = initialMonth + y
            strDataYM = str(intDataYear)+"-"+str(intDataMonth)
            # If Data Year and Mmonth is larger than Current time, stop collect data
            print (strCurrentYM)
            print (strDataYM)
            #AddDataByMonth(strST_Number, intDataYear, intDataMonth, f)
            strCollectDone = "\n"+strST_Number+" data has collected "+str(intDataYear)+"-"+str(intDataMonth)
            print(strCollectDone)
            f.write(strCollectDone)
            intWaitTime = 200
            #time.sleep(intWaitTime)
            dateYMD = datetime.datetime.now()
            strNextDataTime = str(dateYMD + datetime.timedelta(seconds=intWaitTime))
            print ("... Next data start at " + strNextDataTime)   
            if strDataYM == strCurrentYM:
                print ("\n ***  All Data st_"+strST_Number+" has collected.  ***  ")
                return                         
            return          
        
    """
        # Collect Data each month.
        for y in range(11):
            intM = 1 + y
            # If Data Year and Mmonth is larger than Current time, stop collect data
            print (intDataYear > intCurrentYear)
            print (intM > intCurrentMonth)
            if intDataYear > intCurrentYear & intM > intCurrentMonth:
                print ("\nAll Data st_"+strST_Number+" has collected.")
                return
            else:
                #AddDataByMonth(strST_Number, intDataYear, intM, f)
                strCollectDone = "\n"+strST_Number+" data has collected "+str(intDataYear)+"-"+str(intM)
                print(strCollectDone)
                f.write(strCollectDone)
                intWaitTime = 200
                #time.sleep(intWaitTime)
                dateYMD = datetime.datetime.now()
                strNextDataTime = str(dateYMD + datetime.timedelta(seconds=intWaitTime))
                print ("... Next data start at " + strNextDataTime)                
        return        
    """

def CreateST_Table(strST_Number, f):
    try:
        ST_MySQLdb.CreateST_TableByST_Number(strST_Number)
        strTableInfo = "New Table is created: st_"+strST_Number
        print (strTableInfo)
        f.write(strTableInfo+"\n")        
    except:
        strTableInfo = "Table st_"+strST_Number+" is not created."
        print (strTableInfo)
        f.write(strTableInfo+"\n")        
        
def Add50sDataByYear(intInitialY, intInitialM, f):
    lst50s = ST_MySQLdb.GetColumnDataByOrder("st_0050_list", "ST_Number", "No")
    for i in range (len(lst50s)):
        strST_Number = lst50s[i]
        strStartCollect = "\n  ---- Start to Write st_"+strST_Number+" Data ---  "
        f.write(strStartCollect+"\n")
        AddDataByStIDInitialYM(strST_Number, intInitialY, intInitialM, f)
    

    
if __name__ == "__main__":
    
    # Write Log to DataLog.txt
    dateYMD = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M')
    fw = open("DataLog.txt", "w+")
    fa = open("DataLog.txt", "a+")  
    fw.write("Start Time: "+str(dateYMD)+"\n")
    
    # Add Data by ST_Number(str) and initial year(int)
    #AddDataByStIDInitialYM("2330", 2017, 01, fa)
    
    # Add Data by ST_Number(str) and year(int) month(int)
    AddDataByMonth("0050", 2017, 11, fa)
    
    # Create New st_Table by ST_number
    #CreateST_Table("1234", fa)    
    
    # Add 50s Data by initial year(int)
    #Add50sDataByYear(2016, 01, fa)
    
    fw.close()   
    fa.close()   
    
    