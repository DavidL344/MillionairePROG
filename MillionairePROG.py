# Kdo chce být milionářem - PROG edition
# Autor: David Langr

from time import sleep
from sys import exit
from os import path, remove
from random import randrange
from random import choice as randchoice

questions_filename = "./questions"
questions_encoded_ext = ".bin"
questions_decoded_ext = ".csv"
questions_encoded = questions_filename + questions_encoded_ext
questions_decoded = questions_filename + questions_decoded_ext

# pip install cryptography
# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
crypt_key = "li_CR6HR4m4uyTaWPPoD90rfbUrHjBvN0jq0ERrcspA="

def clearScreen():
    from os import system, name
    if name == 'nt':
        # Windows
        _ = system('cls')
    else:
        # MacOS or GNU/Linux
        _ = system('clear')

def pause(text = "\r\nPokračujte stisknutím klávesy Enter..."):
    input(text)
    return

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
            base64_bytes_encrypted = EncoderTool("crypt", "encrypt", base64_bytes)

            value_encrypted = EncoderTool("decode", "utf-8", base64_bytes_encrypted)
            return value_encrypted
        elif (encodeType == "csv"):
            with open(value + questions_decoded_ext, 'r', encoding="utf-8") as csv_file:
                in_memory_file = csv_file.read()
                encoded_file = EncoderTool("encode", "base64", in_memory_file)
                if (returnWhere == "memory"):
                    return encoded_file
                elif (returnWhere == "file"):
                    with open(value + questions_encoded_ext, 'w', encoding="utf-8") as bin_file:
                        bin_file.writelines(encoded_file)
            return
        else:
            return value.encode(encoding=encodeType, errors='strict')
    elif (endecode == "decode"):
        if (encodeType == "base64"):
            value_bytes_encrypted = EncoderTool("encode", "utf-8", value)
            value_bytes_decrypted = EncoderTool("crypt", "decrypt", value_bytes_encrypted)
            value_bytes = base64.b64decode(value_bytes_decrypted)
            
            value_text = EncoderTool("decode", "utf-8", value_bytes)
            return value_text
        elif (encodeType == "csv"):
            with open(value + questions_encoded_ext, 'r', encoding="utf-8") as bin_file:
                in_memory_file = bin_file.read()
                decoded_file = EncoderTool("decode", "base64", in_memory_file)
                if (returnWhere == "memory"):
                    return decoded_file
                elif (returnWhere == "file"):
                    with open(value + questions_decoded_ext, 'w', encoding="utf-8") as csv_file:
                        csv_file.writelines(decoded_file)
            return
        else:
            return value.decode(encoding=encodeType, errors='strict')
    elif (endecode == "crypt"):
        from cryptography.fernet import Fernet
        if (encodeType == "encrypt"):
            return Fernet(crypt_key).encrypt(value)
        elif (encodeType == "decrypt"):
            return Fernet(crypt_key).decrypt(value)
        else:
            return value
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
            errchoice = choice([f"Chyba: {errtext}", f"Vložte '{questions_encoded}' nebo '{questions_decoded}' a stiskněte ENTER...", "Pro navrácení do menu napište EXIT."], ["", "EXIT"], str, False)
            if (errchoice == "exit"): return False
            
            if (path.exists(questions_encoded)):
                return True
            elif (path.exists(questions_decoded)):
                if (convertQuestions(f"Soubor s otázkami neexistuje!")):
                    return True

def getQuestion(csv_questions, availableQuestions = []):
    if (csv_questions == False): return False

    # If availableQuestions variable is set to None, the question is picked regardless of the already used questions
    if (availableQuestions == None): randomQuestionNumber = randrange(1, len(csv_questions))
    elif (isinstance(availableQuestions, list)):
        if (len(availableQuestions) > 0):
            randomQuestionNumber = randchoice(availableQuestions)
        else:
            # There are no more available questions to use
            return True
    else:
        # The availableQuestions is neither None nor a list
        return False

    # Remove the quotation marks around the strings
    for i in range(len(csv_questions[randomQuestionNumber])):
        csv_questions[randomQuestionNumber][i] = csv_questions[randomQuestionNumber][i][1:-1]
    
    # This doesn't apply for the header data
    if (randomQuestionNumber != 0):
        # If the question contains multiple answers (at index 5), split them to an array
        csv_questions[randomQuestionNumber][5] = csv_questions[randomQuestionNumber][5].split(',')

    # Return the question number as well as the question data
    return [randomQuestionNumber, csv_questions[randomQuestionNumber]]

