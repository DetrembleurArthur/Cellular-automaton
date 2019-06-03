#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <time.h>
#define DEAD 0
#define ALIVE 1
#ifdef U2
#warning U2
#endif
void print_matrix(char *m, const int ml, const int mc)
{
	for(int i = 0; i < mc+2; i++)
		printf("--");
	printf("\n");
	for(int i = 0; i < ml; i++)
	{
		printf("| ");
		for(int j = 0; j < mc; j++)
		{
			if(*(m+i*mc+j))
			{
				printf("\033[105m  \033[0m");
				//printf("\033[105m \033[0m ");
			}
			else
			{
				printf("  ");
			}
		}
		printf(" |\n");
	}
	for(int i = 0; i < mc+2; i++)
		printf("--");
	printf("\n");
}

int alter(char *m, const int ml, const int mc, const int ipos, const int jpos)
{
	int nb = *(m+ ipos * mc + jpos)?-1:0;
	int i, j;
	int imax, jmax;
	if(ipos-1 < 0)
		i = ipos;
	else
		i = ipos-1;
	if(ipos+1 >= ml)
		imax = ipos;
	else
		imax = ipos+2;
	if(jpos+1 >= mc)
		jmax = jpos;
	else
		jmax = jpos+2;
	while(i < imax)
	{
		if(jpos-1 < 0)
			j = jpos;
		else
			j = jpos-1;
		while(j < jmax)
		{
			if(*(m + i * mc + j))
				nb++;
			j++;
		}
		i++;
	}
	
	if(nb <= 1)
		return DEAD;
	if(nb >= 4)
		return DEAD;
	if(nb == 2 || nb == 3)
	{
		if(*(m+ ipos * mc + jpos) == DEAD)
		{
			if(nb == 3)
			{
				return ALIVE;
			}
			else
				return DEAD;
		}
		else
		{
			return ALIVE;
		}
	}

	return ALIVE;
}

void update_matrix(char *m, char *bis, const int ml, const int mc)
{
	for(int i = 0; i < ml; i++)
	{
		for(int j = 0; j < mc; j++)
		{
			*(bis + i * mc + j) = alter(m, ml, mc, i, j);
		}
	}
	for(int i = 0; i < ml; i++)
		for(int j = 0; j < mc; j++)
			*(m + i * mc + j) = *(bis + i * mc + j);
}


void update_matrix2(char *m, char *bis, const int ml, const int mc)
{
	int i, j, k, l;clock_t t1 = clock();
	for(i = 0; i < ml; i++)
	{
		for(j = 0; j < mc; j++)
		{
			if(*(m + i *mc + j))
			{
				*(bis + i * mc + j) = alter(m, ml, mc, i, j);
				for(k = i-1; k <= i+1; k++)
				{
					for(l = j-1; l <= j+1; l++)
					{
						if(k!=i || l!=i)
						{
							if(k >= 0 && k < ml)
							{
								if(l >= 0 && l < mc)
								{
									if(!*(m + k *mc + l))
										*(bis + k * mc + l) = alter(m, ml, mc, k, l);
								}
							}
						}
					}
				}
			}
		}
	}
	fprintf(stderr,"%lf,", (clock()-t1)/(double)CLOCKS_PER_SEC);

	for(int i = 0; i < ml; i++)
		for(int j = 0; j < mc; j++)
			*(m + i * mc + j) = *(bis + i * mc + j);
		
		exit(0);
}

void set_matrix(char *m, const int mml, const int mmc, int ybeg, int xbeg, char *s, const int ml, const int mc)
{
	for(int i = ybeg; i < ybeg+ml; i++)
	{
		for(int j = xbeg; j < xbeg+mc; j++)
		{
			*(m + i * mmc + j) = *(s + (i-ybeg) * mc + (j-xbeg));
		}
	}
}

void interrupt(int dummy)
{
	fprintf(stderr, "stop\n");
	exit(0);
}

int main(void)
{
	signal(SIGINT, interrupt);
	const int ml = 140;//70;
	const int mc = 80;//180;
	char matrix[ml][mc] = {DEAD};
	char bis[ml][mc] = {DEAD};
	char planneur[3][3] = {
		{0,1,0},
		{0,0,1},
		{1,1,1},
	};
	printf("%d\n",ml*mc );
	char set[9][36] = {
		{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1},
		{0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1},
		{1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
		{1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	};
	char set2[9][18] = {
		{1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
		{1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0},
		{1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0},
		{0,1,0,0,1,0,0,1,1,0,0,0,0,0,1,1,1,0},
		{0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1},
		{0,1,0,0,1,0,0,1,1,0,0,0,0,0,1,1,1,0},
		{1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0},
		{1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0},
		{1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	};

	char set3[16][15] = {
		{0,0,0,0,1,1,1,1,0,0,0,0,0,0,0},
		{0,0,0,1,1,1,1,1,1,0,0,0,0,0,0},
		{0,0,1,1,0,1,1,1,1,0,0,0,0,0,0},
		{0,0,0,1,1,0,0,0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0,0,0,0,1,1,0,0},
		{0,1,0,0,0,0,0,0,0,0,0,0,0,0,1},
		{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
		{1,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
		{1,1,1,1,1,1,1,1,1,1,1,1,1,1,0},
		{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
		{0,0,0,0,1,1,1,1,0,0,0,0,0,0,0},
		{0,0,0,1,1,1,1,1,1,0,0,0,0,0,0},
		{0,0,1,1,0,1,1,1,1,0,0,0,0,0,0},
		{0,0,0,1,1,0,0,0,0,0,0,0,0,0,0},
	};
	//set_matrix(&matrix[0][0], ml, mc, 0,0,&planneur[0][0], 3,3);
	//set_matrix(&matrix[0][0], ml,mc, 0,0, &set[0][0], 9,36);
	//set_matrix(&matrix[0][0], ml,mc, 50,mc-18, &set2[0][0], 9,18);
	//set_matrix(&matrix[0][0], ml,mc, 0,mc-20, &set3[0][0], 16,15);
	int i = 0;
	//FILE *fp = fopen("mesures.txt", "at");
	//#ifdef U2
	//fprintf(fp, "\nopti:");
	//#else
	//fprintf(fp, "\nbase:");
	//#endif
	
	//for(int j = 1; j <= 30; j++){
		//i=0;
		clock_t t1 = clock();
		printf("2.\n");
		while(i <1000/*i < j*10*/)
		{
			//system("clear");
			//print_matrix(&matrix[0][0], ml,mc);
			#ifdef U2
			update_matrix2(&matrix[0][0], &bis[0][0], ml,mc);
			#else
			update_matrix(&matrix[0][0], &bis[0][0], ml,mc);
			#endif
			//usleep(0.03333333333333333*1000000);
			i++;
		}
		//printf("i -> %d: %lf\n", j*10,(clock()-t1)/(double)CLOCKS_PER_SEC);
		//fprintf(stderr,"%lf,", (clock()-t1)/(double)CLOCKS_PER_SEC);
	//}
	//fclose(fp);

	return 0;
}
