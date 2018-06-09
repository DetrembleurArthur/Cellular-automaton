import pygame
from pygame.locals import*
import os


fenetre_largeur = 1400
fenetre_hauteur = 800
fenetre_dimension = (fenetre_largeur, fenetre_hauteur)
fenetre = pygame.display.set_mode(fenetre_dimension)

GRIS = (150,150,150)
NOIR = (0,0,0)
BLANC = (255,255,255)

DIMCASE = 8

casesLigneH = fenetre_largeur//DIMCASE
casesLigneV = fenetre_hauteur//DIMCASE

pygame.font.init()
police = pygame.font.Font('Montel.ttf', 25)

txtEdit = "MODE EDITION"
txtSouris = "boutons de souris: de/placer une cellule"
txtC = "< c >: copier la configuration"
txtV = "< v >: coller la configuration"
txtG = "< g >: lancer la simulation"
txtSim = "MODE SIMULATION"
txtR = "< r >: lancer le mode edition (grille reinitialisee)"
txtS = "< s >: lancer le mode edition avec la configuration obtenue"
txtP = "< p >: afficher/effacer la grille"
txtQ = "< q >: quitter le programme"
txtK = "< k >: enregistrer votre configuration/specimen"

marquoirEdit = police.render(txtEdit, True, (0,0,200))
marquoirSouris = police.render(txtSouris, True, (0,0,200))
marquoirC = police.render(txtC, True, (0,0,200))
marquoirV = police.render(txtV, True, (0,0,200))
marquoirG = police.render(txtG, True, (0,0,200))
marquoirSim = police.render(txtSim, True, (0,0,200))
marquoirR = police.render(txtR, True, (0,0,200))
marquoirS = police.render(txtS, True, (0,0,200))
marquoirP = police.render(txtP, True, (0,0,200))
marquoirQ = police.render(txtQ, True, (0,0,200))
marquoirK = police.render(txtK, True, (0,0,200))

def affiche_grille():

	for i in range(0, fenetre_largeur+1, 1):
		if i%DIMCASE == 0:
			pygame.draw.line(fenetre, GRIS, (i,0), (i,fenetre_hauteur), 1)
		
	for i in range(0, fenetre_hauteur+1, 1):
		if i%DIMCASE == 0:
			pygame.draw.line(fenetre, GRIS, (0,i), (fenetre_largeur,i), 1)


def affiche_controles():
	
	fenetre.fill(BLANC)
	fenetre.blit(marquoirEdit, (fenetre_largeur/2-350, 100))
	fenetre.blit(marquoirSouris, (fenetre_largeur/2-350, 150))
	fenetre.blit(marquoirC, (fenetre_largeur/2-350, 200))
	fenetre.blit(marquoirV, (fenetre_largeur/2-350, 250))
	fenetre.blit(marquoirG, (fenetre_largeur/2-350, 300))
	fenetre.blit(marquoirK, (fenetre_largeur/2-350, 350))
	fenetre.blit(marquoirSim, (fenetre_largeur/2-350, 400))
	fenetre.blit(marquoirR, (fenetre_largeur/2-350, 450))
	fenetre.blit(marquoirS, (fenetre_largeur/2-350, 500))
	fenetre.blit(marquoirP, (fenetre_largeur/2-350, 550))
	fenetre.blit(marquoirQ, (fenetre_largeur/2-350, 600))

class Cursor:

	color = (0,150,0)
	oldPos = [0,0]

	def __init__(self):

		pass


	def place_curseur(self, x, y, env):

		if env.caseAvant[y][x] == 1:
			return False
		self.oldPos = [x, y]
		pygame.draw.rect(fenetre,self.color,(x*DIMCASE,y*DIMCASE,DIMCASE,DIMCASE))

	def enleve_curseur(self, env):

		if self.oldPos[0] < 0 or self.oldPos[1] < 0 or self.oldPos[0] >= casesLigneH or self.oldPos[1] >= casesLigneV:
			return False
		if env.caseAvant[self.oldPos[1]][self.oldPos[0]] == 1:
			pygame.draw.rect(fenetre,NOIR,(self.oldPos[0]*DIMCASE,self.oldPos[1]*DIMCASE,DIMCASE,DIMCASE))
		else:
			pygame.draw.rect(fenetre,BLANC,(self.oldPos[0]*DIMCASE,self.oldPos[1]*DIMCASE,DIMCASE,DIMCASE))


class Cell:
	
	pos = [-1,-1]
	dim = DIMCASE

	def __init__(self, x, y):
		
		self.pos = [x*DIMCASE, y*DIMCASE]


	def vie(self):

		pygame.draw.rect(fenetre,NOIR,(self.pos[0],self.pos[1],self.dim,self.dim))

	def mort(self):

		pygame.draw.rect(fenetre,BLANC,(self.pos[0],self.pos[1],self.dim,self.dim))






