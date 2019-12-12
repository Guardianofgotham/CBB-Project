from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import gzip
import os
from bs4 import BeautifulSoup
import getpass
import tkinter
from tkinter import messagebox
from selenium.webdriver.support.ui import Select
from collections import Counter
import sys
import subprocess




# UGAAGCUCUCGUUGGUUGAU
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def welcome():
   messagebox.showinfo('RNA 3D STRUCTURE',"Enter valid inputs and click on next. Then click Submit to run the program.")

# Function to open downloaded files
def openDownloadedFiles():
    pathToDownloadsFolder = "/Users/ritvikgupta/Downloads/"#"C:\\Users\\"+getpass.getuser()+"\\Downloads\\";

    DownloadedFiles = os.listdir(pathToDownloadsFolder)

    for file in DownloadedFiles:
        if file[-3:] == ".gz":
            gzipFile = gzip.GzipFile(filename=pathToDownloadsFolder + file, mode='rb')
            content = gzipFile.read()
            gzipFile.close()
            location = open(pathToDownloadsFolder + file[:-3], 'wb')
            location.write(content)
            location.close()

    getUpdatedFilesDirectory = os.listdir(pathToDownloadsFolder)

    for file in getUpdatedFilesDirectory:
        if file[-3:] == "pdb":
            open_file(pathToDownloadsFolder + file)#os.startfile(pathToDownloadsFolder + file)


# Function to return the most stable structure number
def getMostStableStructure(HTMLFile):
    soup = BeautifulSoup(HTMLFile, "html.parser").get_text()
    ind = soup.index("Structures sorted by energy")
    proteinNumber = int(soup[ind + 59:ind + 61])
    print(proteinNumber)
    return proteinNumber


# Function to remove previous files
def removePrevFiles():
    path = "/Users/ritvikgupta/Downloads/"#"C:\\Users\\"+getpass.getuser()+"\\Downloads\\";
    listOfPrevFiles = os.listdir(path)
    for file in listOfPrevFiles:
        if (file[-3:] == ".gz" or file[-3:] == "pdb"):
            os.remove(path + file)


# Function to check weather integer or not
def isInt(var):
    try:
        int(var)
        return True
    except:
        return False


# function to verify Correcteness of input
def verifyInput():
    if (Sequence1TextBox.get() == '' or TimeOutTextBox.get() == ''):
        messagebox.showinfo("Missing Field", "Sequence and Timeout are mandatory field")
        return
    if (not isInt(TimeOutTextBox.get())):
        messagebox.showinfo("Value Error", "Timeout Must be a number")
        return
    currentEnteredSequence = Sequence1TextBox.get()
    if (currentEnteredSequence in GlobalVarForUserSequencesThrough):
        messagebox.showinfo("Repeated Sequence", "You're repeating Sequence")
        return
    for i in currentEnteredSequence:
        if (i == 'A' or i == 'U' or i == 'G' or i == 'C'):
            continue
        else:
            messagebox.showinfo("Incorrect Sequence", "A, U, G, C are the only Valid Characters in Sequence")
            return
    return True


# Function to Store input ("Next" event Handler)
def storeInput():
    if (verifyInput() == None):
        return
    print("StoringInput")
    GlobalVarForUserSequencesThrough.append(Sequence1TextBox.get())
    Sequence1TextBox.delete(0, len(Sequence1TextBox.get()))
    TimeOut.append(int(TimeOutTextBox.get()))


# Function to get structure from VS Fold
def getSecondaryStructureFromVSfold(sequence):
    UserSequence = sequence
    ChromeBrowser.get('http://www.rna.it-chiba.ac.jp/~vsfold/vsfold5/')
    SequeunceTextField = ChromeBrowser.find_element_by_name('SEQU')
    print("\nFeeding Sequence")
    SequeunceTextField.send_keys(UserSequence)
    enterbutton = ChromeBrowser.find_element_by_name("SNAM")
    enterbutton.send_keys("basil")
    enterbutton.send_keys(Keys.ENTER)
    ChromeBrowser.switch_to_window(ChromeBrowser.window_handles[-1])
    time.sleep(5)

    # print(ChromeBrowser.page_source)
    submitbutton = ChromeBrowser.find_element_by_link_text("basil_ss.ss")
    submitbutton.click()
    time.sleep(1)
    ChromeBrowser.switch_to_window(ChromeBrowser.window_handles[-1])
    HTMLFile = ChromeBrowser.page_source
    soup = BeautifulSoup(HTMLFile).get_text()

    structindex = soup.find(sequence)
    strlen = len(UserSequence)
    finalstr = soup[structindex + strlen + 1:structindex + strlen + 1 + strlen]
    # print(finalstr)
    # time.sleep(100)
    # ChromeBrowser.close()
    return finalstr


