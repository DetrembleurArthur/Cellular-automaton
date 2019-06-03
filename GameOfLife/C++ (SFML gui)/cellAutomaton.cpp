#include "cellAutomaton.hpp"
#include <iostream>
#include <stdlib.h>
#include <stdlib.h>
#define _obsolete
#define get_bit_value(line, bit) ((*((unsigned char*)cells + line * ncellsWidth + bit/8) >> (7-bit%8))&1)
#define set_bit(line, bit) *((unsigned char*)cellsCpy + line * ncellsWidth + bit/8) |= (1 << (7-(bit%8)))
#define config(line, bit) *((unsigned char*)cells + line * ncellsWidth + bit/8) |= (1 << (7-(bit%8)))
#define delete_bit(line, bit) *((unsigned char*)cells + line * ncellsWidth + bit/8) &= ~(1 << (7-(bit%8)))

CellRenderWindow::CellRenderWindow(int width, int height, const std::string& title, int cellSize) : sf::RenderWindow(sf::VideoMode(width, height),title),cellSize(cellSize), rs(sf::Vector2f(cellSize, cellSize)), mode(pause_m)
{
	ncellsMacroWidth = (width/cellSize);
	ncellsWidth = (double)width/cellSize/8-width/cellSize/8>0?width/cellSize/8+1:width/cellSize/8;
	ncellsHeight = height/cellSize;
	ncells = ncellsMacroWidth*ncellsHeight;
	cells = new unsigned char[ncellsHeight*ncellsWidth];
	cellsCpy = new unsigned char[ncellsHeight*ncellsWidth];
	int i;
	for(i = 0; i < ncellsHeight*ncellsWidth; i++)
	{
		*((unsigned char*)cells+i) = 0;
		*((unsigned char*)cellsCpy+i) = 0;
	}

	rs.setFillColor(sf::Color(255,255,255));
}

char CellRenderWindow::new_state(int i, int j)
{
	int ii, jj, nb = 0;
	for(ii = i-1; ii <= i+1; ii++)
	{
		for(jj = j-1; jj <= j+1; jj++)
		{
			if(ii >= 0 && ii < ncellsHeight)
			{
				if(jj >= 0 && jj < ncellsMacroWidth)
				{
					if(ii != i || jj != j)
					{
						if(get_bit_value(ii, jj))
						{
							nb++;
						}
					}
				}
			}
		}
	}
	if(get_bit_value(i, j))
	{
		if(nb == 2 || nb == 3)
		{
			return 1;
		}
		else
		{
			return 0;
		}
	}
	else
	{
		if(nb == 3)
		{
			return 1;
		}
		else
		{
			return 0;
		}
	}
}

void CellRenderWindow::update_cells()
{
	int i, j, k, l;
	for(i = 0; i < ncellsHeight; i++)
	{
		for(j = 0; j < ncellsMacroWidth; j++)
		{
			if(get_bit_value(i, j))
			{
				if(new_state(i, j))
				{
					rs.setPosition(j*cellSize , i*cellSize);
					this->draw(rs);
					set_bit(i, j);
				}
				for(k = i-1; k <= i+1; k++)
				{
					for(l = j-1; l <= j+1; l++)
					{
						if(k >= 0 && k < ncellsHeight)
						{
							if(l >= 0 && l < ncellsMacroWidth)
							{
								if(k != i || l != j)
								{
									if(get_bit_value(k, l) == 0)
									{
										if(new_state(k, l))
										{
											rs.setPosition(l*cellSize , k*cellSize);
											this->draw(rs);
											set_bit(k, l);
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
	int ncellsFormat;
	for(ncellsFormat = 8; ncellsFormat > 0; ncellsFormat -= ncellsFormat/2)
	{
		if((ncellsHeight*ncellsWidth) % ncellsFormat == 0)
		{
			switch(ncellsFormat)
			{
				case 8:
					ncellsFormat = (ncellsHeight*ncellsWidth)/ncellsFormat;
					for(i = 0; i < ncellsFormat; i++)
					{
						*((unsigned long *)cells + i) = *((unsigned long*) cellsCpy + i);
						*((unsigned long*) cellsCpy + i) = 0;
					}
					break;
				case 4:
					ncellsFormat = (ncellsHeight*ncellsWidth)/ncellsFormat;
					for(i = 0; i < ncellsFormat; i++)
					{
						*((unsigned *)cells + i) = *((unsigned *) cellsCpy + i);
						*((unsigned *) cellsCpy + i) = 0;
					}
					break;
				case 2:
					ncellsFormat = (ncellsHeight*ncellsWidth)/ncellsFormat;
					for(i = 0; i < ncellsFormat; i++)
					{
						*((unsigned short *)cells + i) = *((unsigned short*) cellsCpy + i);
						*((unsigned short *) cellsCpy + i) = 0;
					}
					break;
				default:
					ncellsFormat = (ncellsHeight*ncellsWidth)/ncellsFormat;
					for(i = 0; i < ncellsFormat; i++)
					{
						*((unsigned char *)cells + i) = *((unsigned char*) cellsCpy + i);
						*((unsigned char *) cellsCpy + i) = 0;
					}
					break;
			}
			ncellsFormat = 0;
		}
	}
}


void _obsolete CellRenderWindow::print_cells()
{
	int i, j;
	this->clear(sf::Color::Black);
	for(i = 0; i < ncellsHeight; i++)
	{
		for(j = 0; j < ncellsMacroWidth; j++)
		{
			if(get_bit_value(i, j))
			{
				rs.setPosition(j*cellSize , i*cellSize);
				this->draw(rs);
			}
		}
	}
	this->display();
}

void CellRenderWindow::refresh()
{
	this->draw(rs);
	this->display();
}

void CellRenderWindow::set_cell(sf::Vector2<int>& mousePos)
{
	int x=mousePos.x/cellSize, y=mousePos.y/cellSize;
	if(x >= 0 and x < ncellsMacroWidth)
	{
		if(y >= 0 and y < ncellsHeight)
		{
			if(get_bit_value(y, x) == 1)
			{
				rs.setFillColor(sf::Color(0,0,0));
				delete_bit(y, x);
			}
			else
			{
				rs.setFillColor(sf::Color(255,255,255));
				config(y, x);
			}
			rs.setPosition(x*cellSize, y*cellSize);
			this->draw(rs);
			rs.setFillColor(sf::Color(255,255,255));
		}
	}
}

void CellRenderWindow::set_particulary_cell(sf::Vector2<int>& mousePos, int mode)
{
	int x=mousePos.x/cellSize, y=mousePos.y/cellSize;
	sf::Color c = mode?sf::Color(255,255,255):sf::Color(0,0,0);
	rs.setFillColor(c);
	if(x >= 0 and x < ncellsMacroWidth)
	{
		if(y >= 0 and y < ncellsHeight)
		{
			if(not mode)
			{
				rs.setFillColor(c);
				delete_bit(y, x);
			}
			else
			{
				config(y, x);
			}
			rs.setPosition(x*cellSize, y*cellSize);
			this->draw(rs);
			rs.setFillColor(sf::Color(255,255,255));
		}
	}
}

char CellRenderWindow::get_bit(sf::Vector2<int>& mousePos)
{
	int x=mousePos.x/cellSize, y=mousePos.y/cellSize;
	if(x >= 0 and x < ncellsMacroWidth)
	{
		if(y >= 0 and y < ncellsHeight)
		{
			return get_bit_value(y, x);
		}
	}
	return -1;
}

CellRenderWindow::~CellRenderWindow()
{
	delete [] (char*)cells;
	delete [] (char*)cellsCpy;
}
