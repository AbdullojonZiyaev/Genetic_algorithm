"""
use python 3.11.4
"""

def counter(string):
    counter_1,counter_2 = 0, 0
    for c in string:
        if c == "[":
            counter_1 += 1
        elif c == "]":
            counter_2 += 1
        else:
            pass
    print(counter_1,counter_2, counter_1 == counter_2, len(string))
def main():
    counter("++[.-,>+<++-<.[+<-<-<.[]<][+.>,.,>[<].>.>+>][<[[,.,<[--<],-]-]<[.>]+.>->-+.]++><>++-.<,,>[].[]]")
main()