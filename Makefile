# libretro-database
#
# This file provides some install and building commands for libretro-database.
#
# make install
#     Installs the needed files to the given DESTDIR and INSTALLDIR.

PREFIX := /usr
INSTALLDIR := $(PREFIX)/share/libretro/overlays

all:
	@echo "Nothing to make for libretro-overlays."

install:
	mkdir -p $(DESTDIR)$(INSTALLDIR)
	cp -ar -t $(DESTDIR)$(INSTALLDIR) borders ctr effects gamepads ipad keyboards misc wii

test-install: all
	DESTDIR=/tmp/build $(MAKE) install
