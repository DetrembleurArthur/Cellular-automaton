import pygame, pygame.mixer
from pygame.locals import*

fenetre_largeur = 1400
fenetre_hauteur = 800
fenetre_dimension = (fenetre_largeur, fenetre_hauteur)

DIMCASE = 8
casesLigneH = fenetre_largeur//DIMCASE
casesLigneV = fenetre_hauteur//DIMCASE

HAUT = 1
DROITE = 2
BAS = 3
GAUCHE = 4

GRIS = (150,150,150)
NOIR = (0,0,0)
BLANC = (255,255,255)

fenetre = pygame.display.set_mode(fenetre_dimension)

def affiche_grille(grille):
	Color = (0,0,0)
	if grille:
		Color = BLANC
	else:
		Color = GRIS
	for i in range(0, fenetre_largeur+1, 1):
		if i%DIMCASE == 0:
			pygame.draw.line(fenetre, Color, (i,0), (i,fenetre_hauteur), 1)
		
	for i in range(0, fenetre_hauteur+1, 1):
		if i%DIMCASE == 0:
			pygame.draw.line(fenetre, Color, (0,i), (fenetre_largeur,i), 1)


class Env:

	def __init__(self):

		self.gen = 0
		self.case = []
		self.orientation = HAUT
		self.fourmi = [casesLigneV//2, casesLigneH//2]
		for i in range(casesLigneV):
			self.case.append([0]*casesLigneH)

	def out_of_band(self):

		if self.fourmi[0] >= casesLigneV or self.fourmi[1] >= casesLigneH:
			return "STOP"
		else:
			return "CONTINUE"

	def incr_orientation(self, direction):

		if direction == "droite":
			self.orientation += 1
			if self.orientation > 4:
				self.orientation = 1
		elif direction == "gauche":
			self.orientation -= 1
			if self.orientation < 1:
				self.orientation = 4

	def deplace_fourmi(self):

		if self.orientation == HAUT:
			self.fourmi[0] -= 1
		elif self.orientation == BAS:
			self.fourmi[0] += 1 
		elif self.orientation == DROITE:
			self.fourmi[1] += 1
		elif self.orientation == GAUCHE:
			self.fourmi[1] -= 1

	def gen_plus_plus(self):

		self.gen += 1

	def operation(self):

		if self.out_of_band() == "STOP":
			return "STOP"
		if self.case[self.fourmi[0]][self.fourmi[1]] == 0:
			self.incr_orientation("droite")
			self.case[self.fourmi[0]][self.fourmi[1]] = 1
			pygame.draw.rect(fenetre,NOIR, (self.fourmi[1]*DIMCASE,self.fourmi[0]*DIMCASE,DIMCASE,DIMCASE))
			self.deplace_fourmi()
		else:
			self.incr_orientation("gauche")
			self.case[self.fourmi[0]][self.fourmi[1]] = 0
			pygame.draw.rect(fenetre,BLANC,(self.fourmi[1]*DIMCASE,self.fourmi[0]*DIMCASE,DIMCASE,DIMCASE))
			self.deplace_fourmi()
		self.gen_plus_plus()
		pygame.display.set_caption("Fourmi de Langton  gen:  " + str(self.gen))

		return "CONTINUE"

env = Env()

fenetre.fill(BLANC)

pygame.init()


fini = False
temps = pygame.time.Clock()


pygame.display.set_caption("Fourmi de Langton")

#images:

end = 0
grille = True
while not fini:
	

	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			fini = True
		if event.type == KEYUP:
			if event.key == K_q:
				fini = True
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				if grille == False:
					grille = True
				else:
					grille = False
			

	

	temps.tick(60)

	affiche_grille(grille)
	if env.operation() == "STOP" and end == 0:
		end = 1
		print("autoroute créée\nfin du programme")
	
	pygame.display.flip()