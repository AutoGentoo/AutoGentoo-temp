#! /usr/bin/env python

from client import Server, Host
from api.request import *
import pprint
import atexit
import rlcompleter
import readline
import traceback
import time

histfile = ".autogentoo_history"
try:
	readline.read_history_file(histfile)
	# default history len is -1 (infinite), which may grow unruly
	readline.set_history_length(1000)
except FileNotFoundError:
	pass

atexit.register(readline.write_history_file, histfile)


class Cli:
	port = 9491
	
	def __init__(self, path):
		self.path = path
		self.server = Server(self.path)
		self.commands = {
			"stage3": ("host_id", "args"),
			"mkhost": ("arch", "profile", "hostname"),
			"emerge": ("host_id", "emerge_str"),
			"ls": (),
			"help": (),
			"q": (),
		}
		
		self.completion = self.commands
		
		readline.set_completer(rlcompleter.Completer(self.completion).complete)
		readline.parse_and_bind("tab: complete")
		
		self.pp = pprint.PrettyPrinter(indent=1)

	def update_completion(self):
		for host_id in self.server.hosts:
			self.completion[host_id] = self.server.hosts[host_id]
		
		readline.set_completer(rlcompleter.Completer(self.completion).complete)

	def cli(self):
		time.sleep(0.1)
		while True:
			try:
				self.server.read()
			except IOError:
				traceback.print_exc(file=sys.stdout)
				print("Failed to read config")
			
			self.update_completion()
			try:
				line = input("autogentoo > ").strip()
				if not len(line):
					continue
			except KeyboardInterrupt:
				break
			
			try:
				res = self.command(line)
			except KeyboardInterrupt:
				print("")
				continue
			except Exception:
				traceback.print_exc(file=sys.stdout)
			else:
				if res is not None:
					print(res)
	
	def command(self, cmd_name):
		try:
			arg_enum = self.commands[cmd_name]
		except KeyError:
			return "Command %s not found" % cmd_name
		
		args = []
		for i in arg_enum:
			args.append(input("%s: " % i).replace("\n", ""))
		
		return eval("self.%s(*args)" % cmd_name)
	
	def stage3(self, host_id, args=""):
		req = Request(Address("localhost", self.port), Request.REQ_HOST_STAGE3, [
			Request.authorize("cli", self.server.sudo_token),
			Request.host_select(host_id),
			Request.job_select(args)
		])
		
		req.send()
		res = req.recv()
		
		print(res.content)
	
	def emerge(self, host_id, emerge_str):
		req = Request(Address("localhost", self.port), Request.REQ_HOST_EMERGE, [
			Request.authorize("cli", self.server.sudo_token),
			Request.host_select(host_id),
			Request.host_emerge(emerge_str)
		])
		
		req.send()
		res = req.recv()
		
		print(res.content)
	
	def mkhost(self, arch, profile, hostname):
		req = Request(Address("localhost", self.port), Request.REQ_HOST_NEW, [
			Request.authorize("cli", self.server.sudo_token),
			Request.host_new(Host.generate_id(), arch, profile, hostname)
		])
		
		req.send()
		req.recv()
	
	def ls(self):
		for host_id, host in self.server.hosts.items():
			print("id: %s" % host_id)
			print("path: %s" % host.get_path())
			print("arch %s" % host.arch)
			print("profile %s" % host.profile)
			print("")
		
		if not len(self.server.hosts):
			print("No hosts")
	
	def help(self):
		self.pp.pprint(self.commands)
	
	def q(self):
		exit(0)


def main(args):
	if len(args) != 2:
		print("usage %s [config path]" % args[0])
		return 1
	
	cli = Cli(args[1])
	cli.cli()
	
	return 0


if __name__ == "__main__":
	import sys
	exit(main(sys.argv))
