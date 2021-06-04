import math

# Set hand-picked number X_NUM
X_NUM = 15

# Set number of objects
NUM_OBJS = 64

# Array with numbers
arr = [0]*NUM_OBJS
for i in range(NUM_OBJS):
    arr[i] = i + 1

# Algorithm of searching hand-picked number X_NUM
steps = int(1 + math.log(NUM_OBJS, 2))
print("Maximum number of steps: " + str(steps) + "\n")

guess_num = 0
print("Source array: " + str(arr) + "\n")

while (guess_num != X_NUM):
    guess_num = arr[int(len(arr)/2)]
    print("Is " + str(guess_num) + "?")
    if guess_num > X_NUM:
        print("It's so much")
        arr = arr[0:int(len(arr)/2)]
        print("Array now (shorten): "+str(arr)+"\n")
    elif guess_num == X_NUM:
        print("Yep!")
        print("Array: "+str(arr)+"\n")
    else:
        print("It's so little")
        arr = arr[int(len(arr)/2):len(arr)]
        print("Array now (shorten): "+str(arr)+"\n")