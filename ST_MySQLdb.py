import pymysql
# 2018_01_09 lstDataInfo remove column`Change`.
lstDataInfo = ["`YMD` date NOT NULL," ,"`open` decimal(8,2),", "`close` decimal(8,2),",
               "`high` decimal(8,2),","`low` decimal(8,2),","`capacity` decimal(16,2),",
               "`turnover` decimal(16,2),","`transaction` decimal(12,2)"]

def GoToMySQLdb(strTable, lstColumn, lstValue):
    strYMD = str(lstValue[0])
    for x in range (len(lstColumn)):
        strColumn = lstColumn[x]
        #print ("Write Data: " +strYMD+" "+strColumn )
        if strColumn == "YMD":
            #print (strTable, strColumn, strYMD)
            InsertValue(strTable, strColumn, strYMD)
        else:
            strValue =lstValue[x]
            #print (strTable, strColumn, strValue)
            # Filter decimal to 2 digits.
            strFormatValue = format(strValue, '.2f')
            intFormatValue =  float(strFormatValue)
            UpdateValue(strTable, "YMD", strYMD, strColumn, intFormatValue)
    
        
# sql_cmd = "INSERT INTO st_list (ST_ID, ST_OpenPrice) VALUES ('%s', %.6f)" % ('1111', 22.22)
# sql_cmd = InsertValue("st_list", "ST_ID", "123")
def SQLExecute(sql_cmd):
    connect=pymysql.Connect( host="localhost", port=8888, user="root",  password="123456", db="st_db", charset="utf8") 
    cursor = connect.cursor()
    cursor.execute(sql_cmd)
    connect.commit()
    #return connect

def CreateST_TableByST_Number(strTable):    
    #ql_cmd = CREATE TABLE `1234` (`YMD` date NOT NULL,`Open` decimal(4,2),`Close` decimal(4,2),`Change` decimal(12,2),`High` decimal(4,2),`Low` decimal(4,2),`Capacity` decimal(12,2),`Turnover` decimal(12,2),`Transaction` decimal(12,2),PRIMARY KEY (`YMD`))
    strDataInfo = ""
    strTable = "st_"+strTable
    for i in range(len(lstDataInfo)):
        strDataInfo = strDataInfo + lstDataInfo[i] 
    sql_cmd = """CREATE TABLE `%s` (%s,PRIMARY KEY (`YMD`))"""%(strTable, strDataInfo)
    print("Create Table "+strTable)
    SQLExecute(sql_cmd)

def GetColumnDataByOrder(strTable, sColumn, sOrderColumn):
    connect=pymysql.Connect( host="localhost", port=8888, user="root",  password="123456", db="st_db", charset="utf8") 
    cursor = connect.cursor()
    sql_cmd = """SELECT %s FROM %s ORDER BY %s"""%(sColumn, strTable, sOrderColumn)
    cursor.execute(sql_cmd)
    lstTuple = cursor.fetchall()
    #strDataType = type(lstST_50s[0][0])
    lstData = []
    for i in range (len(lstTuple)):
        lstValue = lstTuple[i][0]
        lstData.append(lstValue) 
    print (lstData)
    return lstData
    

"""
def decValueInsert(strTable, strColumn, decValue):
    sql_cmd = "INSERT INTO strTable (strColumn) VALUES (%.8f)" % (decValue)
    SQLExecute(sql_cmd)
"""

def InsertValue(strTable, strColumn, strValue):
    sql_cmd = """INSERT INTO %s (%s) VALUES ('%s')""" %(strTable, strColumn, strValue)
    #print (sql_cmd)
    SQLExecute(sql_cmd)        
    
def UpdateValue(strTable, strItemColumn, strItemValue, strColumn, strValue):
    if strColumn == "Change":
        sql_cmd = """UPDATE %s SET %s = '%s'  WHERE %s = '%s'"""%(strTable, strColumn, strValue, strItemColumn, strItemValue)
        #print (sql_cmd)
    else:
        sql_cmd = """UPDATE %s SET %s = %.8f  WHERE %s = '%s'"""%(strTable, strColumn, strValue, strItemColumn, strItemValue)
        #print (sql_cmd)
    SQLExecute(sql_cmd)
    

if __name__ == "__main__":

    #CreateST_TableByST_Number("2317")
    GetColumnDataByOrder("st_50s", "ST_Number", "No")
    