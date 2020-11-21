# Kdo chce být milionářem - PROG edition
# Autor: David Langr

from time import sleep
from sys import exit

def clearScreen():
    from os import system, name
    if name == 'nt':
        # Windows
        _ = system('cls')
    else:
        # MacOS or GNU/Linux
        _ = system('clear')

def choice(textlines = [], choiceList = [], outputType = int, caseSensitive = False):
    while (True):
        clearScreen()

        # Write info about the choice on screen
        for textline in textlines:
            print(textline)
        userInput = input("\r\nZvolte možnost a potvrďte tlačítkem ENTER: ")

        # Try to convert the user input to desired output type
        userInput = convertVar(userInput, outputType) 

        # Convert to lowercase if answer is string that is not case-sensitive
        if outputType == str and not caseSensitive:
            userInput = userInput.lower()
            for i in range(len(choiceList)):
                choiceList[i] = choiceList[i].lower()

        if userInput in choiceList:
            if (outputType == int):
                userInput = int(userInput)
            elif (outputType == str):
                userInput = str(userInput)
            return userInput
        else:
            continue

def convertVar(var, datatype):
    try:
        if (datatype == str):
            return str(var)
        elif (datatype == int):
            return int(var)
        elif (datatype == float):
            return float(var)
        elif (datatype == bool):
            return bool(var)
    except:
        return var

def EncoderTool(endecode, encodeType, value):
    import base64
    if (endecode == "encode"):
        if (encodeType == "base64"):
            value_bytes = EncoderTool("encode", "UTF-8", value)
            base64_bytes = base64.b64encode(value_bytes)
            value_base64 = EncoderTool("decode", "UTF-8", base64_bytes)
            return value_base64
        else:
            return value.encode(encoding=encodeType, errors='strict')
    elif (endecode == "decode"):
        if (encodeType == "base64"):
            base64_bytes = EncoderTool("encode", "UTF-8", value)
            value_bytes = base64.b64decode(base64_bytes)
            value_text = EncoderTool("decode", "UTF-8", value_bytes)
            return value_text
        else:
            return value.decode(encoding=encodeType, errors='strict')
    else:
        return value

def main():
    while(True):
        menu = choice(["Kdo chce být milionářem - PROG edition\r\n", "1 - Hrát\r\n2 - Odejít"], [1, 2])

        if (menu == 1):
            break
        elif (menu == 2):
            exit(0)
        else:
            # Should never occue
            continue
    print("Game, Start!")
    encode = EncoderTool("decode", "base64", "RGF2aWQ=")
    print(encode)

main()