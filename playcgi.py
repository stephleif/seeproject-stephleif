import cgi

def processInput(numStr1, numStr2):
    '''
      Process input parameters and return the final page as a string.
      Keyword Arguments
      (str) numStr1
      (str) numStr2
    '''
    num1 = int(numStr1)
    num2 = int(numStr2)
    total = num1+num2
    return fileToStr('additionTemplate.html').format(**locals())


def main():
    form = cgi.FieldStorage()
    numStr1 = form.getfirst("x", "0")
    numStr2 = form.getfirst("y",0)
    contents = processInput(numStr1, numStr2)
    print(contents)