#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# UnknownBible.py
#   Last modified: 2013-07-07 (also update ProgVersion below)
#
# Module handling a unknown Bible object
#
# Copyright (C) 2013 Robert Hunt
# Author: Robert Hunt <robert316@users.sourceforge.net>
# License: See gpl-3.0.txt
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Module handling an unknown Bible object.

Given a folder name, analyses the files in it
    and tries to determine what type of Bible it probably contains (if any).

Currently aware of the following Bible types:
    USFM
    Unbound Bible (table based), TheWord (line based), MySword (SQLite3 based)
    OSIS, USX, OpenSong, Zefania (all XML)
    Sword modules (binary).
"""

ProgName = "Unknown Bible object handler"
ProgVersion = "0.04"
ProgNameVersion = "{} v{}".format( ProgName, ProgVersion )


import logging, os.path
from gettext import gettext as _

import Globals
from USFMFilenames import USFMFilenames
from USXFilenames import USXFilenames

from USFMBible import USFMBibleFileCheck, USFMBible
from USXXMLBible import USXXMLBibleFileCheck, USXXMLBible
from OpenSongXMLBible import OpenSongXMLBibleFileCheck, OpenSongXMLBible
from OSISXMLBible import OSISXMLBibleFileCheck, OSISXMLBible
from ZefaniaXMLBible import ZefaniaXMLBibleFileCheck, ZefaniaXMLBible
from UnboundBible import UnboundBibleFileCheck, UnboundBible
from TheWordBible import TheWordBibleFileCheck, TheWordBible
from MySwordBible import MySwordBibleFileCheck, MySwordBible
#from SwordResources import SwordInterface



class UnknownBible:
    """
    Class for handling an entire Bible.
    """

    def __init__( self, givenFolderName ):
        """
        Constructor: creates an empty Bible object.
        """
        if Globals.debugFlag: assert( givenFolderName and isinstance( givenFolderName, str ) )
        self.givenFolderName = givenFolderName

        # Check that the given folder is readable
        if not os.access( givenFolderName, os.R_OK ):
            logging.critical( _("UnknownBible: Given '{}' folder is unreadable").format( self.givenFolderName ) )

        self.foundType = None
    # end of UnknownBible.__init__


    def __str__( self ):
        """
        This method returns the string representation of a Bible.

        @return: the name of a Bible object formatted as a string
        @rtype: string
        """
        result = _("Unknown Bible object")
        result += ('\n' if result else '') + "  " + _("Folder: {} ").format( self.givenFolderName )
        if self.foundType: result += ('\n' if result else '') + "  " + _("Type: {} ").format( self.foundType )
        return result
    # end of UnknownBible.__str__


    def search( self, strictCheck=True, autoLoad=False ):
        """
        Search our folder to found what if any Bible versions can be found.

        These searches are best done in a certain order to avoid false detections.
        """
        totalBibleCount, totalBibleTypes, typesFound = 0, 0, []

        # Search for TheWord Bibles
        TheWordBibleCount = TheWordBibleFileCheck( self.givenFolderName, strictCheck=strictCheck )
        if TheWordBibleCount:
            totalBibleCount += TheWordBibleCount
            totalBibleTypes += 1
            typesFound.append( 'TheWord' )
            if Globals.verbosityLevel > 2: print( "TheWordBible.search: TheWordBibleCount", TheWordBibleCount )

        # Search for MySword Bibles
        MySwordBibleCount = MySwordBibleFileCheck( self.givenFolderName, strictCheck=strictCheck )
        if MySwordBibleCount:
            totalBibleCount += MySwordBibleCount
            totalBibleTypes += 1
            typesFound.append( 'MySword' )
            if Globals.verbosityLevel > 2: print( "MySwordBible.search: MySwordBibleCount", MySwordBibleCount )

        # Search for Unbound Bibles
        UnboundBibleCount = UnboundBibleFileCheck( self.givenFolderName, strictCheck=strictCheck )
        if UnboundBibleCount:
            totalBibleCount += UnboundBibleCount
            totalBibleTypes += 1
            typesFound.append( 'Unbound' )
            if Globals.verbosityLevel > 2: print( "UnknownBible.search: UnboundBibleCount", UnboundBibleCount )

        # Search for USFM Bibles
        USFMBibleCount = USFMBibleFileCheck( self.givenFolderName, strictCheck=strictCheck )
        if USFMBibleCount:
            totalBibleCount += USFMBibleCount
            totalBibleTypes += 1
            typesFound.append( 'USFM' )
            if Globals.verbosityLevel > 2: print( "UnknownBible.search: USFMBibleCount", USFMBibleCount )

        # Search for USX XML Bibles
        USXBibleCount = USXXMLBibleFileCheck( self.givenFolderName, strictCheck=strictCheck )
        if USXBibleCount:
            totalBibleCount += USXBibleCount
            totalBibleTypes += 1
            typesFound.append( 'USX' )
            if Globals.verbosityLevel > 2: print( "UnknownBible.search: USXBibleCount", USXBibleCount )

        # Search for OSIS XML Bibles
        OSISBibleCount = OSISXMLBibleFileCheck( self.givenFolderName, strictCheck=strictCheck )
        if OSISBibleCount:
            totalBibleCount += OSISBibleCount
            totalBibleTypes += 1
            typesFound.append( 'OSIS' )
            if Globals.verbosityLevel > 2: print( "UnknownBible.search: OSISBibleCount", OSISBibleCount )

        # Search for OpenSong XML Bibles
        OpenSongBibleCount = OpenSongXMLBibleFileCheck( self.givenFolderName, strictCheck=strictCheck )
        if OpenSongBibleCount:
            totalBibleCount += OpenSongBibleCount
            totalBibleTypes += 1
            typesFound.append( 'OpenSong' )
            if Globals.verbosityLevel > 2: print( "UnknownBible.search: OpenSongBibleCount", OpenSongBibleCount )

        # Search for Zefania XML Bibles
        ZefaniaBibleCount = ZefaniaXMLBibleFileCheck( self.givenFolderName, strictCheck=strictCheck )
        if ZefaniaBibleCount:
            totalBibleCount += ZefaniaBibleCount
            totalBibleTypes += 1
            typesFound.append( 'Zefania' )
            if Globals.verbosityLevel > 2: print( "UnknownBible.search: ZefaniaBibleCount", ZefaniaBibleCount )


        assert( len(typesFound) == totalBibleTypes )
        if totalBibleCount == 0:
            if Globals.verbosityLevel > 0: print( "UnknownBible.search: No Bibles found" )
            self.foundType = 'None found'
        elif totalBibleCount > 1:
            if totalBibleTypes == 1:
                if Globals.verbosityLevel > 0:
                    print( "UnknownBible.search: Multiple ({}) {} Bibles found".format( totalBibleCount, typesFound[0] ) )
            else:
                if Globals.verbosityLevel > 0:
                    print( "UnknownBible.search: Multiple ({}) Bibles found: {}".format( totalBibleCount, typesFound ) )
                self.foundType = 'Many found'

        elif TheWordBibleCount == 1:
            self.foundType = "TheWord Bible"
            if autoLoad: return TheWordBibleFileCheck( self.givenFolderName, strictCheck=strictCheck, autoLoad=autoLoad )
            else: return self.foundType, TheWordBibleCount
        elif MySwordBibleCount == 1:
            self.foundType = "MySword Bible"
            if autoLoad: return MySwordBibleFileCheck( self.givenFolderName, strictCheck=strictCheck, autoLoad=autoLoad )
            else: return self.foundType, MySwordBibleCount
        elif UnboundBibleCount == 1:
            self.foundType = "Unbound Bible"
            if autoLoad: return UnboundBibleFileCheck( self.givenFolderName, strictCheck=strictCheck, autoLoad=autoLoad )
            else: return self.foundType, UnboundBibleCount
        elif USFMBibleCount == 1:
            self.foundType = "USFM Bible"
            if autoLoad: return USFMBibleFileCheck( self.givenFolderName, strictCheck=strictCheck, autoLoad=autoLoad )
            else: return self.foundType, USFMBibleCount
        elif USXBibleCount == 1:
            self.foundType = "USX XML Bible"
            if autoLoad: return USXXMLBibleFileCheck( self.givenFolderName, strictCheck=strictCheck, autoLoad=autoLoad )
            else: return self.foundType, USXBibleCount
        elif OSISBibleCount == 1:
            self.foundType = "OSIS XML Bible"
            if autoLoad: return OSISXMLBibleFileCheck( self.givenFolderName, strictCheck=strictCheck, autoLoad=autoLoad )
            else: return self.foundType, OSISBibleCount
        elif OpenSongBibleCount == 1:
            self.foundType = "OpenSong XML Bible"
            if autoLoad: return OpenSongXMLBibleFileCheck( self.givenFolderName, strictCheck=strictCheck, autoLoad=autoLoad )
            else: return self.foundType, OpenSongBibleCount
        elif ZefaniaBibleCount == 1:
            self.foundType = "Zefania XML Bible"
            if autoLoad: return ZefaniaXMLBibleFileCheck( self.givenFolderName, strictCheck=strictCheck, autoLoad=autoLoad )
            else: return self.foundType, ZefaniaBibleCount
    # end of UnknownBible.search
# end of class UnknownBible



def demo():
    """
    Main program to handle command line parameters and then run what they want.
    """
    if Globals.verbosityLevel > 0: print( "{} V{}".format(ProgName, ProgVersion ) )

    # Now demo the class
    testFolders = ( "/home/robert/Logs",
                    "../../../../../Data/Work/Bibles/TheWord modules/",
                    "../../../../../Data/Work/Bibles/Biola Unbound modules/",
                    "../../../../../Data/Work/Bibles/OpenSong Bibles/",
                    "../../../../../Data/Work/Bibles/Zefania modules/",
                    "../../../../../Data/Work/Matigsalug/Bible/MBTV/",
                    "../../../../../SSD/AutoProcesses/Processed/",
                    "Tests/DataFilesForTests/USFMTest1/", "Tests/DataFilesForTests/USFMTest2/",
                    "Tests/DataFilesForTests/USXTest1/", "Tests/DataFilesForTests/USXTest2/",
                    "Tests/DataFilesForTests/OSISTest1/", "Tests/DataFilesForTests/OSISTest2/",
                    "Tests/DataFilesForTests/ZefaniaTest/",
                    "Tests/DataFilesForTests/TheWordTest/",
                    "Tests/DataFilesForTests/MySwordTest/",
                    "Tests/DataFilesForTests/", # Up a level
                    )
    if 1: # Just find the files
        for j, testFolder in enumerate( testFolders ):
            if Globals.verbosityLevel > 0: print( "\n\nA{}/ Trying {}...".format( j+1, testFolder ) )
            B = UnknownBible( testFolder )
            #print( B )
            result = B.search( autoLoad=False )
            #result2 = B.search( autoLoad=True ) if result1 else None
            if Globals.verbosityLevel > 2: print( "  Result is: {}".format( result ) )
            if Globals.verbosityLevel > 0: print( B )

    if 1: # Just load the files
        for j, testFolder in enumerate( testFolders ):
            if Globals.verbosityLevel > 0: print( "\n\nB{}/ Loading {}...".format( j+1, testFolder ) )
            B = UnknownBible( testFolder )
            #print( B )
            #result1 = B.search( autoLoad=False )
            result = B.search( autoLoad=True )
            if Globals.verbosityLevel > 2: print( "  Result is: {}".format( result ) )
            if Globals.verbosityLevel > 0: print( B )

    if 1: # Load, check, and export the files
        for j, testFolder in enumerate( testFolders ):
            if Globals.verbosityLevel > 0: print( "\n\nC{}/ Processing {}...".format( j+1, testFolder ) )
            B = UnknownBible( testFolder )
            #print( B )
            result = B.search( autoLoad=True )
            #result2 = B.search( autoLoad=True ) if result1 else None
            #if Globals.verbosityLevel > 2: print( "  Results are: {} and {}".format( result1, result2 ) )
            if Globals.verbosityLevel > 0: print( B )
            if result:
                result.check()
                results = result.doAllExports()
                if Globals.verbosityLevel > 2: print( "  Results are: {}".format( results ) )
# end of demo

if __name__ == '__main__':
    # Configure basic set-up
    parser = Globals.setup( ProgName, ProgVersion )
    Globals.addStandardOptionsAndProcess( parser )

    demo()

    Globals.closedown( ProgName, ProgVersion )
# end of UnknownBible.py