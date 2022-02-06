import pandas as pd 
from english_words import english_words_lower_alpha_set
from wordfreq import zipf_frequency as wf

LENGTH = 5

class WordleGuesser():
    def __init__(self, length = LENGTH):
        ### Initialize
        WORD_LIST = pd.DataFrame(list(english_words_lower_alpha_set), columns=['Word'])
        ### Filter by length
        WORD_LIST = WORD_LIST[WORD_LIST.iloc[:,0].str.len() == LENGTH]
        ### Implement frequency of words
        WORD_LIST['Frequency'] = WORD_LIST.apply(lambda row: wf(row['Word'], 'en'), axis = 1)
        self.__WORD_LIST = WORD_LIST.sort_values(by=['Frequency'], ascending=False)
        self.iterNum = 0
        self.guesses = []
        self.__temp = ['[a-z]'] * length
        self.__status = True

    def start(self):
        print('Enter the word "TARES"')
        greenDict = {}
        while self.__status:
            greenTemp = True
            rejected = input('\nWhat letters are grayed out? Enter them with a space in-between:\t\t').split(' ')
            contained = input('\nWhat letters are yellowed out? Enter them with a space in-between:\t\t').split(' ')
            green = input('\nEnter a letter that is green, followed by a space and the position it is located. (0 refers to the first letter of the word):\t\t').split(' ')
            if green == ['']:
                greenTemp = False
            while greenTemp:
                checkGreen = input('\nAre there any more green letters? (Y/N):\t\t').lower()
                if checkGreen == 'n':
                    greenTemp = False
                else:
                    green = input('\nEnter a letter that is green, followed by a space and the position it is located. (0 refers to the first letter of the word):\t\t').split(' ')
                greenDict[green[0]] = int(green[1])
                
            self.WordGuesser(greenLetters = greenDict, yellowLetters=contained, grayLetters=rejected)
            check = input('\nWas that the final answer? (Y/N):\t\t').lower()
            if check == 'y':
                self.__status = False

    def end(self):
        print('\n\n\n\nThanks for using the Wordle Guesser')
        print(f"We completed today's word in {self.iterNum} iterations")
        print(f"Your guesses today are {self.guesses[:-2]}, with the final answer being '{self.guesses[-1]}'.")

    def WordGuesser(self, greenLetters = None, yellowLetters = [], grayLetters = []):
        self.iterNum += 1
        if grayLetters:
            for rejected in grayLetters:
                self.__notContains(rejected)
        if yellowLetters:
            for contained in yellowLetters:
                self.__contains(contained)
        if greenLetters:
            for accepted in greenLetters:
                self.__has(accepted, greenLetters[accepted])       


        print(self.__WORD_LIST)
        try:
            self.guesses.append(self.__WORD_LIST.iloc[0,0])
            print(f'\n\n\n\nI recommend entering: {self.__WORD_LIST.iloc[0,0]}\n\n\n\n') 
        except:
            print('\n\n\n\nNo more available words to guess from\n\n\n\n')

    def __notContains(self, letter):
        self.__WORD_LIST = self.__WORD_LIST[self.__WORD_LIST.iloc[:,0].str.contains(r"{}".format(letter)) == False]

    def __contains(self, letter):
        self.__WORD_LIST = self.__WORD_LIST[self.__WORD_LIST.iloc[:,0].str.contains(r"{}".format(letter))]

    def __has(self, letter, position):
        self.__contains(letter)
        self.__temp[position] = letter
        self.__WORD_LIST = self.__WORD_LIST[self.__WORD_LIST.iloc[:,0].str.contains(r"{}{}{}{}{}".format(self.__temp[0],self.__temp[1],self.__temp[2],self.__temp[3],self.__temp[4],), regex = True)]

    def getTemp(self):
        return self.__temp

    def getWordList(self):
        return self.__WORD_LIST

    def checkWordList(self, word):
        result = self.__WORD_LIST[self.__WORD_LIST['Word'] == word]
        return print(result)



if __name__ == '__main__':
    game = WordleGuesser()
    game.start()
    game.end()