#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  portage.py
#  
#  Copyright 2017 Andrei Tumbar <atuser@Hyperion>
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

from collections import namedtuple
import os
from stdio import *
import socketrequest
import _xml

global current_keywords
current_keywords = ["amd64", "x86", "alpha", "arm", "hppa", "ia64", "ppc", "ppc64", "sparc"]

Ebuild = namedtuple ("Ebuild", ('name', 'id', 'keywords', 'slot'))
PackageBinary = namedtuple ("PackageBinary", ("name", "category", "version", "slot", "build_time", "size", "use"))
PackageMeta = namedtuple ("PackageMeta", ("name", "v_id")) # Used to id packages before generation
Flag = namedtuple ("Flag", ("name", "description"))
Package = namedtuple ("Package", ("name", "category", "description", "homepage", "versions", "license", "globaluse"))

class portage:
    packages = {} # category: {name: Package}
    package_list = {} # {name: category} used for searching
    server_packages = {}
    global_use = {}
    local_use = {}
    path = ""
    binhost_ip = ""
    binhost_port = 9490
    
    def __init__ (self, binhost_ip, path="/usr/portage"):
        self.path = os.path.expanduser(path)
        self.generate_global_use ()
        self.generate_local_use ()
        self.generate_packages ()
        self.binhost_ip = binhost_ip
        socket_package = socketrequest.SocketRequest (self.binhost_ip, 9490)
        res = socket_package.send (b"GET /Packages HTTP/1.0").decode ("utf-8")
        self.generate_server_packages (res.splitlines ()[2:]) # Skip 200 OK and newline
    
    def readlines (self, path):
        out = []
        with open ("%s/%s" % (self.path, path), "r") as f:
            out = f.read().splitlines()
            f.close ()
        return out
    
    def generate_global_use (self):
        b = self.readlines ("profiles/use.desc")
        for x in b:
            if not x: # Skip comments and empty lines
                continue
            elif x[0] == "#":
                continue
            i_b = x.find (" ")
            self.global_use[x[:i_b]] = Flag (x[:i_b], x[i_b+3:])
    
    def get_dirs (self, path):
        return [name for name in os.listdir(path)
                if os.path.isdir(os.path.join(path, name))]
    
    def parse_version_id (self, buff):
        if (buff[buff.rfind("-")+1] == 'r'): # Revision number
            v_id = buff[buff.rfind ("-", 0, buff.rfind ("-"))+1:]
            name = buff[:buff.rfind ("-", 0, buff.rfind ("-"))]
        else:
            v_id = buff[buff.rfind ("-")+1:]
            name = buff[:buff.rfind ("-")]
        return PackageMeta (name, v_id)
    
    def gen_unknown_key (self):
        out = {}
        for x in current_keywords:
            out[x] = "unknown"
        return out
    
    def gen_keywords (self, keyword_str):
        # KEYWORD STATUS
        # 0 = stable
        # 1 = unstable (~)
        # 2 = broken (-)
        # 3 = unknown
        
        key_list = list(filter(bool, keyword_str.split (" ")))
        out = self.gen_unknown_key () # They default to unknown
        for key in key_list:
            if (key == "*"):
                for x in current_keywords:
                    try:
                        out[x]
                    except KeyError:
                        out[x] = "stable"
                continue
            if (key == "~*"):
                for x in current_keywords:
                    try:
                        out[x]
                    except KeyError:
                        out[x] = "unstable"
                continue
            if (key == "**"):
                for x in current_keywords:
                    out[x] = "masked"
                break
            
            status = "stable"
            if key[0] == "~":
                status = "unstable"
                key = key[1:]
            elif key[0] == "-":
                status = "masked"
                key = key[1:]
            out[key] = status
        
        return out
    
    def get_cats (self):
        return self.readlines ("profiles/categories")
    
    def generate_local_use (self):
        cats = self.get_cats ()
        localuse = self.readlines ("profiles/use.local.desc")
        self.local_use = {}
        for cat in cats:
            self.local_use[cat] = {}
        for line in localuse:
            if not line: # Skip comments and empty lines
                continue
            elif line[0] == "#":
                continue
            desc_delim = line.find (" ")
            c_cat = line[:line.find("/")]
            name = line[line.find("/")+1:line.find(":")]
            flag_name = line[line.find(":")+1:line.find(" ")]
            desc = line[line.find(" ")+3:]
            try:
                self.local_use[c_cat][name]
            except KeyError:
                self.local_use[c_cat][name] = []
            self.local_use[c_cat][name].append (Flag (flag_name, desc))
    
    def parse_cpv (self, cpv):
        cat = cpv[:cpv.find("/")]
        namebuf = cpv[cpv.find("/")+1:]
        vid = self.parse_version_id (namebuf)
        return cat, vid.name, vid.v_id
    
    def generate_server_packages (self, binhost_package_lines):
        self.server_packages = {}
        dirs = self.get_cats ()
        for cat in dirs:
            self.server_packages [cat] = {}
        package_buff = list (group (binhost_package_lines, ""))
        for pkg in package_buff[1:-1]:
            parsed = self.parse_from_delim (pkg, ": ")
            cat, name, v = self.parse_cpv(parsed["CPV"])
            try:
                self.server_packages[cat][name]
            except KeyError:
                self.server_packages[cat][name] = {}
            try:
                parsed["SLOT"]
            except KeyError:
                parsed["SLOT"] = "0"
            self.server_packages[cat][name][v] = PackageBinary(name, cat, v, parsed["SLOT"], parsed["BUILD_TIME"], parsed["SIZE"], parsed["USE"])
    
    def parse_from_delim (self, lines, delim):
        parsed = {}
        for line in lines:
            splt = line.split (delim, 1)
            parsed[splt[0]] = splt[1]
        return parsed
    
    def generate_package (self, cat, pkg):
        meta = self.parse_version_id (pkg)
        metalines = self.readlines ("metadata/md5-cache/%s/%s" % (cat, pkg))
        parsed = self.parse_from_delim (metalines, "=")
        keywords = {}
        slot = ""
        _license = []
        try:
            keywords = self.gen_keywords(parsed["KEYWORDS"])
        except KeyError:
            keywords = self.gen_unknown_key ()
        for x in keywords:
            if keywords[x] == 2:
                printf ("%s/%s %s\n", cat, pkg, x)
                break
        try:
            slot = parsed["SLOT"]
        except KeyError:
            slot = "0"
        try:
            parsed["DESCRIPTION"]
        except KeyError:
            parsed["DESCRIPTION"]
        try:
            parsed["HOMEPAGE"]
        except KeyError:
            parsed["HOMEPAGE"] = ""
        try:
            _license = parsed["LICENSE"]
        except KeyError:
            pass
        try:
            parsed["IUSE"]
        except KeyError:
            parsed["IUSE"] = ""
            
        return Ebuild(meta.name, meta.v_id, keywords, slot), meta, parsed, _license, parsed["IUSE"]
    
    def get_flag_names (self, arr):
        out = []
        for x in arr:
            out.append (x.name)
        return out
    
    def parse_iuse (self, iuse_list, cat, pkg):
        out = []
        for flag in iuse_list:
            if not flag:
                continue
            if flag[0] in ("+", "-"):
                flag = flag[1:]
            try:
                if (flag not in self.get_flag_names(self.local_use[cat][pkg])):
                    out.append (flag)
            except KeyError:
                out.append (flag)
        return out
    
    def generate_packages (self):
        self.packages = {}
        self.package_list = {}
        dirs = self.get_cats ()
        for cat in dirs:
            self.packages [cat] = {}
            self.server_packages[cat] = {}
            
            cat_pkgs = os.listdir ("%s/metadata/md5-cache/%s" % (self.path, cat))
            for pkg in cat_pkgs:
                temp, meta, parsed, _license, iuse = self.generate_package(cat,pkg)
                try:
                    self.packages[cat][meta.name]
                except KeyError:
                    global_iuse = self.parse_iuse (iuse.split (" "), cat, meta.name)
                    self.packages[cat][meta.name] = Package (meta.name, cat, parsed["DESCRIPTION"], parsed["HOMEPAGE"], [], _license, global_iuse)
                    self.package_list[meta.name] = cat
                self.packages[cat][meta.name].versions.append (temp)
    
    def search (self, atom):
        pkg_buf = [s for s in self.package_list if atom in s]
        out = []
        for x in pkg_buf:
            out.append (self.packages[self.package_list[x]][x])
        return out
    
    def get_maintainer (self, cat, pkg):
        tree = _xml._XML ("%s/%s/%s/metadata.xml" % (self.path, cat, pkg))
        return tree.pkgmetadata.maintainer.email.text(), tree.pkgmetadata.maintainer.name.text()

def main(args):
    temp = portage ("kronos", "~/Downloads/portage")
    print(temp.get_maintainer("sys-devel", "gcc"))
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
