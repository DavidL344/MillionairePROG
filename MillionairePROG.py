# Kdo chce být milionářem - PROG edition
# Autor: David Langr

from time import sleep
from sys import exit
from os import path
from random import randrange

questions_filename = "./questions"
questions_encoded_ext = ".bin"
questions_decoded_ext = ".csv"
questions_encoded = questions_filename + questions_encoded_ext
questions_decoded = questions_filename + questions_decoded_ext

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

def EncoderTool(endecode, encodeType, value=questions_filename, returnWhere="memory"):
    import base64
    if (endecode == "encode"):
        if (encodeType == "base64"):
            value_bytes = EncoderTool("encode", "utf-8", value)
            base64_bytes = base64.b64encode(value_bytes)
            value_base64 = EncoderTool("decode", "utf-8", base64_bytes)
            return value_base64
        elif (encodeType == "csv"):
            # value = "./questions"
            with open(value + questions_decoded_ext, 'r', encoding="utf-8") as csv_file:
                in_memory_file = csv_file.read()
                encoded_file = EncoderTool("encode", "base64", in_memory_file)
                if (returnWhere == "memory"):
                    return encoded_file
                elif (returnWhere == "file"):
                    # value = "./questions"
                    with open(value + questions_encoded_ext, 'w', encoding="utf-8") as bin_file:
                        bin_file.writelines(encoded_file)
            return
        else:
            return value.encode(encoding=encodeType, errors='strict')
    elif (endecode == "decode"):
        if (encodeType == "base64"):
            base64_bytes = EncoderTool("encode", "utf-8", value)
            value_bytes = base64.b64decode(base64_bytes)
            value_text = EncoderTool("decode", "utf-8", value_bytes)
            return value_text
        elif (encodeType == "csv"):
            # value = "./questions"
            with open(value + questions_encoded_ext, 'r', encoding="utf-8") as bin_file:
                in_memory_file = bin_file.read()
                decoded_file = EncoderTool("decode", "base64", in_memory_file)
                if (returnWhere == "memory"):
                    return decoded_file
                elif (returnWhere == "file"):
                    # value = "./questions"
                    with open(value + questions_decoded_ext, 'w', encoding="utf-8") as csv_file:
                        csv_file.writelines(decoded_file)
            return
        else:
            return value.decode(encoding=encodeType, errors='strict')
    else:
        return value

def loadQuestions():
    # Load file in memory: https://stackoverflow.com/a/17767445
    import csv
    if (path.exists(questions_encoded)):
        in_memory_file = EncoderTool("decode", "csv")
        return list(csv.reader(in_memory_file.splitlines(), delimiter="¤", quotechar="|", escapechar="\\"))
    else:
        if (convertQuestions("Program ztratil přístup k otázkám!")):
            return loadQuestions()
        else:
            return False

def convertQuestions(errtext = "Nelze načíst otázky."):
    clearScreen()
    if (path.exists(questions_decoded)):
        print(f"Probíhá importování otázek ze souboru '{questions_decoded}'...")
        EncoderTool("encode", "csv", questions_filename, "file")
        print("Import dokončen!")
        sleep(3)
        return True
    else:
        while (True):
            clearScreen()
            errchoice = choice([f"ERROR: {errtext}", f"Vložte '{questions_encoded}' nebo '{questions_decoded}' a stiskněte ENTER...", "Pro navrácení do menu zvolte napište EXIT."], ["", "EXIT"], str, False)
            if (errchoice == "exit"): return False
            
            if (path.exists(questions_encoded)):
                return True
            elif (path.exists(questions_decoded)):
                if (convertQuestions(f"Soubor s otázkami neexistuje!")):
                    return True

def getQuestion():
    csv_questions = loadQuestions()
    if (csv_questions == False): return False
    randomQuestionNumber = randrange(1, len(csv_questions))

    # Remove the quotation marks around the strings
    for i in range(len(csv_questions[randomQuestionNumber])):
        csv_questions[randomQuestionNumber][i] = csv_questions[randomQuestionNumber][i][1:-1]
    return csv_questions[randomQuestionNumber]

def loadTheGame():
    clearScreen()
    if not (path.exists(questions_encoded)):
        if (path.exists(questions_decoded)):
            if not (convertQuestions()): return
        else:
            if not (convertQuestions(f"Otázky nejsou k nalezení! Je třeba je nejprve importovat ze souboru '{questions_decoded}'.")): return
        clearScreen()
    print("Game, Start!")
    sleep(3)
    clearScreen()

    score = 0
    answeredQuestions = 0
    numberOfQuestions = 10
    for questionNumber in range(1, numberOfQuestions + 1):
        questionData = getQuestion()
        if (questionData == False): return
        questionAnswer = choice(textlines = ["[Skóre: " + str(score) + "]", "Otázka č." + str(questionNumber) + ": " + questionData[0], "a) " + questionData[1], "b) " + questionData[2], "c) " + questionData[3], "d) " + questionData[4]], choiceList = ["a", "b", "c", "d", "exit"], outputType = str)
        if not (questionAnswer == "exit"):
            answeredQuestions = questionNumber
            if (questionAnswer == questionData[5]):
                score += 1
        else: break
    clearScreen()
    if (answeredQuestions == 0): return
    percentValue = (score / answeredQuestions) * 100
    
    if (percentValue.is_integer()):
        # If the float is an integer, cut the decimal places
        percentValue = int(percentValue)
    else:
        # If not, round it to two decimal places
        percentValue = round(percentValue, 2)

    print(f"Výsledky:\r\n\r\nPočet bodů: {score}/{answeredQuestions}\r\nÚspěšnost: {percentValue}%")
    input("Press ENTER to continue...")
    return

def main():
    while(True):
        menu = choice(["Kdo chce být milionářem - PROG edition\r\n", "1 - Hrát\r\n2 - Odejít\r\n# - Importovat otázky"], ['1', '2', '#', "exit"], str)
        if (menu == '1'):
            loadTheGame()
        elif (menu == '2') or (menu == "exit"):
            exit(0)
        elif (menu == '#'):
            convertQuestions()
        continue
main()