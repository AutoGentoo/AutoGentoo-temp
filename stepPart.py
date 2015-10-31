#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  partitions.py
#  
#  Copyright 2015 Andrei Tumbar <atadmin@Kronos>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os
import subprocess
from gi.repository import Gtk, Gdk, GObject
from reparted import *
from reparted.device import probe_standard_devices

global global_unit
global_unit = "m"
class part:
	mounts = []
	format_types = []
	partnums = []
	partsizes = []
	partunits = []
	start = []
	start_unit = []
	end = []
	end_unit = []
	mounts_frees = []
	format_types_frees = []
	partnums_frees = []
	partsizes_frees = []
	partunits_frees = []
	start_frees = []
	start_unit_frees = []
	end_frees = []
	end_unit_frees = []
	primary = []
	parent = []
	extended = False
	partnum = 0
	startnum = 0
	def __init__(self, disk_path, unit):
		os.system("echo -n 'Clearing old values...'")
		part.mounts = []
		part.format_types = []
		part.partnums = [] # Number of Partition (Used for order)
		part.partsizes = []
		part.partunits = []
		part.start = []
		part.start_unit = []
		part.end = []
		part.end_unit = []
		part.primary = []
		part.parent = []
		extended = False
		part.partnum = 0
		os.system("echo 'Done'")
		os.system("echo -n 'Scanning disk %s...'" % disk_path)
		curr_disk = disk.path_to_device[disk_path]
		#Detect partitions
		partitions = curr_disk.partitions()
		#Partition number
		for x in range(len(partitions)): part.partnums.append(partitions[x].num)
		#Start and end
		
		part.mounts_frees = part.mounts
		part.format_types_frees = part.format_types
		part.partnums_frees = part.partnums
		part.partsizes_frees = part.partsizes
		part.partunits_frees = part.partunits
		part.start_frees = part.start
		part.start_unit_frees = part.start_unit
		part.end_frees = part.end
		part.end_unit_frees = part.end_unit
		
def get_value(string, start_num, exit_mark=' '):
	curr_char = ""
	temp = ""
	num = start_num
	while curr_char != exit_mark:
		curr_char = string[num]
		temp += curr_char
		num += 1
	temp = temp.replace(exit_mark, "")
	return_val = [temp, num]
	return return_val
def format_units_size(unit, input_float, demical=2):
	unit = unit.lower()
	unit_list = ["k", "m", "g", "t"]
	unit_values = [1024, 1048576, 1073741824, 1099511627776]
	if unit in unit_list:
		listnum = unit_list.index(unit)
		temp_float = float(input_float)
		temp_float = temp_float/unit_values[listnum]
		input_float = str(round(temp_float, demical))
		return input_float
def format_units(unit, input_float, demical=2):
	unit = unit.lower()
	unit_list = ["k", "m", "g", "t"]
	unit_values = [1, 1024, 1048576, 1073741824]
	if unit in unit_list:
		listnum = unit_list.index(unit)
		temp_float = float(input_float)
		temp_float = temp_float/unit_values[listnum]
		input_float = str(round(temp_float, demical))
		return input_float
def get_iter(gtk_treestore, iters, string, column=0):
	if string == None:
		return None
	current_row = 0
	while gtk_treestore.get_value(iters[current_row], column) != string:
		current_row += 1
	return gtk_treestore.get_iter(gtk_treestore.get_path(iters[current_row]))
class disk:
	devices = []
	path_to_device = {}
	path_to_disk = {}
	disks = []
	sd_disks = []
	size = []
	unit = []
	disk_name = ""
	def __init__(self, disk_num):
		#Clear disk values
		disk.disks = []
		disk.sd_disks = []
		disk.size = []
		disk.unit = []
		disk.path_to_disk = []
		disk.path_to_device = {}
		
		#Probe for Devices
		disk.devices = probe_standard_devices()
		print disk.devices
		
		# Add device paths
		for x in range(0, len(disk.devices)):
			disk.disks.append(disk.devices[x].path)
		
		#Dictionary, path: device
		for x in disk.disks:
			disk.path_to_device[x] = Device(x)
			disk.path_to_disk.append(disk.path_to_device[x])
		
		#Add other disk information
		for x in disk.disks: x.replace("/dev/", "")
		for x in range(0, len(disk.disks)): disk.size.append(float(str(disk.devices[x].size).replace("MB", "")))
		for x in disk.disks: disk.unit.append("M")
		disk.disk_name = disk.devices[disk_num].model
		
