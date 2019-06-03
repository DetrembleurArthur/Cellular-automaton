/** COMPILATION **
g++ -o test test.cpp -lsfml-graphics -lsfml-window -lsfml-system
******************/
#include <SFML/Graphics.hpp>
#include <iostream>
#include <string>
#include <unistd.h>
#include <vector>
#include "cellAutomaton.hpp"

/*
Add random mode
Add modify size
*/

int main()
{
	bool pulse = false, deleteCell=false, drawColorPulse=false;
	int timemcs=1000;
	char color=0;
	sf::Vector2i v;
	CellRenderWindow window(1400,800, "Cellular automaton", 1);
	window.print_cells();
	while(window.isOpen())
	{
		for(sf::Event event;window.pollEvent(event);)
		{
			if(event.type == sf::Event::Closed)
				window.close();
			if(event.type == sf::Event::KeyPressed)
			{
				if(event.key.code == sf::Keyboard::P)
				{
					window.mode = (window.mode+1)%2;
				}
			}
		}
		
		if(window.mode == play_m)
		{
			if(sf::Keyboard::isKeyPressed(sf::Keyboard::Left))
			{
				timemcs += 1000;
				if(timemcs > 1000000)
					timemcs = 1000000;
			}
			else if(sf::Keyboard::isKeyPressed(sf::Keyboard::Right))
			{
				timemcs -= 1000;
				if(timemcs < 0)
					timemcs = 0;
			}
			window.clear(sf::Color::Black);
			window.update_cells();
			usleep(timemcs);
		 	window.display();
		}
		else
		{
			if(not pulse and sf::Mouse::isButtonPressed(sf::Mouse::Left))
			{
				v = sf::Mouse::getPosition(window);
				window.print_cells();
				window.set_cell(v);
				window.display();
				pulse = true;
			}
			if(pulse)
			{
				if(not sf::Mouse::isButtonPressed(sf::Mouse::Left))
				{
					pulse = false;
				}
			}
			if(not pulse)
			{
				if(not drawColorPulse and sf::Mouse::isButtonPressed(sf::Mouse::Right))
				{
					v = sf::Mouse::getPosition(window);
					drawColorPulse = true;
					color = window.get_bit(v);
				}
				if(drawColorPulse)
				{
					if(not sf::Mouse::isButtonPressed(sf::Mouse::Right))
					{
						drawColorPulse = false;
					}
					else
					{
						if(color != -1)
						{
							v = sf::Mouse::getPosition(window);
							window.print_cells();
							window.set_particulary_cell(v, color);
							window.set_cell(v);
							window.display();
						}
					}
				}
			}
		}
	}
	
	return 0;
}









