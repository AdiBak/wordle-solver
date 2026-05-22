class WordleDB:
    def __init__(self, filename):
        self.words = self.load_words(filename)
    
    def load_words(self, filename):
        words = []

        with open(filename, "r") as file:
            for line in file:
                word = line.strip().lower()

                if word.isalpha() and len(word) == 5:
                    words.append(word)
                
        return words


    def get_words(self):
        return self.words
