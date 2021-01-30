import random
myval = random.randint(0,0)
print(myval)

def crazy():
    return

val = crazy()
print(val)
print('Start')

def func1():
    print('func1')
    return 'func1_value'

def func2(var1):
    print('func2')
    print(var1)
    print(func1())

func1()
func2('hello')
print('End')