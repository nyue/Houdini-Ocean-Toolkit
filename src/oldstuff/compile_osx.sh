#!/bin/sh
echo
echo
echo "Building and installing the Houdini Ocean Toolkit..."
echo
#
# You may need to edit this to point to your fftw3 and blitz++
# libraries. Ubuntu users may be able to ignore it and instead install
# the relevant packages, including the "dev" components, using the
# Synaptic package manager.
#
MYLIBS=./3rdparty/osx

hcustom -e -I./3rdparty/include \
        -I $MYLIBS/include \
        -L $MYLIBS/lib     \
        -l blitz \
        -l fftw3f \
        SOP_Cleave.C SOP_Ocean.C VEX_Ocean.C 
echo "Done compiling and installing the DSO's to $HIH/dso."
echo

# HIH isn't defined for the Mac version of houdini ... ???
HIH=$HOME/Library/Preferences/houdini/$HOUDINI_MAJOR_RELEASE.$HOUDINI_MINOR_RELEASE

ICON_DIR="$HIH/config/Icons"
mkdir -p "$ICON_DIR"
cp *.icon "$ICON_DIR"
cp *.png "$ICON_DIR"
echo "Done installing the icon files to $HIH/config/Icons."
echo
        
mkdir -p $HIH/vex
cat VEXdso_osx >> $HIH/vex/VEXdso
cp $HIH/vex/VEXdso $HIH/vex/VEXdso.orig
uniq $HIH/vex/VEXdso.orig > $HIH/vex/VEXdso
echo "Done installing and editing $HIH/vex/VEXdso."
echo
echo "All done. You can now try loading ../examples_and_otl/sop_simple.hip"
echo





