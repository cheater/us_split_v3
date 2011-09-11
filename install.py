#!/usr/bin/env python 

import os, sys

def add_xml(xml_file):
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
        name.text   =     'us_split'
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

# {'symbols_dir': 'symbols', 'symbols_target_name': 'us_split', 'dirname':
# '/usr/share/X11/xkb', 'xml_file_path': 'rules/evdev.xml',
# 'symbols_source_name': 'us_split'}
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
    add_xml(xml_file)
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

    (options, args) = parser.parse_args()
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

