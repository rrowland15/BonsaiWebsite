import random
import string

def generateurl():
    mystr = []
    for _ in range(5):
        mystr.append(str(random.randint(0,1000)))
        mystr.append(random.choice(string.ascii_letters))

    return "".join(mystr)
    
