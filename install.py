#!/usr/bin/env python 

"""
NAME

us_split
an xkb keyboard layout


ABOUT THIS PROGRAM

A keyboard layout for xkb. Geared specifically towards reducing RSI,
this layout is nearly identical to QWERTY, except there is a two-key
split between the T and Y columns into which symbols from the furthest
right of each row are placed. This way, the hands can assume a more
natural position (sort of like with Dvorak) and hitting enter is not a
contortionist exercise any more.

The problem with QWERTY is, among others, that the right hand needs to
move a lot -- especially in the wrist -- which can lead to Repetitive
Strain Injury. If you spend a lot of time typing, you should be aware
of this and should know that you might be hurting yourself with an
inappropriate keyboard layout. This layout makes it easy for people to
try out something new, while alleviating some important issues.


The changes can be seen easily at the diagrams below:

Normal QWERTY:

     ` 1 2 3 4 5 6 7 8 9 0 - = Back
    Tab q w e r t y u i o p [ ] RRR
    Caps a s d f g h j k l ; ' \ RR
    Shf . z x c v b n m , . / Shift
    Ctr W Alt __________ Al RC Ctrl


This layout:

     ` 1 2 3 4 5 - = 6 7 8 9 0 BBBB
    Tab q w e r t [ ] y u i o p RRR
    Caps a s d f g \ ' h j k l ; RR
    SSS B z x c v , . b n m / SSSSS
    CCC W Alt __________ Al RC CCC

INSTALLATION

In order to install the layout under Ubuntu 10.04, use the included
install.py script which will take care of the rest. This should work
in newer versions as well, however has not been tested with the Unity
desktop or KDE and might not work in them. This version has only been
tested with GNOME under Ubuntu 10.04.

In order to install on other systems, you might need to change the
options of the installer. See ./install.py --help for a description of
the options. Specifically, the xkb directory might have moved. You are
searching for a directory called 'xkb' with subdirectories including
'rules' and 'symbols', as well as a few others. You might also need
to change the name of the xml file, normally rules/evdev.xml is used
on Ubuntu 10.04 but it might be rules/xfree86.xml or rules/base.xml
or rules/xorg.xml.

On some systems .lst files with the same base names are used instead.
Those files are not supported by the installer, however editing them by
hand should be fairly easy: in the !layout section you would add the line:

us_split  USA Split

Then, you should put the us_split file in the symbols/
subdirectory. Finally, a restart of your X server might be required. This
has, however, not been tested.


USAGE

In order to use the layout, under GNOME you would use the program
gnome-keyboard-properties(1) which can normally be accessed in the
System menu, Preferences submenu. Alternatively, it can be run from the
terminal. Then, in the Layouts tab, you would click the Add button and
navigate to the By Language tab. In this tab, select English as the
language and then find USA Split in the Variants dropdown. Finally,
click Add. You can then select the layout from the list.


STABILITY

Note that the layout may change (even drastically!) in the future. Older
versions should be available from the usual sources.


LICENSE

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, sys

def add_xml(xml_file, symbols_file):
    """ Installs the data needed in the XML file so that X can find the layout.
        Should add something like the following under the layoutList element:

    <layout>
      <configItem>
        <name>us_split</name>
        <shortDescription>U SA</shortDescription>
        <description>USA Split</description>
        <languageList><iso639Id>eng</iso639Id></languageList>
      </configItem>
      <variantList/>
    </layout>

        Adds it all on one line, if you care (or can't use the installer) then
        just copypaste it.
        """
    from xml.etree import ElementTree as ET
    se = ET.SubElement
    t = ET.parse(xml_file)
    for ll in [x for x in t.getroot().getchildren() if x.tag == 'layoutList']:
        # XML is ugly even if it's not XML.
        layout      =  se(ll,       'layout'            )
        vl          =  se(layout,   'variantList'       )
        ci          =  se(layout,   'configItem'        )
        name        =  se(ci,       'name'              )
        name.text   =     symbols_file
        sdesc       =  se(ci,       'shortDescription'  )
        sdesc.text  =     'U_SA'
        desc        =  se(ci,       'description'       )
        desc.text   =     'USA Split'
        langs       =  se(ci,       'languageList'      )
        lang        =  se(langs,    'iso639Id'          )
        lang.text   =     'eng'
    print 'Updating XML file: `%s\'' % (xml_file)
    t.write(xml_file)

def copy_symbols(source, target):
    """ Copies the symbols file from source to target. Really just a wrapper.
        """
    print "Copying `%s' -> `%s'" % (source, target)
    shutil.copyfile(source, target)

def install(
    dirname,
    symbols_source_name,
    symbols_dir,
    symbols_target_name,
    xml_file_path,
    ):
    """ Copy symbols_file to symbols_dir and augument xml_file with the layout
        so that Gnome can find the layout.
        """

    errors = []

    # prepare stuff for copying the symbols file
    target = os.path.join(dirname, symbols_dir, symbols_target_name)
    if not os.path.exists(symbols_source_name):
        errors.append('Cannot find the symbols file %s' % symbols_source_name)
    target_dir = os.path.dirname(os.path.abspath(target))
    if not os.path.exists(target_dir):
        errors.append('Cannot find symbols directory %s' % target_dir)
    if not os.access(target_dir, os.W_OK):
        errors.append('Cannot write to the symbols directory %s' % target_dir)

    # prepare stuff for installing metadata into the xml file
    xml_file = os.path.join(dirname, xml_file_path)
    if not os.path.exists(xml_file):
        errors.append('Cannot find evdev.xml file')
    if not os.access(xml_file, os.W_OK):
        errors.append('Cannot write to evdev.xml file')

    if errors:
        print 'The installer cannot continue because it encountered the '\
            'following problems:'
        print '\n'.join(errors)
        return False

    copy_symbols(symbols_source_name, target)
    add_xml(xml_file, symbols_target_name)
    return True

def main():
    """ Runs the script when it was called from the command line.
        """
    from optparse import OptionParser

    parser = OptionParser()
    d = '/usr/share/X11/xkb'
    parser.add_option(
        '-d',
        '--target-directory',
        dest='dirname',
        help='use DIRNAME as the xkb dir, default: `%s\'' % d,
        metavar='DIRNAME',
        default=d,
        )
    d = 'rules/evdev.xml'
    parser.add_option(
        '-x',
        '--xml-file',
        dest='xml_file_path',
        help='install layout metadata into FILE, default: `%s\'' % d,
        metavar='FILE',
        default=d,
        )
    d = 'symbols'
    parser.add_option(
        '-s',
        '--symbols-directory',
        dest='symbols_dir',
        help='use DIRNAME as the symbols dir, default: `%s\'' % d,
        metavar='DIRNAME',
        default=d,
        )
    d = 'us_split'
    parser.add_option(
        '-n',
        '--symbols-target-name',
        dest='symbols_target_name',
        help='install layout as FILE, default: `%s\'' % d,
        metavar='FILE',
        default=d,
        )
    d = 'us_split'
    parser.add_option(
        '-f',
        '--symbols-source-name',
        dest='symbols_source_name',
        help='install layout from FILE, default: `%s\'' % d,
        metavar='FILE',
        default=d,
        )

    options = parser.parse_args()[0]
    return install(**options.__dict__)

if '__main__' == __name__:
    try:
        ret = main()
        if ret:
            status = 0
        elif ret == False:
            status = 1
        else:
            status = 2
    except KeyboardInterrupt:
        status = 1
    sys.exit(status)

