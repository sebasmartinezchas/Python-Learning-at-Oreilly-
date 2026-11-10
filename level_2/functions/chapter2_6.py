import time
# Chose List, Dicts, or Sets in Python | Comparing Lists, Dictionaries, and Sets
my_words=[elt.strip() for elt in open('sonnet_words.txt','r').readlines()]
word_list=[elt.strip() for elt in open('sowpods.txr','r').readlines()]
# Fast way | La forma real y sin trampa sería con set word_set= Set(my_words) y cambiar el iterador
word_dict=dict((elt,1) for elt in word_list)

counter=0
start=time.time()
for word in my_words:
    if word not in word_list:
        print(word)
        counter +=1

stop=time.time()
print("Total new words: %d" % counter)
print("Time elapsed: %.1f seconds" % (stop- start))
