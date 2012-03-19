#
# build and deployment tool for the HOT
#

from __future__ import with_statement
import os,sys,platform,zipfile
from paver.easy import *
from paver.setuputils import setup

release_version = '1.0rc9'

srcfiles = 'SOP_Cleave.C SOP_Ocean.C VEX_Ocean.C'.split()

# work out what platform we're using
if platform.system() == 'Linux':
    if platform.machine()=='x86_64':
        build_type = 'linux64'
    else:
        build_type = 'linux32'
    soext = '.so'
    oext = '.o'
    includes='-I 3rdparty/linux/include -I 3rdparty/include'
    libs='-L 3rdparty/linux/lib -l blitz -l fftw3f'
    python_exe = 'python'
elif platform.system() == 'Darwin':
    build_type = 'osx'
    soext = '.dylib'
    oext = '.o'
    includes='-I 3rdparty/osx/include -I 3rdparty/include'
    libs='-L 3rdparty/osx/lib -l blitz -l fftw3f'
    python_exe = 'python'
elif platform.system() == 'Windows':
    if platform.architecture()[0] == '64bit':
        build_type = 'win64'
    else:
        build_type = 'win32'
    soext = '.dll'
    oext = '.o'
    includes='-I 3rdparty/%s -I 3rdparty/include' % build_type
    libs='-L 3rdparty/%s -l blitz.lib -l libfftw3f-3.lib' % build_type
    python_exe = 'hython'
else:
    RuntimeError('paver script has not been implemented for this architecture (%s)' % sys.platform)

@task
def update_docs():
    """makes the html docs and pushes them to the web site"""
    with pushd(path('../docs')):
        sh('make html')
    sh('scp -r ../docs/_build/* sf:public_html/houdini/ocean/docs')

@task
def clean():
    """remove the build files"""
    for f in srcfiles:
        path(soname(f)).remove()
        path(oname(f)).remove()
    if 'win' in build_type:
        for f in srcfiles:
            path(soname(f)+'.manifest').remove()
            path(f[:-2]+'.exp').remove()
            path(f[:-2]+'.lib').remove()

    for p in path('.').glob('hotbin_*'):
        if p.isdir():
            p.rmtree()
    for p in path('.').glob('hotsrc_*'):
        if p.isdir():
            p.rmtree()
    for p in path('.').glob('hotbin_*.zip'):
        p.remove()
    for p in path('.').glob('hotsrc_*.zip'):
        p.remove()

@task
def build():
    """builds the plugins inplace, doesn't install them"""
    call_task('clean')
    call_task('build_sop_cleave')
    call_task('build_sop_ocean')
    call_task('build_vex_ocean')

def install():
    """installs the plugins, not completed"""
    sofiles = map(soname,srcfiles)

def szipname():
    return 'hotsrc_%s.zip' % release_version

@task
def sdist():
    """make a source distribution"""
    zipname = szipname()
    path(zipname).remove()
    sh('hg archive -t zip %s' % zipname)

def bdistname():
    return 'hotbin_%s_H%s.%s.%s_%s' % (build_type,
                                      os.getenv('HOUDINI_MAJOR_RELEASE'),
                                      os.getenv('HOUDINI_MINOR_RELEASE'),
                                      os.getenv('HOUDINI_BUILD_VERSION'),
                                      release_version)
@task
@cmdopts([('norebuild','n','don\'t rebuild the targets')])
def bdist(options):
    """makes a binary distribution of the plugins"""

    if 'norebuild' not in options.bdist:
        call_task('build')

    path('hotdist').rmtree()
    path('hotdist').makedirs()

    with pushd('hotdist'):
        path('dso').makedirs()
        path('config').makedirs()
        path('config/Icons').makedirs()
        path('vex').makedirs()
        path('otls').makedirs()

    # copy the dso's
    for f in srcfiles:
        path(soname(f)).copy(path('hotdist/dso')/soname(f))

    # copy in the Icons
    for f in path('.').files('*.png'):
        f.copy(path('hotdist/config/Icons')/f)
    for f in path('.').files('*.icon'):
        f.copy(path('hotdist/config/Icons')/f)
        
    # write the VEXdso
    path('hotdist/vex/VEXdso').write_lines([soname('VEX_Ocean.C')])

    # copy the otl
    for f in path('../otls').files('*.otl'):
        f.copy(path('hotdist/otls'))

    # copy the examples
    path('../examples').copytree('hotdist/examples')

    # if we are on windows, we need manifests and the fftw dll
    if build_type == 'win32' or build_type == 'win64':
        for f in srcfiles:
            name = soname(f)+'.manifest'
            path(name).copy(path('hotdist/dso')/name)
        path('hotdist/dlls').makedirs()
        path('3rdparty/%s/libfftw3f-3.dll' % build_type).copy(path('hotdist/dlls'))

    # finally move the directory to a representative name
    n = bdistname()
    path(n).rmtree()
    path('hotdist').rename(n)

    # zip it up
    zipname = '%s.zip' % n
    path(zipname).remove()
    zipper(n,n+'.zip')
    path(n).rmtree()

@task
def upload_bdist():
    """uploads the binary distribution to google code"""
    zipname = '%s.zip' % bdistname()
    sh('%s ../scripts/googlecode_upload.py -p houdini-ocean-toolkit -s "binary distribution" -u Drew.Whitehouse %s' % (python_exe,zipname))

@task
def upload_sdist():
    """uploads the source distribution to google code"""
    sh('%s ../scripts/googlecode_upload.py -p houdini-ocean-toolkit -s "source distribution" -u Drew.Whitehouse %s' % (python_exe,szipname()))

@task
def build_sop_cleave():
    hcustom('SOP_Cleave.C')

@task
def build_sop_ocean():
    hcustom('SOP_Ocean.C')

@task
def build_vex_ocean():
    hcustom('VEX_Ocean.C')

def soname(srcfile):
    return srcfile[:-2]+soext

def oname(srcfile):
    return srcfile[:-2]+oext

def hcustom(srcfile):
    """run hcustom on the srcfile, don't install the result"""
    path(oname(srcfile)).remove()
    path(soname(srcfile)).remove()
    sh('hcustom  -e %s %s  -i . %s' % (includes,libs,srcfile))
    assert path(oname(srcfile)).exists()
    assert path(soname(srcfile)).exists()


def zipper(dir, zip_file):
    zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
    root_len = len(os.path.abspath(dir))
    for root, dirs, files in os.walk(dir):
        for f in files:
            fullpath = os.path.join(root, f)
            zip.write(fullpath, fullpath, zipfile.ZIP_DEFLATED)
    zip.close()
    return zip_file

setup(
    name='The Houdini Ocean Toolkit',
    packages=[],
    version=release_version,
    author='Drew Whitehouse',
    author_email='Drew.Whitehouse@anu.edu.au')

