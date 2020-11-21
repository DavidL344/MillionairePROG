# Kdo chce být milionářem - PROG edition
# Autor: David Langr

from time import sleep
from sys import exit
from os import path

csv_questions = []

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

def EncoderTool(endecode, encodeType, value = "./questions", returnWhere = "memory"):
    import base64
    if (endecode == "encode"):
        if (encodeType == "base64"):
            value_bytes = EncoderTool("encode", "UTF-8", value)
            base64_bytes = base64.b64encode(value_bytes)
            value_base64 = EncoderTool("decode", "UTF-8", base64_bytes)
            return value_base64
        elif (encodeType == "csv"):
            # value = "./questions"
            with open(value + ".csv", 'r') as csv_file:
                in_memory_file = csv_file.read()
                encoded_file = EncoderTool("encode", "base64", in_memory_file)
                if (returnWhere == "memory"):
                    return encoded_file
                elif (returnWhere == "file"):
                    # value = ./questions
                    with open(value + ".bin", 'w') as bin_file:
                        bin_file.writelines(encoded_file)
            return
        else:
            return value.encode(encoding=encodeType, errors='strict')
    elif (endecode == "decode"):
        if (encodeType == "base64"):
            base64_bytes = EncoderTool("encode", "UTF-8", value)
            value_bytes = base64.b64decode(base64_bytes)
            value_text = EncoderTool("decode", "UTF-8", value_bytes)
            return value_text
        elif (encodeType == "csv"):
            # value = ./questions
            with open(value + ".bin", 'r') as bin_file:
                in_memory_file = bin_file.read()
                decoded_file = EncoderTool("decode", "base64", in_memory_file)
                if (returnWhere == "memory"):
                    return decoded_file
                elif (returnWhere == "file"):
                    # ./questions
                    with open(value + ".csv", 'w') as csv_file:
                        csv_file.writelines(decoded_file)
            return
        else:
            return value.decode(encoding=encodeType, errors='strict')
    else:
        return value

def loadQuestions():
    # Load file in memory: https://stackoverflow.com/a/17767445
    clearScreen()
    import csv
    if (path.exists("./questions.bin")):
        in_memory_file = EncoderTool("decode", "csv")
        csv_questions = csv.reader(in_memory_file.splitlines(), delimiter=",", quotechar="|")

        # Test start
        # TODO: ignore row[0] - it is used as a header of the table
        for row in csv_questions:
            string_no_quotation_marks = row[0][1:-1]
            print(string_no_quotation_marks)
        # Test end

        print("Game, Start!")
    else:
        print("Otázky nejsou k nalezení! Je třeba je nejprve importovat.")
    sleep(3)

def convertQuestions():
    clearScreen()
    if (path.exists("./questions.csv")):
        print("Probíhá importování otázek ze souboru questions.csv")
        EncoderTool("encode", "csv", "./questions", "file")
        print("Import dokončen")
    else:
        print("Soubor questions.csv neexistuje!")
    sleep(3)

def loadTheGame():
    loadQuestions()
    
    #encode = EncoderTool("decode", "base64", "RGF2aWQ=")
    #print(encode)
    

def main():
    while(True):
        menu = choice(["Kdo chce být milionářem - PROG edition\r\n", "1 - Hrát\r\n2 - Odejít\r\n# - Importovat otázky"], ['1', '2', '#'], str)
        if (menu == '1'):
            loadTheGame()
        elif (menu == '2'):
            exit(0)
        elif (menu == '#'):
            convertQuestions()
        continue
main()