from tkinter import *
import tkinter.messagebox
import random
from random import shuffle
import string


class FourPicsOneWord(Tk):
    def __init__(self):
        super().__init__()
        # Save Progress
        self.picfileNames = list()
        self.donePictures = list()

        # Variables
        self.picNumber = 0
        self.currentLevel = 1
        self.currentCoins = 100
        self.boxContainer = []
        self.index = 0
        self.numberOfButtons = 12
        self.userWord = ''
        self.pressedButtons = []
        self.btns = []
        self.skippedPictures = []

        # Check Progress File
        seeProgress = open('gameFile.txt', 'r')
        seeInfo = seeProgress.readlines()
        for i in seeInfo:
            clr = i.strip().split(',')
            self.currentLevel = int(clr[0])
            self.currentCoins = int(clr[1])
            for item in clr[2].split('*'):
                if item != '':
                    self.donePictures.append(item)
        seeProgress.close()

        # Append Pictures to list
        f = open('picList.txt', 'r')
        x = f.readlines()

        for p in x:
            fn = p.strip().split(';')
            if fn[1] not in self.donePictures:
                self.picfileNames.append(fn[1])
        f.close()

        # Word to guess
        self.wordGuess = self.picfileNames[self.picNumber]

        # Design
        self.title('4 Pics 1 Word')
        self.geometry('500x700')
        self.configure(bg='#24293E')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.onClosing)

        # Widgets
        frameOne = Frame(self, height=50, width=500, bg='#2F3855')
        frameOne.place(x=0, y=0)

        self.lblLevel = Label(frameOne, text='LEVEL: %s' % (self.currentLevel), font=('Helvetica', 20, 'bold'), fg='#F4F5FC', bg='#2F3855')
        self.lblLevel.place(x=10, y=6)

        self.lblValue = Label(frameOne, text='%s' % (self.currentCoins), font=('Helvetica', 20, 'bold'), fg='#F4F5FC', bg='#2F3855')
        self.lblValue.place(x=435, y=6)

        self.coinImage = PhotoImage(file='coin.png')
        self.lblCoin = Label(frameOne, image=self.coinImage, bg='#2F3855')
        self.lblCoin.place(x=390, y=3)

        self.pics = PhotoImage(file=self.picfileNames[self.picNumber]+'.png')
        self.lblPics = Label(self, image=self.pics, bg='#F4F5FC', highlightthickness=3)
        self.lblPics.place(x=100, y=74)

        self.lightBulbImage = PhotoImage(file='lightbulb.png')
        self.btnLightBulb = Button(self, image=self.lightBulbImage, bg='#24293E', borderwidth=0, command=self.hint)
        self.btnLightBulb.place(x=440, y=485)

        self.passImage = PhotoImage(file='pass.png')
        self.btnNextPic = Button(self, image=self.passImage, bg='#24293E', borderwidth=0, command=self.changeImage)
        self.btnNextPic.place(x=440, y=535)

        self.clearImage = PhotoImage(file='clear.png')
        self.btnClear = Button(self, image=self.clearImage, bg='#24293E', borderwidth=0, command=self.clearGuess)
        self.btnClear.place(x=180, y=630)

        self.newGameButton = PhotoImage(file='newgame.png')
        self.btnNewGame = Button(self, image=self.newGameButton, bg='#24293E', borderwidth=0, command=self.gameResetConfirmation)
        self.btnNewGame.place(x=20, y=630)

        self.char_of_Word = len(self.wordGuess)
        self.bg1 = Frame(self, height=65, width=60 * len(self.wordGuess), bg='#F4F5FC')
        self.bg1.place(relx=0.5, rely=0.61, anchor=CENTER)

        self.frameTwoButtons = Frame(self, height=200, width=325, bg='#F4F5FC')
        self.frameTwoButtons.place(relx=0.5, rely=0.76, anchor=CENTER)

        self.frameTwo = Frame(self, height=50, width=100, bg='#24293E')
        self.frameTwo.place(relx=0.5, rely=0.61, anchor=CENTER)

        for i, o in zip(range(self.char_of_Word), self.wordGuess.upper()):
            self.letter_box = Label(self.frameTwo, bg='#8EBBFF', relief='flat', highlightbackground='#24293E', highlightthickness=1,  width=4, height=2, text=o, fg='#8EBBFF', font=('Helvetica', 14, 'bold'))
            self.letter_box.grid(row=1, column=i)
            self.boxContainer.append(self.letter_box)

        # Initialize Jumbled Letters
        r = 0
        y = 0
        numOfRandomLetters = self.numberOfButtons - len(self.wordGuess)
        randomLetters = ''.join(random.choice(string.ascii_uppercase) for x in range(numOfRandomLetters))
        joinedLetters = list(str(self.wordGuess + randomLetters).upper())
        shuffle(joinedLetters)
        self.jumbledWord = ''.join(joinedLetters)
        for i in range(len(self.jumbledWord)):
            btnLetter = Button(self.frameTwoButtons, text=self.jumbledWord[i], command=lambda i=i: self.displayText(i, self.jumbledWord), width=4, height=1, font=('Helvetica', 15, 'bold'), fg='#272727', bg='#F4F5FC')
            btnLetter.grid(row=r, column=y, sticky=W)
            self.btns.append(btnLetter)
            y += 1
            if i != 0 and y == 6:
                r += 1
                y = 0

    # Most Important Part of Code, It updates the state of the game.
    def updateGameState(self):
        # Delete Previous Game State
        self.char_of_Word = len(self.wordGuess)
        self.bg1.destroy()
        self.frameTwo.destroy()
        for widget in self.frameTwoButtons.grid_slaves():
            widget.destroy()
        for box in self.boxContainer:
            box.destroy()
        self.boxContainer.clear()
        self.pressedButtons.clear()
        self.btns.clear()
        self.index = 0
        self.lblLevel.configure(text='LEVEL: %s' % (self.currentLevel))
        self.lblValue.configure(text=self.currentCoins)
        self.pics.configure(file=self.picfileNames[self.picNumber] + '.png')

        # Create New Game State and Update State
        self.bg1 = Frame(self, height=65, width=60 * len(self.wordGuess), bg='#F4F5FC')
        self.bg1.place(relx=0.5, rely=0.61, anchor=CENTER)

        self.frameTwo = Frame(self, height=50, width=100, bg='#24293E')
        self.frameTwo.place(relx=0.5, rely=0.61, anchor=CENTER)

        # Reshuffle
        for i, o in zip(range(self.char_of_Word), self.wordGuess.upper()):
            self.letter_box = Label(self.frameTwo, bg='#8EBBFF', relief='flat', highlightbackground='#24293E',
                                    highlightthickness=1, width=4, height=2, text=o, fg='#8EBBFF',
                                    font=('Helvetica', 14, 'bold'))
            self.letter_box.grid(row=1, column=i)
            self.boxContainer.append(self.letter_box)
        r = 0
        y = 0
        numOfRandomLetters = self.numberOfButtons - len(self.wordGuess)
        randomLetters = ''.join(random.choice(string.ascii_uppercase) for x in range(numOfRandomLetters))
        joinedLetters = list(str(self.wordGuess + randomLetters).upper())
        shuffle(joinedLetters)
        self.jumbledWord = ''.join(joinedLetters)
        for i in range(len(self.jumbledWord)):
            btnLetter = Button(self.frameTwoButtons, text=self.jumbledWord[i],
                               command=lambda i=i: self.displayText(i, self.jumbledWord), width=4, height=1,
                               font=('Helvetica', 15, 'bold'), fg='#272727', bg='#F4F5FC')
            btnLetter.grid(row=r, column=y, sticky=W)
            self.btns.append(btnLetter)
            y += 1
            if i != 0 and y == 6:
                r += 1
                y = 0

    def changeImage(self):
        changeCost = 10

        if self.currentCoins < changeCost:
            self.insufficientCoinsImage = PhotoImage(file='insufficient.png')
            self.lblInsufficientCoins = Label(self, image=self.insufficientCoinsImage, bg='#24293E', borderwidth=0)
            self.lblInsufficientCoins.place(x=125, y=200)
            self.lblInsufficientCoins.after(2000, self.lblInsufficientCoins.destroy)
            return

        # Store the current picNumber as previousPicNumber
        self.currentCoins -= changeCost
        self.previousPicNumber = self.picNumber
        # Check if there are any more skipped pictures to show
        if not self.skippedPictures:
            # Update picNumber to the next index in picfileNames list
            self.picNumber += 1
            if self.picNumber == len(self.picfileNames):
                self.picNumber = 0
            self.wordGuess = self.picfileNames[self.picNumber]
        else:
            # Show the next skipped picture, if any
            self.wordGuess = self.skippedPictures.pop(0)

            # Check if the skipped picture has already been passed
            if self.wordGuess in self.skippedPictures:
                self.skippedPictures.append(self.wordGuess)
                self.changeImage()
                return

        self.userWord = ''
        self.updateGameState()

    def hint(self):
        hintCost = 2
        if self.currentCoins < hintCost:
            self.insufficientCoinsImage = PhotoImage(file='insufficient.png')
            self.lblInsufficientCoins = Label(self, image=self.insufficientCoinsImage, bg='#24293E', borderwidth=0)
            self.lblInsufficientCoins.place(x=125, y=200)
            self.lblInsufficientCoins.after(2000, self.lblInsufficientCoins.destroy)
            return

        self.currentCoins -= hintCost

        hinted_letter = self.wordGuess[self.index]
        # Find the lowest index of the substring in the given string    
        hinted_letter_index = self.jumbledWord.upper().find(hinted_letter.upper())

        while hinted_letter_index in self.pressedButtons:
            # if the hinted letter has already been pressed, find the next occurrence
            hinted_letter_index = self.jumbledWord.upper().find(hinted_letter.upper(), hinted_letter_index + 1)

        self.btns[hinted_letter_index].config(state=DISABLED, bg='#83899F')
        self.pressedButtons.append(hinted_letter_index)
        self.userWord = self.userWord + self.wordGuess[self.index]
        self.boxContainer[self.index].configure(text=self.wordGuess[self.index].upper(), fg='#24293E')
        self.lblValue.configure(text=self.currentCoins)
        self.index += 1
        if self.index == (len(self.wordGuess)):
            self.isCorrect()


    def clearGuess(self):
        self.index = 0
        self.userWord = ''
        self.clearBoxes()
        self.pressedButtons = []


    def clearBoxes(self):
        for i in range(len(self.wordGuess)):
            self.boxContainer[i].configure(text='')
        for i, btn in enumerate(self.btns):
            if btn.cget('state') == 'disabled' and (btn.cget('bg') == '#83899F' or btn.cget('bg') == '#A9FF65'):
                btn.config(state=NORMAL, bg='#F4F5FC')
        for i in self.pressedButtons:
            self.btns[i].config(state=NORMAL, bg='#F4F5FC')


    def isCorrect(self):
        self.index = 0
        for i, btn in enumerate(self.btns):
            if btn.cget('state') == 'normal' and btn.cget('bg') == '#F4F5FC':
                btn.config(state=DISABLED, bg='#83899F')

        if self.userWord.lower() == self.wordGuess.lower():
            for i in self.pressedButtons:
                self.btns[i].config(state=DISABLED, bg='#A9FF65')
            self.userWord = ''
            correctWidget = self.correctAnswer()
            correctWidget.after(3000, correctWidget.destroy)
            self.after(3000, self.nextLevel)

        else:
            self.userWord = ''
            wrongWidget = self.wrongAnswer()
            wrongWidget.after(3000, wrongWidget.destroy)

        self.pressedButtons = []
        self.after(3000, self.clearBoxes)


    def correctAnswer(self):
        self.correctAnswerImage = PhotoImage(file='correct.png')
        self.lblCorrectAnswer = Label(self, image=self.correctAnswerImage, bg='#24293E', borderwidth=0)
        self.lblCorrectAnswer.place(x=125, y=200)
        return self.lblCorrectAnswer


    def wrongAnswer(self):
        self.incorrectAnswerImage = PhotoImage(file='incorrect.png')
        self.lblIncorrectAnswer = Label(self, image=self.incorrectAnswerImage, bg='#24293E', borderwidth=0)
        self.lblIncorrectAnswer.place(x=125, y=200)
        return self.lblIncorrectAnswer


    def displayText(self, value, j_words):
        letter = j_words[value]
        self.boxContainer[self.index].configure(text=letter, fg='#24293E')
        self.pressedButtons.append(value)
        self.btns[value].config(state=DISABLED, bg='#83899F')
        if self.index + 1 == (len(self.wordGuess)):
            self.userWord = self.userWord + letter
            self.isCorrect()
        else:
            self.userWord = self.userWord + letter
            self.index += 1


    def nextLevel(self):
        self.donePictures.append(self.wordGuess)

        if self.currentLevel + 1 == 51:
            self.winnerFrame = Frame(self, height=700, width=500, bg='#24293E')
            self.winnerFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

            self.winnerFrame.lift()
            self.winnerImage = PhotoImage(file='winner.png')
            self.lblWinner = Label(self, image=self.winnerImage, bg='#24293E')
            self.lblWinner.place(relx=0.5, rely=0.4, anchor=CENTER)
            self.lblTotalScore = Label(self, text='Score: %s Coins Left!' % (self.currentCoins), font=('Helvetica', 20, 'bold'), fg='#F4F5FC', bg='#24293E')
            self.lblTotalScore.place(relx=0.5, rely=0.6, anchor=CENTER)
            self.winnerNewGameButton = Button(self, image=self.newGameButton, bg='#24293E', borderwidth=0, command=self.gameReset)
            self.winnerNewGameButton.place(relx=0.5, rely=0.7, anchor=CENTER)

        else:
            # Update Progress
            self.currentLevel += 1
            self.currentCoins += 10
            self.picNumber += 1
            if self.picNumber == len(self.picfileNames):
                self.picNumber = 0
            self.wordGuess = self.picfileNames[self.picNumber]

            self.updateGameState()


    def onClosing(self):
        if self.currentLevel + 1 == 51:
            result = tkinter.messagebox.askyesno(title=None, message='Thank you for Playing!\nClosing the window will reset back to Level 1.')
            if result:
                # Reset Values when Player closes the window.
                self.picfileNames.clear()
                self.donePictures.clear()
                f = open('picList.txt', 'r')
                x = f.readlines()
                for p in x:
                    fn = p.strip().split(';')
                    self.picfileNames.append(fn[1])
                f.close()

                self.picNumber = 0
                self.currentLevel = 1
                self.currentCoins = 100
                self.boxContainer = list()
                self.index = 0
                self.numberOfButtons = 12
                self.userWord = ''
                self.wordGuess = self.picfileNames[self.picNumber]

                saveProgress = open('gameFile.txt', 'w')
                saveProgress.write('%s,%s,' % (self.currentLevel, self.currentCoins))
                for done in self.donePictures:
                    if self.donePictures.index(done) == -1:
                        saveProgress.write(done)
                    else:
                        saveProgress.write('%s*' % (done))
                saveProgress.close()
                self.destroy()
            else:
                return
        else:
            result = tkinter.messagebox.askyesno(title=None, message='Are you sure you want to exit?\nProgress will be saved.')
            if result:
                saveProgress = open('gameFile.txt', 'w')
                saveProgress.write('%s,%s,' % (self.currentLevel, self.currentCoins))
                for done in self.donePictures:
                    if self.donePictures.index(done) == -1:
                        saveProgress.write(done)
                    else:
                        saveProgress.write('%s*' % (done))
                saveProgress.close()
                self.destroy()
            else:
                return

    def gameResetConfirmation(self):
        result = tkinter.messagebox.askyesno(title=None, message='Are you sure you want to make a new game?\nProgress will be lost.')
        if result:
            self.gameReset()
        else:
            return

    def gameReset(self):
        if self.currentLevel + 1 == 51:
            self.winnerFrame.destroy()
            self.lblWinner.destroy()
            self.lblTotalScore.destroy()
            self.winnerNewGameButton.destroy()
        # Reset Values
        self.picfileNames.clear()
        self.donePictures.clear()
        f = open('picList.txt', 'r')
        x = f.readlines()
        for p in x:
            fn = p.strip().split(';')
            self.picfileNames.append(fn[1])
        f.close()

        self.picNumber = 0
        self.currentLevel = 1
        self.currentCoins = 100
        self.boxContainer = list()
        self.index = 0
        self.numberOfButtons = 12
        self.userWord = ''
        self.wordGuess = self.picfileNames[self.picNumber]

        self.lblLevel.configure(text='LEVEL: %s' % (self.currentLevel))
        self.lblValue.configure(text=self.currentCoins)
        self.pics.configure(file=self.picfileNames[self.picNumber] + '.png')

        self.updateGameState()


def main():
    root = FourPicsOneWord()
    root.mainloop()


if __name__ == '__main__':
    main()
