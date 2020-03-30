import numpy as np
from colorama import Fore, Style

def red_text(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

class Ruler: 

    """ 
    Ruler class allows us to create the different tools necessary to finally return the distance
    between two strings, and represent the differences in a relevant way.
    
    """

    #We want to be able to give an indel cost and distance between two character that would 
    # be different from 1. We want to be able to give the distances in a matrix.
    def __init__(self, a: str, b: str, indel = 1, *arg_distances_matrix):

        #a and b should be the strings to compare.
        #indel is the cost for insertion / deletion.
        #arg_distances_matrix should be a couple, made of a matrix of distances between characters,
        #and a list of these characters in the corresponding order.

        self.b = b
        self.a = a
        self.indel = indel
        if len(arg_distances_matrix) > 0:
            self.distances_matrix = arg_distances_matrix[0]
            
            #We also create a dictionnary to remember where each character is situated.
            dict_alphabet = {}
            for i, char in enumerate(arg_distances_matrix[1]):
                dict_alphabet[char] = i
            self.dict_alphabet = dict_alphabet

        #If no distances_matrix is defined, we create one by default, where distances are 1 
        # between two different characters, and 0 between same characters. The distances_matrix
        # is adapted to the characters present in the two strings, with a default distance of 1. 
        else:
            alphabet = set([char for char in a] + [char for char in b])
            dict_alphabet = {}                              
            for i, char in enumerate(alphabet):
                dict_alphabet[char] = i
            self.dict_alphabet = dict_alphabet
            c = len(alphabet)
            self.distances_matrix = np.ones((c, c)) - np.eye(c, c)


    def compute(self):

        """
        Compute method builds two matrixes in a recursive way:
        a 'grid' matrix contains in each element, the shortest distance possible to compare two 
        characters of the a string, represented by the first column, and the b string, 
        represented by the first line.
        The first line and column are filled with the cost corresponding to indel added
        as many times as the element's index in the line or column respectively, corresponding to
        "up" and "left" in the decode matrix (see below).
        Then each element is filled with the minimun of the up, left or diag-up-left value added to
        the indel cost or the distance between the corresponding letters.

        'decode' is a numpy matrix filled with numbers, remembering the way followed,
         with "up" == 1, "left" == 2, "diag" == 3 designating the previous element of grid.
        
        """
        # We first initialise grid and decode :
        a_len, b_len = len(self.a), len(self.b)
        grid = np.zeros((a_len + 1, b_len + 1))
        decode = np.zeros((a_len + 1, b_len + 1))
        for i in range(a_len + 1):
            grid[i][0] =  i * self.indel
            decode[i][0] = 1
        for j in range(b_len + 1): 
            grid[0][j] =  j * self.indel
            decode[0][j] = 2

        #Now we can fill the rest.
        for i in range(1, a_len + 1):
            for j in range(1, b_len + 1):

                #We get the distance between the two characters considered,
                #thanks to dict_alphabet and distances_matrix
                x = self.dict_alphabet[self.a[i - 1]]
                y = self.dict_alphabet[self.b[j - 1]]
                current_distance = self.distances_matrix[x][y]
                up = grid[i - 1][j] + self.indel
                left = grid[i][j - 1] + self.indel
                diag = grid[i - 1][j - 1] + current_distance
                grid[i][j] = min(up, left, diag)
                if grid[i][j] == up:
                    decode[i][j] = 1
                elif grid[i][j] == left:
                    decode[i][j] = 2
                else :
                    decode[i][j] = 3
        
        #We now only need to remember decode, in order to prompt the two strings compared,
        #and distance, which interested us in the first place.
        self.decode = decode
        self.distance = grid[a_len][b_len]

    def __repr__(self):

        """
        __repr__ is the simplest way to use the Ruler class: it allows to print the distance
        between the strings.
        
        """

        return(self.distance)

    def report(self):

        """
        The report method builds two strings from the two previou a and b:
        the characters are redened when there are changes, and offsets are 
        symbolised by '-'.

        """

        alignement_a = str()
        alignement_b = str()
        a, b = self.a, self.b
        a_len, b_len = len(a), len(b)

        #We follow the 'way' indicated by the decode matrix, 
        #starting from self.decode[len(a)][len(b)].
        #We add '-' (indel) in the builded strings if a 'up' or 'left' is found,
        #we add the corresponding letters of a and b if a 'diag' is found.
        while (a_len > 0 or b_len > 0) :    
            if self.decode[a_len][b_len] == 3:           #Here the path taken was 'diag'.
                letter_a = a[a_len - 1]
                letter_b = b[b_len - 1]

                #we want to check if the letters have to be redened.
                i = self.dict_alphabet[self.a[a_len - 1]]
                j = self.dict_alphabet[self.b[b_len - 1]]
                if self.distances_matrix[i][j] != 0:

                    #Here we reden the characters, as there was a distance different from 0.
                    letter_a = f"{red_text(letter_a)}"  
                    letter_b = f"{red_text(letter_b)}"


                alignement_a = letter_a + alignement_a
                alignement_b = letter_b + alignement_b
                a_len = a_len - 1
                b_len = b_len - 1

            elif self.decode[a_len][b_len] == 1:          #Here the path taken was 'up'.
                alignement_a = red_text(a[a_len - 1]) + alignement_b 
                alignement_b = red_text("-") + alignement_b
                a_len = a_len - 1

            else:                                         #Here the path taken was 'left'.
                alignement_a= red_text("-") + alignement_a
                alignement_b = red_text(b[b_len - 1]) + alignement_b
                b_len = b_len - 1

        #It may occur that we arrive on the first line or column. From that point, 
        #only one direction is possible.
        while a_len > 0:
            alignement_a = a[a_len - 1] + alignement_a
            alignement_b = red_text("-") + alignement_b
            a_len = a_len - 1

        while b_len > 0:
            alignement_a = red_text("-") + alignement_a
            alignement_a = red_text(b[b_len - 1]) + alignement_b
            b_len = b_len - 1

        return(alignement_a, alignement_b)

        
ruler = Ruler("vertueux", "tueurs")
ruler.compute()
print(ruler.distance)
top, bottom = ruler.report()
print (top)
print(bottom)
