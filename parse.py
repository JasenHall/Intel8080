def parse(line):
    words = []
    index=0
    string_on = False
    count = len(line)
    while index < count:
        print(index,line)
        if line[index] == "'":
            string_on = not string_on
        if line[index] == " " and string_on is False: # word break
            words.append(line[:index])
            line = line[index+1:]
            count = len(line) # update count after modifying line
            index=-1 # reset index to start again
        index+=1
    words.append(line) # add the last word
    print(words)



if __name__ == "__main__":
    line = input("Enter a line: ")
    parse(line)