class Env:

	caseAvant = []
	caseApres = []
	pressPapier = []
	generation = 0
	nCell = casesLigneH*casesLigneV
	vCell = 0
	mCell = nCell

	def __init__(self):
		
		for i in range(casesLigneV):
			self.caseAvant.append([0]*casesLigneH)
		for i in range(casesLigneV):
			self.caseApres.append([0]*casesLigneH)
		for i in range(casesLigneV):
			self.pressPapier.append([0]*casesLigneH)
		

	def out_of_band(self, line, col):

		if line < 0 or col < 0 or line >= casesLigneV or col >= casesLigneH:
			return True
		else:
			return False

	def est_voisine(self, line, col):

		if self.out_of_band(line, col):
			return False

		if self.caseAvant[line][col] == 1:
			return True
		else:
			return False

	def calcul_etat(self, line, col):

		if self.out_of_band(line, col):
			return False

		cellPrec = [line-1, col-1]
		voisine = 0
		for i in range(0, 3, 1):
			if self.est_voisine(cellPrec[0], cellPrec[1]+i):
				voisine += 1
			if self.est_voisine(cellPrec[0]+1, cellPrec[1]+i) and i != 1:
				voisine += 1 
			if self.est_voisine(cellPrec[0]+2, cellPrec[1]+i):
				voisine += 1

		if self.caseAvant[line][col] == 0:
			if voisine == 3:
				self.caseApres[line][col] = 1
		elif self.caseAvant[line][col] == 1:
			if voisine == 3 or voisine == 2:
				self.caseApres[line][col] = 1
			else:
				self.caseApres[line][col] = 0


	def evolution(self, line, col):

		cellPrec = [line-1, col-1]
		for i in range(0, 3, 1):
			self.calcul_etat(cellPrec[0], cellPrec[1]+i)
			self.calcul_etat(cellPrec[0]+1, cellPrec[1]+i)
			self.calcul_etat(cellPrec[0]+2, cellPrec[1]+i)

	def maj_case(self):

		for ln in range(0, casesLigneV, 1):
			for cn in range(0, casesLigneH, 1):
				if self.caseApres[ln][cn] == 1:
					self.caseAvant[ln][cn] = 1
					cell = Cell(cn, ln)
					cell.vie()
				else:
					self.caseAvant[ln][cn] = 0
					cell = Cell(cn, ln)
					cell.mort()

	def refresh(self):

		for ln in range(0, casesLigneV, 1):
			for cn in range(0, casesLigneH, 1):
				if self.caseAvant[ln][cn] == 1:
					cell = Cell(cn, ln)
					cell.vie()
				else:
					self.caseAvant[ln][cn] = 0
					cell = Cell(cn, ln)
					cell.mort()
					

	def creation(self):
		
		for ln in range(0, casesLigneV, 1):
			for cn in range(0, casesLigneH, 1):
				if self.caseAvant[ln][cn] == 1:
					self.evolution(ln, cn)

		self.maj_case()
						
		

	def init_cell(self, idCol, idLine):

		if self.out_of_band(idLine, idCol):
			return
		if self.caseAvant[idLine][idCol] == 1:
			self.caseAvant[idLine][idCol] = 0
			self.caseApres[idLine][idCol] = 0
			cell = Cell(idCol, idLine)
			cell.mort()
			env.vCell -= 1
			env.mCell += 1
		else:
			self.caseAvant[idLine][idCol] = 1;
			cell = Cell(idCol, idLine)
			cell.vie()
			env.vCell += 1
			env.mCell -= 1


	def restart(self):

		for ln in range(0, casesLigneV, 1):
			for cn in range(0, casesLigneH, 1):
				self.caseAvant[ln][cn] = 0
				self.caseApres[ln][cn] = 0
				cell = Cell(cn, ln)
				cell.mort()
				self.generation = 0
				self.vCell = 0
				self.mCell = self.nCell

	def copie_config(self):

		for ln in range(0, casesLigneV, 1):
			for cn in range(0, casesLigneH, 1):
				if self.caseAvant[ln][cn] == 1:
					self.pressPapier[ln][cn] = 1
				else:
					self.pressPapier[ln][cn] = 0
					
	def screen(self):

		ptrL = 0
		ptrC = 0
		ptrLe = 0
		ptrCe = 0
		for ln in range(0, casesLigneV, 1):
			for cn in range(0, casesLigneH, 1):
				if self.caseAvant[ln][cn] == 1:
					ptrL = ln
					break
			if ptrL:
				break
		for cn in range(0, casesLigneH, 1):
			for ln in range(ptrL, casesLigneV, 1):
				if self.caseAvant[ln][cn] == 1:
					ptrC = cn
					break
			if ptrC:
				break

		for ln in range(ptrL, casesLigneV, 1):
			for cn in range(ptrC, casesLigneH, 1):
				if self.caseAvant[ln][cn] == 1:
					if ln >= ptrLe:
						ptrLe = ln
					if cn >= ptrCe:
						ptrCe = cn 
		nSpe = 1
		while os.path.isfile("specimens({}).pgm".format(nSpe)):
			nSpe += 1

		file = open("specimens({}).pgm".format(nSpe), "w")
		file.write("P2\n{} {}\n255\n".format(ptrCe-ptrC+1, ptrLe-ptrL+1))
		for ln in range(ptrL, ptrLe+1, 1):
			for cn in range(ptrC, ptrCe+1, 1):
				if self.caseAvant[ln][cn] == 1:
					file.write("0 ")
				else:
					file.write("255 ")
			file.write("\n")
		file.close()

	def colle_config(self, x, y):

		l = 0
		c = 0
		first = 0
		for ln in range(0, casesLigneV, 1):
			for cn in range(0, casesLigneH, 1):
				if self.pressPapier[ln][cn] == 1:
					if first == 1:
						self.init_cell(int(x/DIMCASE)+cn-c, int(y/DIMCASE)+ln-l)
					else:
						self.init_cell(int(x/DIMCASE), int(y/DIMCASE))
						l = ln
						c = cn
					first = 1


