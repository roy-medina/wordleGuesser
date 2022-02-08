import pandas as pd 
from english_words import english_words_lower_alpha_set
from wordfreq import zipf_frequency as wf

def get_all_wordle_words():
    with open("all_wordle_words.txt", "r") as infile:
        return [line.strip() for line in infile.readlines()]

# words_to_choose_from = list(english_words_lower_alpha_set) + get_all_wordle_words()
# words_to_choose_from = list(set(words_to_choose_from))
words_to_choose_from = get_all_wordle_words()

LENGTH = 5

class WordleGuesser():
    def __init__(self, length = LENGTH):
        ### Initialize
        WORD_LIST = pd.DataFrame(words_to_choose_from, columns=['Word'])
        ### Filter by length
        WORD_LIST = WORD_LIST[WORD_LIST.iloc[:,0].str.len() == LENGTH]
        ### Implement frequency of words
        WORD_LIST['Frequency'] = WORD_LIST.apply(lambda row: wf(row['Word'], 'en'), axis = 1)
        self.__WORD_LIST = WORD_LIST.sort_values(by=['Frequency'], ascending=False)
        self.iterNum = 0
        self.guesses = []
        self.__duplicates = []
        self.__containedNotIn = {}
        for num in range(LENGTH):
            self.__containedNotIn[num] = []
        self.__temp = ['[a-z]'] * length
        self.__status = True

    def start(self):
        print('Enter the word "TARES"')
        greenDict = {}
        while self.__status:
            yellowDict = {}
            greenTemp = True
            yellowTemp = True
            rejected = input('\nWhat letters are grayed out? Enter them with a space in-between:\t\t').split(' ')
            if rejected == ['']:
                rejected = None
            yellow = input('\nEnter a letter that is yellow, followed by a space and the position it is located. (0 refers to the first letter of the word):\t\t').split(' ')
            if yellow == ['']:
                yellowTemp = False
                yellow = None
            else: 
                yellowDict[yellow[0]] = int(yellow[1])
            while yellowTemp:
                checkyellow = input('\nAre there any more yellow letters? (Y/N):\t\t').lower()
                if checkyellow == 'n':
                    yellowTemp = False
                else:
                    yellow = input('\nEnter a letter that is yellow, followed by a space and the position it is located. (0 refers to the first letter of the word):\t\t').split(' ')
                yellowDict[yellow[0]] = int(yellow[1])

            green = input('\nEnter a letter that is green, followed by a space and the position it is located. (0 refers to the first letter of the word):\t\t').split(' ')
            if green == ['']:
                greenTemp = False
                green = None
            else:
                greenDict[green[0]] = int(green[1])
            while greenTemp:
                checkGreen = input('\nAre there any more green letters? (Y/N):\t\t').lower()
                if checkGreen == 'n':
                    greenTemp = False
                else:
                    green = input('\nEnter a letter that is green, followed by a space and the position it is located. (0 refers to the first letter of the word):\t\t').split(' ')
                greenDict[green[0]] = int(green[1])
                
            self.WordGuesser(greenLetters = greenDict, yellowLetters=yellowDict, grayLetters=rejected)
            check = input('\nWas that the final answer? (Y/N):\t\t').lower()
            if check == 'y':
                self.__status = False

    def end(self):
        print('\n\n\n\nThanks for using the Wordle Guesser')
        print(f"We completed today's word in {self.iterNum} iterations")
        print(f"Your guesses today are {self.guesses[:-1]}, with the final answer being '{self.guesses[-1]}'.")

    def WordGuesser(self, greenLetters = None, yellowLetters = None, grayLetters = None):
        self.iterNum += 1
        if grayLetters:
            for rejected in grayLetters:
                self.__notContains(rejected)
        if yellowLetters:
            for contained in yellowLetters:
                self.__contains(contained, yellowLetters[contained])
        if greenLetters:
            for accepted in greenLetters:
                self.__has(accepted, greenLetters[accepted])  
        for key in yellowLetters.keys():
            if not key in self.__duplicates:
                if key in greenLetters.keys():
                    self.__duplicates.append(key)
        if self.__duplicates:
            self.__checkDups()
            self.__duplicates = []


        print(self.__WORD_LIST)
        try:
            self.guesses.append(self.__WORD_LIST.iloc[0,0])
            print(f'\n\n\n\nI recommend entering: {self.__WORD_LIST.iloc[0,0]}\n\n\n\n') 
        except:
            print('\n\n\n\nNo more available words to guess from\n\n\n\n')

    def __notContains(self, letter):
        self.__WORD_LIST = self.__WORD_LIST[self.__WORD_LIST.iloc[:,0].str.contains(r"{}".format(letter)) == False]

    def __contains(self, letter, position):
        if not letter in self.__containedNotIn[position]:
            self.__containedNotIn[position].append(letter)
            self.__temp[position] = f'[^{"".join(self.__containedNotIn[position])}]'
            self.__WORD_LIST = self.__WORD_LIST[self.__WORD_LIST.iloc[:,0].str.contains(r"{}{}{}{}{}".format(self.__temp[0],self.__temp[1],self.__temp[2],self.__temp[3],self.__temp[4],), regex = True)]
        self.__WORD_LIST = self.__WORD_LIST[self.__WORD_LIST.iloc[:,0].str.contains(r"{}".format(letter))]

    def __has(self, letter, position):
        self.__temp[position] = letter
        self.__WORD_LIST = self.__WORD_LIST[self.__WORD_LIST.iloc[:,0].str.contains(r"{}{}{}{}{}".format(self.__temp[0],self.__temp[1],self.__temp[2],self.__temp[3],self.__temp[4],), regex = True)]

    def __checkDups(self):
        for letter in self.__duplicates:
            self.__WORD_LIST = self.__WORD_LIST[self.__WORD_LIST['Word'].str.count(letter) == 2]
        
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
