/*
 * kconfig_menu.hpp
 * 
 * Copyright 2016 Andrei Tumbar <atuser@Kronos>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */


#ifndef __AUTOGENTOO_KCONFIG_MENU__
#define __AUTOGENTOO_KCONFIG_MENU__

#include <iostream>
#include <string>
#include <vector>
#include "kconfig_module.hpp"

class __KCONFIG_MENU__
{
	public:
	bool value;
	vector <__KCONFIG_MENU__> menu_list;
	vector <__KCONFIG_MODULE__> module_list;
	__KCONFIG_MENU__
	void add_item ( __KCONFIG_MENU__ input )
	{
		menu_list.push_back ( input );
	}
	
	void add_item ( __KCONFIG_MODULE__ input )
	{
		module_list.push_back ( input );
	}
};

#endif
