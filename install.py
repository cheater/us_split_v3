#!/usr/bin/env python

"""
NAME

us_split_v3
an xkb keyboard layout


ABOUT THIS PROGRAM

A keyboard layout for xkb. Geared specifically towards reducing RSI, this
layout is nearly identical to US-QWERTY, except there is a two-key split
between the T and Y columns into which symbols from the furthest right of
each row are placed. The hands can assume a more natural position two key
columns wider apart (similarly as with Dvorak) and hitting Enter is not an
exercise for contortionists any longer.

One of the problems with US-QWERTY is that the palm of the right hand needs
to move a lot -- especially bending in the wrist -- which can then lead to
Repetitive Strain Injury. If you spend a lot of time typing, you should be
aware of this, and should know that you might be hurting yourself with an
inappropriate keyboard layout. This layout makes it easy for people to try
out something new while mitigating many important issues.

The changes can be seen easily at the diagrams below:

Normal US-QWERTY:

    Esc  F1 ... F12

     ` 1 2 3 4 5 6 7 8 9 0 - = BBBB
    Tab q w e r t y u i o p [ ] RRR
    Caps a s d f g h j k l ; ' \ RR
    SS  < z x c v b n m , . / SSSSS
    CCC W AAA __________ AA MM CCCC


This layout:

    Caps F1 ... F12

     ` 1 2 3 4 5 - = 6 7 8 9 0 BBBB
    Tab q w e r t [ ] y u i o p RRR
    Esc  a s d f g \ ' h j k l ; RR
    SS L3 z x c v , . b n m / SSSSS
    CCC W AAA __________ AA AA CCCC

The shorthands are:

    S = Shift
    C = Control
    A = Alt
    W = Win key (Super key)
    M = Menu key
    R = Return key (Enter key)
    B = Backspace key
    _ = Space key
    L3 = ISO Level3 Shift (Alt Gr)

The symbol keys, which do not get typed very often, have been placed in the
middle. This is analogous to them being out of the reach of the right hand in
its normal position on the US QWERTY keyboard, except that this time they are
accessed using the much more dexterous index finger. Additionally, they are
shared with the left index finger, which as a practical outcome means that
the palms of the hand need to travel less and can in fact stay in their home
position most of the time, as most keys can be accessed by reaching out the
fingers. Additionally, this action of reaching out the fingers is completely
opposite to the movements that cause RSI, and stretches the muscle and
ligaments that get damaged by non-ergonomic layouts.

The symbol keys have been moved because in the US QWERTY layout they increase
the distance the right palm needs to travel in order for the typist to press
Backspace and Enter, which are very important and frequently typed keys. As
it is, the US QWERTY layout develops a habit in its users where they jerk the
palm of the right hand to the right after every finished sentence, creating a
very fast pathway towards RSI. There have been attempts to solve the problem
by using smaller keys for the right-hand-side symbols, as well as by making
the enter key bigger. Some of them have been partly successful, however none
of them was fixing the problem at its source, which is an inadequate layout.

The key between the left Shift and z is the 105th key. It exists on many
European keyboards and some people love it, while others hate it with
passion. The author has been a member of both groups. It is mapped as a
second Super key.

Caps Lock is placed where Esc was and Esc is placed where Caps Lock was. This
is hardcoded for now, but might be configurable in the future.

Naturally, this layout can be used in conjunction with GNOME's keyboard
layout options in order to turn the Caps Lock key into another Escape,
Control, Meta, or Compose key. The author uses it as Compose.


INSTALLATION

In order to install the layout in Ubuntu 10.04 and similar operating systems,
use the included install.py script which will complete the whole process. You
might need to execute it as a superuser. The installer should work in newer
Ubuntu versions, as well. However, it has not been tested with KDE or Unity,
and might not work in them. This version has only been tested with GNOME and
Ubuntu 10.04. Installation usually completes without restarting the X server.

In order to install on other systems, you might need to change the options of
the installer. See ./install.py --help for a description of the options. For
example, the xkb directory might have moved. You would search for a directory
called "xkb" with the subdirectories "rules" and "symbols", among others. You
might also need to change the name of the xml file. Normally, rules/evdev.xml
is used on Ubuntu 10.04, but it might be rules/xfree86.xml, rules/base.xml,
or rules/xorg.xml.

On some systems, lst files with the same base names are used instead of xml
files. Those files are not supported by the installer, however editing them
by hand is fairly easy; in the !layout section you would add the line:

        us_split_v3  USA Split v3

Next, you should copy the us_split_v3 file into the "symbols" subdirectory of
the xkb directory. A restart of your X server might now be required. That
should be all that is necessary; this installation procedure has, however, not
been tested.


USAGE

In order to use the layout, if you are in GNOME you would use the program
gnome-keyboard-properties(1) which can normally be accessed in the System
menu, Preferences submenu. Alternatively, it can be started from a terminal.

Once the Keyboard Properties are visible, you would select the Layouts tab,
where you would then click the Add button and navigate to the By Language
tab. In this tab, select English as the language and then find USA Split in
the Variants dropdown. Finally, click Add. You can then select the layout
from the list.


STABILITY

The layout may change (even drastically!) in the future. Older versions
should be available from the usual sources.


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

import os, sys, shutil

def add_xml(xml_file, symbols_file):
    """ Installs the data needed in the XML file so that X can find the layout.
        Should add something like the following under the layoutList element:

    <layout>
      <configItem>
        <name>us_split_v3</name>
        <shortDescription>U SA 3</shortDescription>
        <description>USA Split v3</description>
        <languageList><iso639Id>eng</iso639Id></languageList>
      </configItem>
    </layout>

        Adds it all on one line, if you care (or can't use the installer) then
        just copypaste it.
        """
    from xml.etree import ElementTree as ET
    se = ET.SubElement
    t = ET.parse(xml_file)
    for ll in [x for x in t.getroot().getchildren() if x.tag == 'layoutList']:
        # XML is ugly even if it's not XML.
        layout       = se( ll,        'layout'           )
        ci           = se( layout,    'configItem'       )
        name         = se( ci,        'name'             )
        name.text    =    symbols_file
        sdesc        = se( ci,        'shortDescription' )
        sdesc.text   =    'U_SA_3'
        desc         = se( ci,        'description'      )
        desc.text    =    'USA Split v3'
        langs        = se( ci,        'languageList'     )
        lang         = se( langs,     'iso639Id'         )
        lang.text    =    'eng'
        countries    = se( ci,        'countryList'      )
        country      = se( countries, 'iso3166Id'        )
        country.text =    'US'
    print 'Updating XML file: `%s\'' % (xml_file)
    t.write(xml_file)

def check_can_copy(source, target, what):
    errors = []
    if not os.path.exists(source):
        errors.append('Cannot find the %s file %s' % (what, source))
    target_dir = os.path.dirname(os.path.abspath(target))
    if not os.path.exists(target_dir):
        errors.append('Cannot find %s directory %s' % (what, target_dir))
    if not os.access(target_dir, os.W_OK):
        errors.append('Cannot write the %s directory %s' % (what, target_dir))
    return errors

def copy_file(source, target, what):
    """ Copies the file from source to target. Really just a wrapper.
        """
    print "Copying %s: `%s' -> `%s'" % (what, source, target)
    shutil.copyfile(source, target)

cache_dir = '/var/lib/xkb'

def delete_cache():
    import os
    for f in os.listdir(cache_dir):
        if 'xkm' == f.split('.')[-1]:
            full_path = os.path.join(cache_dir, f)
            print "Deleting cache: `%s'" % full_path
            os.unlink(full_path)

def install(
    dirname,
    symbols_source,
    symbols_dir,
    symbols_target_basename,
    xml_file_path,
    ):
    """ Copy symbols_file to symbols_dir and augument xml_file with the layout
        so that Gnome can find the layout.
        """

    errors = []


    # prepare stuff for copying the symbols file
    symbols_target = os.path.join(dirname, symbols_dir, symbols_target_basename)
    errors.extend(check_can_copy(
        symbols_source, symbols_target, 'symbols'
        ))

    # prepare stuff for copying the types file
    types_source = 'types-threelevelwithshift'
    types_target = os.path.join(dirname, 'types', 'threelevelwithshift')
    errors.extend(check_can_copy(
        types_source, types_target, 'types'
        ))

    # prepare stuff for copying the compat file
    compat_source = 'compat-threelevelwithshift'
    compat_target = os.path.join(dirname, 'compat', 'threelevelwithshift')
    errors.extend(check_can_copy(
        compat_source, compat_target, 'compat'
        ))

    # prepare stuff for installing metadata into the xml file
    xml_file = os.path.join(dirname, xml_file_path)
    if not os.path.exists(xml_file):
        errors.append('Cannot find evdev.xml file')
    if not os.access(xml_file, os.W_OK):
        errors.append('Cannot write to evdev.xml file')

    # check that you can delete the cache files
    if not os.access(cache_dir, os.W_OK):
        errors.append(
            'Cannot delete cache files: no write permission to %s' % cache_dir
            )

    if errors:
        print 'The installer cannot continue because it encountered the '\
            'following problems:'
        print '\n'.join(errors)
        return False

    copy_file(symbols_source, symbols_target, 'symbols')
    copy_file(types_source,   types_target,   'types'  )
    copy_file(compat_source,  compat_target,  'compat' )
    add_xml(xml_file, symbols_target_basename)
    delete_cache()
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
        help='use DIRNAME as the symbols target dir, default: `%s\'' % d,
        metavar='DIRNAME',
        default=d,
        )

    layout_name = 'us_split_v3'
    d = layout_name
    parser.add_option(
        '-n',
        '--symbols-target-basename',
        dest='symbols_target_basename',
        help='install layout as FILE, default: `%s\'' % d,
        metavar='FILE',
        default=d,
        )

    script_dir = os.path.dirname(sys.argv[0])
    d = os.path.normpath(
        os.path.join(script_dir, layout_name)
        )
    parser.add_option(
        '-f',
        '--symbols-source',
        dest='symbols_source',
        help='install layout from FILE, default: `%s\'' % d,
        metavar='FILE',
        default=d,
        )

    parser.add_option(
        '-C',
        '--only-delete-cache',
        dest='only_delete_cache',
        help='do not run installation, '\
            'only delete cache in %s/*.xkm' % cache_dir,
        default=False,
        action='store_true',
        )

    options = parser.parse_args()[0]
    if options.only_delete_cache:
        return delete_cache()
    else:
        d = options.__dict__
        d.pop('only_delete_cache', None)
        return install(**d)

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