class Specimens:

	def __init__(self, env):
		self.env = env

	def pulsar(self, x, y):

		self.env.init_cell(int(x/DIMCASE), int(y/DIMCASE))
		self.env.init_cell(int(x/DIMCASE)+1, int(y/DIMCASE))
		self.env.init_cell(int(x/DIMCASE)+2, int(y/DIMCASE))

	def planeur1(self, x, y):

		self.env.init_cell(int(x/DIMCASE), int(y/DIMCASE))
		self.env.init_cell(int(x/DIMCASE)+1, int(y/DIMCASE))
		self.env.init_cell(int(x/DIMCASE)+2, int(y/DIMCASE))
		self.env.init_cell(int(x/DIMCASE), int(y/DIMCASE)-1)
		self.env.init_cell(int(x/DIMCASE)+1, int(y/DIMCASE)-2)

	def cell_duplication1(self, x, y):

		self.env.init_cell(int(x/DIMCASE)+1, int(y/DIMCASE))
		self.env.init_cell(int(x/DIMCASE), int(y/DIMCASE)-1)
		self.env.init_cell(int(x/DIMCASE), int(y/DIMCASE)-2)
		self.env.init_cell(int(x/DIMCASE)+2, int(y/DIMCASE)-1)
		self.env.init_cell(int(x/DIMCASE)+2, int(y/DIMCASE)-2)
		self.env.init_cell(int(x/DIMCASE)+1, int(y/DIMCASE)-3)
		self.env.init_cell(int(x/DIMCASE), int(y/DIMCASE)-3)


env = Env()
curseur = Cursor()
spec = Specimens(env)
pygame.init()


fini = False
temps = pygame.time.Clock()
go = False
info = False
grille = True
pygame.display.set_caption("GameOfLife")

fenetre.fill(BLANC)

while not fini:
	mx,  my = pygame.mouse.get_pos()

	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			fini = True
		if event.type == KEYUP:
			if event.key == K_q: #quit
				fini = True
			if event.key == K_g and go == False and info == False: #run
				go = True
			if event.key == K_r and info == False: #restart
				go = False
				env.restart()
			if event.key == K_s and info == False: #stop
				go = False
			if event.key == K_k and info == False:
				env.screen()
			if event.key == K_c and go == False and info == False:
				env.copie_config()
			if event.key == K_v and go == False and info == False:
				env.colle_config(mx, my)
			if event.key == K_a and go == False and info == False:
				spec.pulsar(mx, my)
			if event.key == K_e and go == False and info == False:
				spec.cell_duplication1(mx, my)
			if event.key == K_z and go == False and info == False:
				spec.planeur1(mx, my)
			if event.key == K_p and info == False:
				if grille == True:
					grille = False
					env.refresh()
				else:
					grille = True
			if event.key == K_i and go == False:
				if info:
					fenetre.fill(BLANC)
					env.refresh()
					pygame.display.flip()
					info = False
				else:
					info = True
		if event.type == pygame.MOUSEBUTTONDOWN and go == False and info == False:
			curseur.enleve_curseur(env)
			env.init_cell(int(mx/DIMCASE), int(my/DIMCASE))
	
			
	if go == True and info == False:
		pygame.display.set_caption("gen: " + str(env.generation))
		env.creation()
		env.generation += 1
	elif go == False and info == False:
		curseur.enleve_curseur(env)
		curseur.place_curseur(int(mx/DIMCASE), int(my/DIMCASE), env)
		pygame.display.set_caption("cellules: " + str(env.vCell) + " / " + str(env.nCell))
	else:
		affiche_controles()

	if info == False and grille == True:
		affiche_grille()
	

	temps.tick(60)
	pygame.display.flip()
