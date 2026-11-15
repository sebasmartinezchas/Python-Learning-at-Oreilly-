words='this is a bunch of words to practice the lambas functions in a reuven course'
words_list=words.split()        
print(words_list)

    # Sort this list by the number of letters a-j in each word  
print(sorted(words_list,key=lambda text: sum(1 for char in text if char.lower() in 'abcdefghijklmnopqrstuvwxyz')))

