import generators as ge

def question(n):
    print(f'{n}. ' + ge.QHA[f'q{n}'])

def hint(n):
    print(ge.QHA[f'h{n}'])

def answer(n):
    print(ge.QHA[f'a{n}'])