#First of all, we create a function giving the occurency of each character.
#To do so, we must have an inventory of those characters.

def inventory_characters(text): 
    inventory = []
    for x in text:
        if not x in inventory:
            inventory.append(x)
    return inventory
        
def frequency_characters(text):
    inventory = inventory_characters(text)
    frequency = {}
    for a in inventory:
        frequency[a] = 0
    for a in text:
       frequency[a] = frequency[a] + 1
    return frequency

    
#We will also need a sorting method. I chose simple one. I could have chose a more efficient one.
def order_by_frequency(list_leaves: list):

    """

    Returns a list of leaves ordered by decreasing value of sum_frequency.

    """

    for i in range(len(list_leaves)):
        for j in range(i + 1, len(list_leaves)):
            if list_leaves[j].sum_frequency > list_leaves[i].sum_frequency :
                list_leaves[j], list_leaves[i] = list_leaves[i], list_leaves[j] 
    return (list_leaves)
    

#We create a class Leaf : it allows us create the nodes of the tree. 

class Leaf():

    """
    A class that creates the nodes of the trees.
    
    """

    def __init__(self, sum_frequency, character: str, *family ):

        self.sum_frequency =sum_frequency
        self.character = character

        #We create the attributes left_son, right_son. These links allow us to build the tree.
        #I no family argument is given, we do nothing.
        if len(family) > 0:
            self.left_son = family[0]
            self.right_son = family[1]

        #We create an attribute that indicates if the leaf is the root of the tree.
        #Samely, bottom indicates if the leaf is terminal.
        self.top = False
        self.bottom = True 

    #We can redefine add, in order to concatenate the characters of the node,
    #and add each 'frequency'.
    def __add__ (self, right):
        new_frequency = self.sum_frequency + right.sum_frequency
        new_character = self.character + right.character
        return (Leaf(new_frequency, new_character, self, right))


#We are now able to build the TreeBuilder class.
class TreeBuilder():

    """TreeBuild is a classe able to build binary trees."""

    def __init__(self, text: str):
        self.text = text

        #This will allow to initiate the construction of the tree
        self.frequency_characters = frequency_characters(text) 
        self.inventory_characters = inventory_characters(text) 

    def tree(self):

        """
        This method allows us to build a tree from the terminal leaves, 
        whose frequency is given by self.frequency_characters.
        In order to code and decode, we don't really need a variable to represent it.
        Only to build the links between the leaves is necessary.
        
        self.tree() returns a couple constituted by a dictionary associating 
        each terminal character to its code, and the top leaf, or root
        
        """
        
        #We initiate the tree
        list_terminal_leaves = []
        for a in self.frequency_characters:
            list_terminal_leaves.append(Leaf(self.frequency_characters[a], a))

        #We create a copy, with wich we can work.
        working_list = list_terminal_leaves[:]

        #We build the tree.
        while len(working_list) > 1:

            #We merge the leaves with the smallest frequencies, until the root is reached.
            working_list = order_by_frequency(working_list)
            right = working_list.pop()
            left = working_list.pop()
            new_leaf = left + right
            new_leaf.bottom = False   #We indicate that the newly built leaf is not a terminal one.
            left.parent = new_leaf
            right.parent = new_leaf
            working_list.append(new_leaf)

        root = working_list[0]
        root.top = True #We indicate that this last leaf is the root.
        
        #a dictionary dict_char associates each terminal character to its code
        dict_char = {}
        for leaf in list_terminal_leaves:
            
            #we build the code by climbing up, testing if we come from the right or the left
            #at each leaf.
            code = ''
            current_leaf = leaf
            while not current_leaf.top:
                
                if current_leaf.character == current_leaf.parent.left_son.character :
                    code = code + '0'
                else:
                    code = code + '1'
                current_leaf = current_leaf.parent

            #We don't forget to reverse the code, anticipating the decoding process.
            dict_char[leaf.character] = code[::-1] 
            
        return(dict_char, root) 


class Codec():

    """
    Codec allows to decode and code any text, thanks to an already built binary tree.
    
    """

    def __init__(self, binary_tree):
        self.binary_tree = binary_tree
    
    def encode(self, text: str):
        
        """
        encode returns the code made of 0 and 1 from the text given.

        """

        encoding = ''

        #We concatenate the code of each letter of the text
        for a in text:
            encoding = encoding + self.binary_tree[0][a] 
        return encoding
    
    def decode(self, code: str):

        """
        decode returns the decoded text.
        
        """

        decoding = ''
        current_character_index = 0 #to memorize the characters already processed
        while current_character_index < len(code) - 1:
            current_leaf = self.binary_tree[1] #we start from the root
            
            #we climb the tree down following the 0 or 1 of the code, 
            #until we arrive at a terminal leaf
            while not current_leaf.bottom:     
                if code[current_character_index] == '0':
                    current_leaf = current_leaf.left_son
                elif code[current_character_index] == '1':
                    current_leaf = current_leaf.right_son
                current_character_index += 1

            #the terminal leaf gives us the character to add to decoding    
            decoding = decoding + current_leaf.character 
         
        return (decoding)
            


text = "a dead dad ceded a bad babe a beaded abaca bed"
builder = TreeBuilder(text)
binary_tree = builder.tree()

codec = Codec(binary_tree)
encoded = codec.encode(text)
decoded = codec.decode(encoded)
print(encoded)
print(f"{text}   is the text \n{encoded}")
print(f"{decoded} is the decoded text")


if decoded != text:
    print("OOPS")