# Function to get Structure from RNA Fold
def getSecondaryStructureFromRNAFold(inputSequence):
    ChromeBrowser.get('http://rna.tbi.univie.ac.at/cgi-bin/RNAWebSuite/RNAfold.cgi')
    SequenceTextArea = ChromeBrowser.find_element_by_name("SCREEN")
    SequenceTextArea.send_keys(">structure\n" + inputSequence)
    proceedButton = ChromeBrowser.find_element_by_name("proceed")
    proceedButton.click()
    while (True):
        try:
            Structure = ChromeBrowser.find_element_by_id("MFE_structure_span")
            break
        except:
            print("Waiting...")
            time.sleep(3)

    # ChromeBrowser.close()
    return Structure.text[7:]


# Function to get structure from MC Fold
def getSecondaryStructureFromMCFold(inputSequence):
    ChromeBrowser.get("https://major.iric.ca/MC-Fold/")
    SequeunceTextField = ChromeBrowser.find_element_by_name('sequence')
    SequeunceTextField.send_keys(inputSequence)
    SelectionOfNumberOfStructures = Select(ChromeBrowser.find_element_by_name("top"))
    SelectionOfNumberOfStructures.select_by_visible_text("1")
    SequeunceTextField.send_keys(Keys.ENTER)
    EditButton = ChromeBrowser.find_element_by_link_text("edit")
    EditButton.click()
    ChromeBrowser.switch_to.window(ChromeBrowser.window_handles[-1])
    AreaInWhichTextIsPresent = ChromeBrowser.find_element_by_name("scriptgen")
    WholeText = AreaInWhichTextIsPresent.text
    # AreaInWhichTextIsPresent.clear()

    return WholeText[-len(inputSequence):]


# Function That Will Generate GUI
def generateGUI():
    # BlankLabel
    BLabel1 = tkinter.Label(MainWindow, text="\t         ", font=("Comic sans MS", 15))
    BLabel1.grid(column=0, row=1)
    BLabel1.config(background='black')
    BLabel2 = tkinter.Label(MainWindow, text="", font=("Comic sans MS", 15))
    BLabel2.grid(column=2, row=0)
    BLabel2.config(background='black')

    # blank label
    Sequence1Label = tkinter.Label(MainWindow, text="\t        ", font=("Comic sans MS", 15))
    Sequence1Label.grid(column=1, row=0)
    Sequence1Label.config(bg='black', fg='white', height=2, width=17)

    # Creating label for Sequence1
    Sequence1Label = tkinter.Label(MainWindow, text="ENTER SEQUENCE   :", font=("Comic sans MS", 15))
    Sequence1Label.grid(column=1, row=1)
    Sequence1Label.config(bg='black', fg='white', height=2, width=17)

    # blank label
    Sequence1Label = tkinter.Label(MainWindow, text="\t        ", font=("Comic sans MS", 15))
    Sequence1Label.grid(column=1, row=2)
    Sequence1Label.config(bg='black', fg='white', height=2, width=17)

    # Textbox for Sequence 1
    Sequence1TextBox.grid(column=3, row=1)

    # Creating label for timeout
    TimeOutLabel = tkinter.Label(MainWindow, text="                TIME OUT  :", font=("Comic sans MS", 15))
    TimeOutLabel.grid(column=1, row=3)
    TimeOutLabel.config(bg='black', fg='white', height=2, width=17)

    # TextBox for timeout
    TimeOutTextBox.grid(column=3, row=3)

    # blank label
    Sequence1Label = tkinter.Label(MainWindow, text="\t        ", font=("Comic sans MS", 15))
    Sequence1Label.grid(column=1, row=4)
    Sequence1Label.config(bg='black', fg='white', height=2, width=17)

    # NEXT Button
    NextButton = tkinter.Button(MainWindow, text="NEXT", command=storeInput)
    NextButton.grid(column=1, row=5)
    NextButton.config(height=2, width=10, bg='black', fg='white')

    # Submit Button
    SubmitButton = tkinter.Button(MainWindow, text="SUBMIT", command=MainWindow.destroy)
    SubmitButton.grid(column=3, row=5)
    SubmitButton.config(height=2, width=10, bg='black', fg='white')

    MainWindow.mainloop()
    print(GlobalVarForUserSequencesThrough)
    print(TimeOut)
    return [GlobalVarForUserSequencesThrough, TimeOut]


# Fuction to Generate consensus sequence
def getConsesusSequence():
    consensusSequence = ""
    for i in range(len(MCFoldStructure)):
        temp = list()
        temp.extend([MCFoldStructure[i], RNAFoldStructure[i], VSFoldStructure[i]])
        frequency = Counter(temp)
        maxFreq = max(frequency.values())
        for i in frequency.keys():
            if (frequency.get(i) == maxFreq):
                consensusSequence += i
                break
    return consensusSequence


