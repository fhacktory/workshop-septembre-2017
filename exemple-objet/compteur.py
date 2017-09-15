class Compteur:

    def __init__(self, style):
        self.setType(style)
        self.nombre = 0
        self.romain = {0: '', 1: 'I', 2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI', 7:'VII', 8:'IIV', 9:'IV', 10:'X'}
        self.morse = {0: '-----', 1: '*----', 2:'**---', 3:'***--', 4: '****-', 5:'*****', 6:'-****', 7:'--***', 8:'---**', 9:'----*', 10: '----- *-----'}
         

    def raz(self):
        self.nombre = 0

    def increment(self):
        if self.nombre < 9:
            self.nombre += 1

    def setType(self, style):
        if style in ['arabe', 'romain', 'morse']:
            self.style = style
        else:
            print("Le type n'est pas bon. Choix : 'arabe', 'romain', 'morse'")
            
    def afficher(self):
        if self.style == 'arabe':
            print(self.nombre)
        elif self.style == 'romain':
            print(self.romain[self.nombre])
        elif self.style == 'morse':
            print(self.morse[self.nombre])
