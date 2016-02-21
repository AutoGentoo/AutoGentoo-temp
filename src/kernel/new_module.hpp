/*
 * new_module.hpp
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

#ifndef __AUTOGENTOO_NEW_MODULE__
#define __AUTOGENTOO_NEW_MODULE__

#include <iostream>
#include "module.hpp"

using namespace std;

class NEW_MODULE: public __MODULE__
{
	public:
	string changed_value;
	
	NEW_MODULE ( string input, string _changed_value ) : __MODULE__ ( input )
	{
		changed_value = _changed_value;
	}
};

#endif
