optDict = {
    "Config":{
        "thread":            "integer",
        "crawlerDeep":               "integer",
        "TimeOut":           "integer",
        "UserAgent":          "string",
        "Cookie":       "string",
        "headers":       "string",
        "Sleep":        "integer"
    }
}      

for family, optionData in optDict.items():
    print optionData
    for option, datatype in optionData.items():
    	print datatype
