import pygame, pygame.mixer
from pygame.locals import*
import math


fenetre_hauteur = 700
fenetre_largeur = fenetre_hauteur*2

fenetre_dimension = (fenetre_largeur, fenetre_hauteur)

DIMCASE = 1
casesLigneH = fenetre_largeur//DIMCASE
casesLigneV = fenetre_hauteur//DIMCASE

HAUT = 1
DROITE = 2
BAS = 3
GAUCHE = 4

GRIS = (150,150,150)
NOIR = [0,0,0]
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

		self.curLine = 1
		self.gen = 0
		self.case = []
		for i in range(casesLigneV):
			self.case.append([0]*casesLigneH)
		self.case[0][casesLigneH//2] = 1
		for i in range(0,casesLigneH,1):
			if self.case[0][i] == 1:
				pygame.draw.rect(fenetre,NOIR,(i*DIMCASE,0*DIMCASE,DIMCASE,DIMCASE))

		

	def out_of_band(self, x):

		if x < 0 or x >= casesLigneH:
			return True
		return False

	def check_up(self, cn):

		if self.out_of_band(cn+1) == False and self.out_of_band(cn-1) == False:
			if self.case[self.curLine-1][cn-1] == 1 and self.case[self.curLine-1][cn] == 1 and self.case[self.curLine-1][cn+1] == 1:
				return False
		if self.out_of_band(cn+1) == False and self.out_of_band(cn+1) == False:
			if self.case[self.curLine-1][cn-1] == 0 and self.case[self.curLine-1][cn] == 0 and self.case[self.curLine-1][cn+1] == 0:
				return False
		if self.out_of_band(cn+1) == True:
			if self.case[self.curLine-1][cn] == 0 and self.case[self.curLine-1][cn-1] == 0:
				return False
		if self.out_of_band(cn-1) == True:
			if self.case[self.curLine-1][cn] == 0 and self.case[self.curLine-1][cn+1] == 0:
				return False
		if self.out_of_band(cn+1) == True:
			if self.case[self.curLine-1][cn] == 1 and self.case[self.curLine-1][cn-1] == 1:
				return False
		if self.out_of_band(cn-1) == True:
			if self.case[self.curLine-1][cn] == 1 and self.case[self.curLine-1][cn+1] == 1:
				return False
		return True



	def generation(self, cn):

		self.case[self.curLine][cn] = 1
		pygame.draw.rect(fenetre,NOIR,(cn*DIMCASE,self.curLine*DIMCASE,DIMCASE,DIMCASE))

	def operation(self):

		if self.curLine >=  casesLigneV:
			return "STOP"
		for i in range(0,casesLigneH,1):
			if self.check_up(i):
				self.generation(i)

		self.gen += 1
		self.curLine += 1
		pygame.display.set_caption("Triangles de Sierpinsky ")

		return "CONTINUE"




fenetre.fill(BLANC)

pygame.init()
env = Env()

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

	#affiche_grille(grille)
	if env.operation() == "STOP" and end == 0:
		end = 1
		print("Triangle créé\nfin du programme")
	
	pygame.display.flip()