class Node():  # a node have a size of 27 , each for an alphabet and $
    def __init__(self, size=27):
        self.data = []  # a list to store data, at the "$" of each word
        self.child = [None] * size
        self.occur = 0


class Trie():
    def __init__(self):
        self.root = Node()

    def insert_rec(self, word, data, mode=None):
        current = self.root
        if mode is None:
            self.insert_aux_better(current, word, data)
        elif mode == "p":
            self.insert_palindrome(current,word,data)

    def insert_aux_better(self, current, word, data, i=0):
        if len(word) == i:  # reaches the end of the word
            if current.child[26] is None:  # if the '$' is not already added
                current.child[26] = Node()  # add a node to indicate ending '$'
            if data not in current.child[26].data:  # if data not saved
                current.child[26].data.append(data)  # saved the data in the ending node
                current.child[26].occur += 1  # adding 1 to indicate that it exist in one more song
            return current.child[26].occur

        else:
            index = ord(word[i]) - 97  # get the index for character
            if current.child[index] is None:  # if the alphabet never added
                current.child[index] = Node()  # add a new node

            i += 1

            x = self.insert_aux_better(current.child[index], word, data, i)
            if x > current.child[index].occur:  # only update if it is larger
                current.child[index].occur = x  # update the occurrence when recurse
            return x


    def search(self, word, mode):
        current = self.root
        for char in word:
            index = ord(char) - 97
            if current.child[index] is None:  # the alphabet does not exist
                return "Not Found"
            current = current.child[index]  # if it is found we traverse deeper

        if mode == "whole":  # if the mode is to find the whole word
            if current.child[26] is None:  # there is no such word, as a "$" is not found
                return "Not Found"
            else:
                return current.child[26].data  # return the data retrieved

        elif mode == "prefix":  # if the mode is to find by prefix
            retVal = word
            most = current.occur
            # find the first one with the same occur. then traverse to the end to get the whole word.
            i = 0
            # if prefix is found, there MUST be a complete word for it.
            while i <= 25:  # it will automatically stopped when only '$' is found
                if current.child[i] is not None:
                    if current.child[i].occur == most:  # first node with same occurrence
                        retVal += chr(i + 97)
                        current = current.child[i]
                        i = -1  # restart the loop
                i += 1
            return retVal

    def insert_palindrome(self, current, word, start):
        if len(word) == start:  # if end is reached, add new Node to indicate '$'
            if current.child[26] is None:
                current.child[26] = Node()
            return
        else:  # if its not the end of the word, traverse more
            index = ord(word[start]) - 97
            if current.child[index] is None:
                current.child[index] = Node()
            current.child[index].data.append(start)
            start += 1
            return self.insert_palindrome(current.child[index],word,start)

    def search_palindrome(self, word, ending):
        current = self.root
        result = []  # the index of character from word that a matching character from trie is found
        compare = [0]*ending

        # start checking from the back of word with trie
        for i in range(ending-1, -1, -1):  # time complexity N where N is the length of word
            index = ord(word[i])-97
            if current.child[index] is not None:
                result.append(i)  # found a match char
                compare[i] = current.child[index].data
                current = current.child[index]  # traverse to the next node
            else:  # if a matching char is not found
                break
        retVal = []  # the palindromic substring found in this search
        # only loop until the second last, as need length of >= 2
        for i in range(len(compare)-len(result),len(compare)-1):
            if result[0] in compare[i]:  # find the the ending point
                # the index of end point of word in compare list is the starting point of the palindrome
                retVal.append((i,result[0]))

        if len(retVal) > 0:  # only return when palindromic substring is found
            return retVal


def lookup(data_file, query_file):
    file_data = open(data_file,"r")
    file_find = open(query_file,"r")
    new_file = open("song_ids.txt","w")
    my_trie = Trie()

    for line in file_data:
        line = line.strip("\n")
        line = line.split(":")  # split line into [id,strings]
        id = line[0]  # the id of each word
        words = line[1].split(" ")  # split the strings into [string,string,...]
        for word in words:
            my_trie.insert_rec(word,id)

    for line in file_find:
        line = line.strip("\n")
        result = my_trie.search(line,"whole")
        if result != "Not Found":
            result = " ".join(result)+"\n"
        new_file.writelines(result)


def most_common(data_file,query_file):
    file_data = open(data_file,"r")
    file_find = open(query_file,"r")
    new_file = open("most_common_lyrics.txt","w")
    my_trie = Trie()
    for line in file_data:
        line = line.strip("\n")
        line = line.split(":")  # split line into [id,strings]
        id = line[0]  # the id of each word
        words = line[1].split(" ")  # split the strings into [string,string,...]
        for word in words:
            my_trie.insert_rec(word,id)
    for word in file_find:
        word = word.strip("\n")
        result = my_trie.search(word,"prefix")
        if result != "Not Found":
            result += "\n"
        new_file.write(result)


def palindromic_substrings(S):
    suffix_trie = Trie()
    palindrome = []
    for i in range(len(S)):
        suffix_trie.insert_rec(S,i,"p")
    for i in range(len(S),0,-1):  # time complexity : N ,where N is length of S
        result = suffix_trie.search_palindrome(S,i)
        if result is not None:
            palindrome += result
    if len(palindrome) == 0:
        return "Not palindromic!"
    return palindrome


if __name__ == "__main__":
    lookup("example_songs.txt", "example_queries_1.txt")
    most_common("example_songs.txt", "example_queries_2.txt")
    palindromic_substrings("ababcbaxx")

