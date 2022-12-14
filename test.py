class hello:

    def __init__(self,a='Welcome to '):
        self.a = a

    def welcome(self, x):
        print(self.a +x)

h= hello()
h.welcome('Turing')            
