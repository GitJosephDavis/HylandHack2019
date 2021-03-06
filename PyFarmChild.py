import PyFarm
import time
import platform

argIndex = 0
numArgs = 1

def getIdNum():
    id = 1
    cell = PyFarm.sheet2.cell(id+1,1)
    while cell.value != '':
        id += 1
        cell =PyFarm.sheet2.cell(id+1,1)

    PyFarm.sheet2.update_cell(id+1,1,'Machine Connected')
    PyFarm.sheet2.update_cell(id+1,2, id)
    PyFarm.sheet2.update_cell(id+1,3, platform.processor())
    return id   

def runScript():
    script = getScript()
    global argIndex
    global numArgs
    while getArgs():
        print(str(PyFarm.arg))
        finalScript = script[:script.find("import PyFarm")] + "\nPyFarm.setInput("+str(PyFarm.arg)+")\n"+script[script.find("import PyFarm"):]+"\nPyFarm.sendOutput("+str(argIndex)+","+str(numArgs)+")\nPyFarm.clearOutput()"
        
        #Start Elapsed Time
        exec(finalScript)
        #Get Elapsed Time
        
        PyFarm.sheet1.update_cell(argIndex,1,'1')
        argIndex = 0
        numArgs = 1
    PyFarm.sheet2.update_cell(1,1,'')
    argIndex = 0
    numArgs = 1
    runScript()


def getScript():
    script = ''
    while script == '':
        time.sleep(5)
        script = PyFarm.sheet2.cell(1,1).value
    return script    


def getArgs():
    # query for args
    global argIndex
    status = '-1'
    while status != '0' and status != '':
        argIndex += 1
        status = PyFarm.sheet1.cell(argIndex,1).value
        
    argList = []
    global id
    # if there are args
    if status == '0':
        PyFarm.sheet1.update_cell(argIndex,1,id)
        #   set args
        global numArgs
        arg = '0'
        while arg != '':
            numArgs += 1
            arg = PyFarm.sheet1.cell(argIndex,numArgs).value
            if arg != '':
                argList.append(arg)
        PyFarm.setInput(argList)
        return True
    else:
        return False
    

PyFarm.makeConnection()
id = getIdNum()
runScript()