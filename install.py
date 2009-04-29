#!/usr/bin/env python
import zohmg.install

if __name__ == "__main__":

	# check for rootness.
	if os.geteuid() != 0:
		print "you need to be root. please sudo."
		sys.exit(1)

	zohmg.install.clean()
	zohmg.install.install()
	zohmg.install.setup()
	zohmg.install.test()

	print
	print "ok, that should do it!"
	print "now try this:"
	print "$> zohmg help"
	print
