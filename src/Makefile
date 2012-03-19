#
# Houdini Ocean Toolkit (HOT) Makefile. This may be used under linux
# and win32/cygwin.
#

#
# You may need to edit this to point to your fftw3 and blitz++
# libraries. Ubuntu users may be able to ignore it and instead install
# the relevant packages, including the "dev" components, using the
# Synaptic package manager.
#

#
# Here we setup up the OS dependant vars ...
#
ifeq ($(OS), Windows_NT)

    ifndef OPTIMIZER
        OPTIMIZER = -Ox
    endif

    MYLIBS=./3rdparty/win32

    INCDIRS = -I.  \
              -I$(MYLIBS)/blitz \
              -I$(MYLIBS) \
              -I./3rdparty/include 

    LIBDIRS = -LIBPATH:$(MYLIBS) libfftw3f-3.lib \
              -LIBPATH:$(MYLIBS) blitz.lib 

    include $(HFS)/toolkit/makefiles/Makefile.win
    DSEXT=dll
    VEXDSO=VEXdso_win32

else

    MYLIBS=./3rdparty/linux

    #OPTIMIZER = -g
	OPTIMIZER = -O2

    LIBDIRS = -L$(MYLIBS)/lib -lfftw3f -lblitz 
    INCDIRS = -I$(MYLIBS)/include -I ./3rdparty/include
    include $(HFS)/toolkit/makefiles/Makefile.linux
    DSEXT=so
    VEXDSO=VEXdso_linux

endif

DSOS = SOP_Ocean.$(DSEXT) VEX_Ocean.$(DSEXT) SOP_Cleave.$(DSEXT)

default: $(DSOS)

SOP_Ocean.$(DSEXT): SOP_Ocean.o
VEX_Ocean.$(DSEXT): VEX_Ocean.o
SOP_Cleave.$(DSEXT): SOP_Cleave.o

SOP_Ocean.C: Ocean.h
VEX_Ocean.C: Ocean.h

TAGINFO = $(shell (echo -n "Compiled on:" `date`"\n         by:" `whoami`@`hostname`"\n$(SESI_TAGINFO)") | sesitag -m)

%.o:		%.C
	$(CC) $(OBJFLAGS) -DMAKING_DSO $(TAGINFO) $< $(OBJOUTPUT) $@

SOP_Ocean.$(DSEXT): SOP_Ocean.o
	$(LINK) $(SHAREDFLAG) SOP_Ocean.o $(DSOFLAGS) $(DSOOUTPUT) $@

VEX_Ocean.$(DSEXT): VEX_Ocean.o
	$(LINK) $(SHAREDFLAG) VEX_Ocean.o $(DSOFLAGS) $(DSOOUTPUT) $@

SOP_Cleave.$(DSEXT): SOP_Cleave.o
	$(LINK) $(SHAREDFLAG) SOP_Cleave.o $(DSOFLAGS) $(DSOOUTPUT) $@


install: $(DSOS)
	mkdir -p $(HIH)/dso
	cp $(DSOS) $(HIH)/dso
	mkdir -p $(HIH)/config/Icons
	cp *.png *.icon $(HIH)/config/Icons
	mkdir -p $(HIH)/vex
	cat $(VEXDSO) >> $(HIH)/vex/VEXdso
	cp $(HIH)/vex/VEXdso $(HIH)/vex/VEXdso.orig
	uniq $(HIH)/vex/VEXdso.orig > $(HIH)/vex/VEXdso

clean:
	rm -f *.o *.$(DSEXT)