class find_free_space:
	free_parts = []
	free_start = []
	free_start_unit = []
	free_end = []
	free_end_unit = []
	free_size = []
	free_size_unit = []
	get_free_true = []
	def __init__(self, current_disk, current_unit):
		find_free_space.free_parts = []
		find_free_space.free_start = []
		find_free_space.free_start_unit = []
		find_free_space.free_end = []
		find_free_space.free_end_unit = []
		find_free_space.free_size = []
		find_free_space.free_size_unit = []
		find_free_space.get_free_true = []
		os.system("parted -s %s unit %siB print free > freespaceinfo_2.txt" % (current_disk, current_unit))
		os.system("cat freespaceinfo_2.txt | grep -i free > freespaceinfo.txt")
		find_part_free = open("freespaceinfo_2.txt", "r").readlines()
		find_part_free = find_part_free[7:]
		current_free_find_line = -1
		while current_free_find_line != len(find_part_free):
			current_free_find_line += 1
			try:
				current_line_free = find_part_free[current_free_find_line]
			except IndexError:
				break
			if current_line_free == "" or current_line_free == " " or current_line_free == "\n":
				break
			if current_line_free[0:3] != "   ":
				find_free_space.get_free_true.append(0)
			else:
				find_free_space.get_free_true.append(1)
		free_info_file = open("freespaceinfo.txt", "r").readlines()
		number_of_frees = len(free_info_file)
		current_num = -1
		while len(find_free_space.free_start) != number_of_frees:
			current_num += 1
			current_line = free_info_file[current_num]
			current_line = current_line.replace("\n", "")
			current_line = current_line.replace(" ", "")
			temp_array = []
			current_char = ""
			current_char_num = -1
			while current_char != "B":
				current_char_num += 1
				current_char = current_line[current_char_num]
				temp_array.append(current_char)
			temp_array.remove(temp_array[len(temp_array)-1])
			temp_array.remove(temp_array[len(temp_array)-1])
			temp_array.remove(temp_array[len(temp_array)-1])
			temp = str1 = ''.join(temp_array)
			find_free_space.free_start.append(float(temp))
			find_free_space.free_start_unit.append(str(current_line[current_char_num-2]))
			current_line = current_line[current_char_num+1:]
			temp_array = []
			current_char = ""
			current_char_num = -1
			while current_char != "B":
				current_char_num += 1
				current_char = current_line[current_char_num]
				temp_array.append(current_char)
			temp_array.remove(temp_array[len(temp_array)-1])
			temp_array.remove(temp_array[len(temp_array)-1])
			temp_array.remove(temp_array[len(temp_array)-1])
			temp = str1 = ''.join(temp_array)
			find_free_space.free_end.append(float(temp))
			find_free_space.free_end_unit.append(str(current_line[current_char_num-2]))
			current_line = current_line[current_char_num+1:]
			temp_array = []
			current_char = ""
			current_char_num = -1
			while current_char != "B":
				current_char_num += 1
				current_char = current_line[current_char_num]
				temp_array.append(current_char)
			temp_array.remove(temp_array[len(temp_array)-1])
			temp_array.remove(temp_array[len(temp_array)-1])
			temp_array.remove(temp_array[len(temp_array)-1])
			temp = str1 = ''.join(temp_array)
			find_free_space.free_size.append(float(temp))
			find_free_space.free_size_unit.append(str(current_line[current_char_num-2]))
def diskType(current_disk):
	return Disk(Device(current_disk)).type_name