def loadTheGame():
    clearScreen()
    if not (path.exists(questions_encoded)):
        if (path.exists(questions_decoded)):
            if not (convertQuestions()): return
        else:
            if not (convertQuestions(f"Otázky nejsou k nalezení! Je třeba je nejprve importovat ze souboru '{questions_decoded}'.")): return
        clearScreen()

    try:
        # Load the questions at the beginning to prevent question injection later on that could manipulate the results
        csv_questions = loadQuestions()

        # Locate the messages in the header of the file
        header_0 = getQuestion(csv_questions, [0])[1]
        header_data = [
            header_0[0], # The greeting message
            header_0[1], # Result: 100-87%
            header_0[2], # Result: 86-73%
            header_0[3], # Result: 72-58%
            header_0[4], # Result: 57-44%
            header_0[5]  # Result: 43-0%
        ]
    except:
        rebuildFile = choice(["Vypadá to, že soubor je poškozený. Chcete ho smazat a pokusit se ho znovu importovat (ano/ne)?"], ["ano", "ne", "exit"], str)
        if (rebuildFile == "ano"):
            remove(questions_encoded)
            if (convertQuestions()):
                try:
                    csv_questions = loadQuestions()
                    header_0 = getQuestion(csv_questions, [0])[1]
                    header_data = [
                        header_0[0], # The greeting message
                        header_0[1], # Result: 100-87%
                        header_0[2], # Result: 86-73%
                        header_0[3], # Result: 72-58%
                        header_0[4], # Result: 57-44%
                        header_0[5]  # Result: 43-0%
                    ]
                except:
                    clearScreen()
                    print("Chyba: Po úspěšné konverzi není možné se souborem pracovat.")
                    pause()
                    return
            else: return
        else: return

    while(True):
        clearScreen()
        try:
            # The first line in csv_questions doesn't contain a question
            csv_questions_truelength = len(csv_questions) - 1

            numberOfQuestions = input(f"Počet položených otázek (1-{csv_questions_truelength}): ")
            if (numberOfQuestions.lower() == "exit"): return
            numberOfQuestions = int(numberOfQuestions)
            
            # The length doesn't actually have to be sanitized - the quiz will end automatically once there are no unanswered questions
            if (numberOfQuestions > 0) and (numberOfQuestions <= csv_questions_truelength):
                score = 0
                answeredQuestions = 0
                break
            else: continue
        except: continue

    clearScreen()
    print(header_data[0])
    sleep(3)
    clearScreen()

    # Add all the question numbers to the list
    remainingQuestions = []
    for x in range(1, len(csv_questions)):
        remainingQuestions.append(x)

    for questionNumber in range(1, numberOfQuestions + 1):
        if not (csv_questions == False):
            returnedQuestion = getQuestion(csv_questions, remainingQuestions)
            if (returnedQuestion == True):
                # There are no more questions in the file
                endingScreen(header_data, answeredQuestions, score)
                return
            elif (returnedQuestion == False):
                # The app just checked that the csv_questions are loaded (and therefore cannot be False)
                # This is here just in case something gets terribly wrong and I don't want the app to crash
                return
            else:
                remainingQuestions.remove(returnedQuestion[0])
                questionData = returnedQuestion[1]
        else:
            # Questions failed to load from memory even though they were just successfully loaded from the file
            # Therefore, this should never occur
            return
            
        if (questionData == False): return
        questionAnswer = choice(textlines = ["[Skóre: " + str(score) + "]\r\n", "Otázka č." + str(questionNumber) + ": " + questionData[0], "a) " + questionData[1], "b) " + questionData[2], "c) " + questionData[3], "d) " + questionData[4]], choiceList = ["a", "b", "c", "d", "exit"], outputType = str)
        if not (questionAnswer == "exit"):
            answeredQuestions = questionNumber
            if (questionAnswer in questionData[5]):
                score += 1
        else: break
    endingScreen(header_data, answeredQuestions, score)
    return

def endingScreen(header_data, answeredQuestions = 0, score = 0):
    clearScreen()
    if (answeredQuestions == 0): return
    percentValue = (score / answeredQuestions) * 100

    if (100 >= percentValue >= 87): result_message = header_data[1] # Result: 100-87%
    elif (87 > percentValue >= 73): result_message = header_data[2] # Result: 86-73%
    elif (73 > percentValue >= 58): result_message = header_data[3] # Result: 72-58%
    elif (58 > percentValue >= 44): result_message = header_data[4] # Result: 57-44%
    elif (44 > percentValue >= 0): result_message = header_data[5] # Result: 43-0%
    else: result_message = "Procentuální hodnota je neplatná!"

    if (percentValue.is_integer()):
        # If the float is an integer, cut the decimal places
        percentValue = int(percentValue)
    else:
        # If not, round it to two decimal places
        percentValue = round(percentValue, 2)

    # Convert the value to the Czech locale (cs_CZ)
    # * Both the percentage value and the percentage symbol have a space between them
    # * A comma ',' is used as a decimal separator instead of a dot '.'
    # Summary: https://www.localeplanet.com/icu/cs-CZ/index.html
    percentValue = str(percentValue).replace('.', ',') + " "

    print(f"{result_message}\r\n\r\nPočet bodů: {score}/{answeredQuestions}\r\nÚspěšnost: {percentValue}%")
    pause()
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