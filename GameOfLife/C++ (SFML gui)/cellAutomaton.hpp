#ifndef __CELLAUTOMATON_HPP__
#define __CELLAUTOMATON_HPP__
#include <SFML/Graphics.hpp>
#include <vector>
#include <string>

enum
{
	dead, alive
};

typedef enum
{
	pause_m, play_m
}Mode;

class CellRenderWindow : public sf::RenderWindow
{
private:
	int cellSize;
	int ncellsWidth;
	int ncellsHeight;
	int ncellsMacroWidth;
	int ncells;
	
	void *cells;
	void *cellsCpy;
public:sf::RectangleShape rs;
	int mode;
	CellRenderWindow(int w, int h, const std::string&, int=10);
	char new_state(int, int);
	char get_bit(sf::Vector2<int>&);
	void print_cells();
	void update_cells();
	void refresh();
	void set_cell(sf::Vector2<int>&);
	void set_particulary_cell(sf::Vector2<int>&, int);
	~CellRenderWindow();
};

#endif