# Creating Main Window
MainWindow = tkinter.Tk()

# Giving title to Window
MainWindow.title("3D RNA")
MainWindow.geometry("750x400")
MainWindow.resizable(False, False)
MainWindow.config(background='black')

Sequence1TextBox = tkinter.Entry(MainWindow)  # Global Variable
TimeOutTextBox = tkinter.Entry(MainWindow)  # Global Variable

GlobalVarForUserSequencesThrough = []
TimeOut = []

UserInputFromGUI = generateGUI()

AllSequences = UserInputFromGUI[0]
skippedSequences = []
for i in range(len(UserInputFromGUI[0])):
    skippedSequences.append(False)

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

ChromeBrowser = webdriver.Chrome(os.getcwd() + '/chromedriver', options=chrome_options)#'\\chromedriver.exe'
ChromeBrowser.maximize_window()
removePrevFiles()

for UserSequence in range(len(AllSequences)):

    RNAFoldStructure = getSecondaryStructureFromRNAFold(AllSequences[UserSequence])
    VSFoldStructure = getSecondaryStructureFromVSfold(AllSequences[UserSequence])
    MCFoldStructure = getSecondaryStructureFromMCFold(AllSequences[UserSequence])

    ConsensusSequence = getConsesusSequence()

    ChromeBrowser.close()

    print("Switching window")
    ChromeBrowser.switch_to.window(ChromeBrowser.window_handles[-1])
    ChromeBrowser.back()

    SequeunceTextField = ChromeBrowser.find_element_by_name('sequence')
    # SequeunceTextField.send_keys(AllSequences[UserSequence])
    SelectionOfNumberOfStructures = Select(ChromeBrowser.find_element_by_name("top"))
    SelectionOfNumberOfStructures.select_by_visible_text("1")

    ConstraintTextArea = ChromeBrowser.find_element_by_name("mask");
    ConstraintTextArea.send_keys(ConsensusSequence)

    ConvertDotsToUnconstrainedCheckBox = ChromeBrowser.find_element_by_name("convert")
    ConvertDotsToUnconstrainedCheckBox.click()

    SequeunceTextField.send_keys(Keys.ENTER)

    SubmitButton = ChromeBrowser.find_element_by_link_text("submit")
    SubmitButton.click()

    ChromeBrowser.switch_to.window(ChromeBrowser.window_handles[-1])
    REFRESH_TIME = 10  # in Seconds
    TotalTime = 0
    TIMEOUT = UserInputFromGUI[1][UserSequence] * 60  # User specific to that Sequence
    skipped = False
    while (True):
        try:
            print("Refresing Window...")
            ChromeBrowser.refresh()
            PDBFile = ChromeBrowser.find_element_by_link_text("structure-0001.pdb.gz")
            break
        except:
            time.sleep(REFRESH_TIME)
            TotalTime += REFRESH_TIME
            if (TotalTime >= TIMEOUT):
                print("TimedOut!!!\nSkiping...")
                ChromeBrowser.close()
                ChromeBrowser.switch_to.window(ChromeBrowser.window_handles[0])
                skipped = True
                skippedSequences[UserSequence] = True
                break
    if (skipped):
        continue
    CommandsHtmlLink = ChromeBrowser.find_element_by_link_text("commands.html")
    print("Going to Commands")
    CommandsHtmlLink.click()

    time.sleep(4)

    ScoreRadioButton = ChromeBrowser.find_element_by_name("score")
    print("Selecting Score Field")  # not using entropy
    ScoreRadioButton.click()

    time.sleep(4)

    print("Analyzing")
    AnalyzeButton = ChromeBrowser.find_element_by_xpath("//input[@value = 'Analyze']")
    AnalyzeButton.click()

    HTMLFile = ChromeBrowser.page_source

    print("Sorting...")
    stuctureNumberToDownload = getMostStableStructure(HTMLFile)

    time.sleep(4)

    print("Going Back")
    ChromeBrowser.back()

    time.sleep(4)

    print("Going Back")
    ChromeBrowser.back()

    nameOfTheFileToBeDownloaded = "structure-%04d.pdb.gz" % stuctureNumberToDownload

    ObjectOf_PDB_FileToBeDownloaded = ChromeBrowser.find_element_by_link_text(nameOfTheFileToBeDownloaded)

    ObjectOf_PDB_FileToBeDownloaded.click()

    print("Downloading...")

    time.sleep(4)

    print("Closing Current Window")
    ChromeBrowser.close()
    time.sleep(2)
    ChromeBrowser.switch_to.window(ChromeBrowser.window_handles[0])

for i in range(len(skippedSequences)):
    if (skippedSequences[i]):
        print("Skipped Sequence %d" % (i + 1))
print("Program Suffered 0 error")
print("Closing Browser...")
ChromeBrowser.quit()

openDownloadedFiles()

exit()
