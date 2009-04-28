#!/usr/bin/env python
import zohmg.install

if __name__ == "__main__":
	zohmg.install.clean()
	zohmg.install.install()
	zohmg.install.setup()

	print
	print "ok, that should do it!"
	print "now try this:"
	print "$> zohmg help"
	print
