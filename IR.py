import wx
import os
# import main

import sys
import nltk
import glob
from nltk.tokenize import RegexpTokenizer
from nltk import PorterStemmer


def combine_indexes(words_list_stemmed, files_list):
    index, freq_word = create_inverse_index(files_list)

    sum_freq = 0
    index_list = []
    print(words_list_stemmed)
    for term in words_list_stemmed:
        if term in index.keys():
            print("Term is " + str(term))
            print("Index term " + str(index[term]))
            index_list.append(index[term])
            sum_freq = sum_freq + freq_word[term]

    print("Index list " + str(index_list))

    if sum_freq:
        index_result = list(set.intersection(*index_list))
        print("Index result is " + str(index_result))
        return index_result, sum_freq
    else:
        return ["No results found"], 0


def parse_input(word):
    word = word.strip()
    if ',' in word:
        words_list = word.split(',')
    elif ' ' in word:
        words_list = word.split(' ')
    elif ';' in word:
        words_list = word.split(';')
    elif ':' in word:
        words_list = word.split(':')
    else:
        words_list = [word]

    return words_list


def stemming(word):
    # word = PorterStemmer().stem_word(word.lower())
    return word


def create_inverse_index(files_list):
    # creating a dictionary of words
    index = dict()

    # creating frequency of the words
    freq_word = dict()

    # reading multiple files and tokenizing the contents of the files
    for f in files_list:
        file_content = open(f).read()
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(file_content)
        # creating inverted index data structure
        for word in words:
            # keeping all the words in lower case
            word = stemming(word)
            if word not in index.keys():
                index[word] = [f]
            else:
                index[word].append(f)

    for word in index.keys():
        freq_word[word] = len(index[word])
        index[word] = set(index[word])

    return index, freq_word


def search(term, files_list):
    words_list = parse_input(term)
    print("WOrds list is " + str(words_list))
    words_list_stemmed = [stemming(word.strip()) for word in words_list]
    index_result, sum_freq = combine_indexes(words_list_stemmed, files_list)
    return index_result, sum_freq


# if __name__ == '__main__':
#     files_list = ['adventur.txt', 'apples.txt', 'hVDacrN0.html']
#     search('html', files_list)

MAXIMUM_ALLOWED_FILES = 6


class SecondFrame(wx.Frame):
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Here is what we found", size=(700, 300))
        self.panel = wx.Panel(self)
        # results list
        self.files_result = []
        # SIZER
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)
        self.sizer = wx.GridBagSizer(0, 0)
        # Results label
        self.files_location_label = wx.StaticText(self.panel, -1, "Output of Results:", (10, 1))
        self.sizer.Add(self.files_location_label, (10, 10))

    def get_results_from_search(self, files_with_word, freq):
        self.word_occ_label = wx.StaticText(self.panel, -1, str(freq) + " occurences", (10, 20))
        self.sizer.Add(self.word_occ_label, (10, 25))
        for i, files in enumerate(files_with_word):
            self.files_result.append(wx.StaticText(self.panel, -1, files, (10, 20 + (i + 1) * 20)))
            self.sizer.Add(self.files_result[-1], (10, 20 + (i + 1) * 20))


class gui(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Information Retrieval System [XIA Yuchen]', size=(700, 500))
        self._defaultDirectory = "/home"
        self.panel = wx.ScrolledWindow(self, wx.ID_ANY)

        # SIZER
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)
        self.sizer = wx.GridBagSizer(0, 0)

        # List of files and no of it
        self.no_of_files = 1
        self.fileCtrl = []

        # search
        self.search_label = wx.StaticText(self.panel, -1, "Search Words: ", (100, 35))
        self.sizer.Add(self.search_label, (100, 35))
        self.search_name = wx.TextCtrl(self.panel, pos=(100, 66), size=(260, -1))
        self.sizer.Add(self.search_name, (200, 30))

        # Files location
        self.files_location_label = wx.StaticText(self.panel, -1, "Add documnet index:", (100, 160))

        # Adding file button
        self.button = wx.Button(self.panel, label="Add Files", pos=(380, 200), size=(110, -1))
        self.sizer.Add(self.button, (100, 150))
        self.Bind(wx.EVT_BUTTON, self.add_files_button, self.button)

        self.fileCtrl.append(wx.FilePickerCtrl(self.panel, pos=(100, 200), size=(260, -1)))
        self.sizer.Add(self.fileCtrl[0], (100, 200))

        # Removing file button
        self.button_remove = wx.Button(self.panel, label="Remove Files", pos=(510, 200), size=(110, -1))
        self.Bind(wx.EVT_BUTTON, self.remove_files_button, self.button_remove)
        self.sizer.Add(self.button_remove, (100, 445))

        # running the program button
        self.button_run = wx.Button(self.panel, label="Search", pos=(380, 63), size=(110, -1))
        self.Bind(wx.EVT_BUTTON, self.run_program, self.button_run)
        self.sizer.Add(self.button_run, (500, 500))

    def add_files_button(self, event):
        if self.no_of_files <= MAXIMUM_ALLOWED_FILES:
            height = self.no_of_files * 35 + 200
            self.fileCtrl.append(wx.FilePickerCtrl(self.panel, pos=(100, height), size=(260, -1)))
            self.sizer.Add(self.fileCtrl[self.no_of_files], (100, height))
            self.no_of_files = self.no_of_files + 1

    def remove_files_button(self, event):
        self.sizer.Detach(self.fileCtrl[-1])
        self.fileCtrl[-1].Destroy()
        del self.fileCtrl[-1]
        self.no_of_files = self.no_of_files - 1

    def run_program(self, event):
        frame = SecondFrame()
        keyword = self.search_name.GetValue()

        if not keyword:
            box = wx.MessageDialog(None, 'Search Term Not Mentioned', 'Ivalid Request', wx.OK)
            answer = box.ShowModal()
            box.Destroy()

        # getting files list from the file dialog
        files_list = []
        for file_path in self.fileCtrl:
            files_list.append(file_path.GetPath())
        files_list = filter(None, files_list)
        print(files_list)

        # sending the data to main.py
        if files_list:
            files_with_word, freq = search(keyword, files_list)
            frame.get_results_from_search(files_with_word, freq)
            frame.Show()
        else:
            box = wx.MessageDialog(None, 'Files not mentioned', 'Invalid Request', wx.OK)
            answer = box.ShowModal()
            box.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = gui(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
