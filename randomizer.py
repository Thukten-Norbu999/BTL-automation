import random

def create_new():
    id = ""
    for i in range(11):
        id+= str(random.randint(0,9))

    return id

