def setParam(dict, jsStr):
    for key, value in dict.items():
        jsStr = re.sub('\$\{' + key + '\}', value, jsStr)
    return jsStr
def jsRead(file):
    l = open(file, 'r')
    lcon = l.read()
    l.close()
    return lcon