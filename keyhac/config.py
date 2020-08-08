import sys
import os
import datetime

import pyauto
from keyhac import *

def configure(keymap):

    # --------------------------------------------------------------------
    # Text editer setting for editting config.py file

    # Setting with program file path (Simple usage)
    if 1:
        keymap.editor = "notepad.exe"

    # Setting with callable object (Advanced usage)
    if 0:
        def editor(path):
            shellExecute( None, "notepad.exe", '"%s"'% path, "" )
        keymap.editor = editor

    # --------------------------------------------------------------------
    # Customizing the display

    # Font
    keymap.setFont( "MS Gothic", 20 )

    # Theme
    keymap.setTheme("black")

    # --------------------------------------------------------------------

    # Simple key replacement
    keymap.replaceKey( "LWin", 235 )
    keymap.replaceKey( "RWin", 255 )

    # User modifier key definition
    keymap.defineModifier( 235, "User0" )

    # Global keymap which affects any windows
    if 1:
        keymap_global = keymap.defineWindowKeymap()


    # Basic KeyBidings
    if 1:
        keymap_global[ "C-O" ]   = "243"   # Zenkaku-Hankaku
        keymap_global[ "C-A-O" ] = "243"   # Zenkaku-Hankaku
        keymap_global[ "C-A-G" ] = "W-G"   # Window Capture
        #keymap_global[ "C-A-L" ] = "W-L"   # Lock

        def istarget(window):
            if window.getProcessName() in ("Code.exe"):
                return False
            return True

        keymap_target = keymap.defineWindowKeymap( check_func = istarget )
        #keymap_edit = keymap.defineWindowKeymap( class_name="Edit" )
        keymap_edit = keymap_target

        keymap_edit[ "C-X" ] = keymap.defineMultiStrokeKeymap("C-X")

        keymap_edit[ "C-D" ] = "Delete"              # Delete
        keymap_edit[ "C-H" ] = "Back"                # Backspace
        keymap_edit[ "C-K" ] = "S-End","C-X"         # Removing following text

        keymap_edit[ "C-P" ] = "Up"                  # Move cursor up
        keymap_edit[ "C-N" ] = "Down"                # Move cursor downlll
        keymap_edit[ "C-F" ] = "Right"               # Move cursor right
        keymap_edit[ "C-B" ] = "Left"                # Move cursor left

        keymap_edit[ "C-A" ] = "Home"                # Move to beginning of line
        keymap_edit[ "C-E" ] = "End"                 # Move to end of line

        keymap_edit[ "A-F" ] = "C-Right"             # Word right
        keymap_edit[ "A-B" ] = "C-Left"              # Word left
        keymap_edit[ "A-N" ] = "PageDown"            # Page down
        keymap_edit[ "A-P" ] = "PageUp"              # Page up

        keymap_edit[ "A-Comma" ] = "C-Home"          # Beginning of the document
        keymap_edit[ "A-Period" ] = "C-End"          # End of the document

        keymap_edit[ "C-X" ][ "C-F" ] = "C-O"        # Open file
        keymap_edit[ "C-X" ][ "C-S" ] = "C-S"        # Save
        keymap_edit[ "C-X" ][ "C-W" ] = "A-F","A-A"  # Save as
        keymap_edit[ "C-X" ][ "C-C" ] = "A-F4"       # Exit

        keymap_edit[ "C-U" ]   = "C-Z"               # Undo
        keymap_edit[ "C-A-Y" ] = "C-Y"               # Redo

        keymap_edit[ "C-S" ] = "C-F"                 # Search
        keymap_edit[ "C-R" ] = "C-F"                 # Search
        keymap_edit[ "C-Q" ] = "C-H"                 # Replace
        keymap_edit[ "C-L" ] = "C-G"                 # Jump to specified line number

        keymap_edit[ "C-A-A" ] = "C-A"               # Select all
        keymap_edit[ "C-W" ] = "C-X","U-Shift"       # Cut
        keymap_edit[ "A-W" ] = "C-C","U-Shift"       # Copy
        keymap_edit[ "C-Y" ] = "C-V"                 # Paste

        keymap_edit[ "C-O" ]   = "243"               # Zenkaku-Hankaku
        keymap_edit[ "C-A-O" ] = "243"               # Zenkaku-Hankaku
        keymap_edit[ "C-A-P" ] = "C-P"               # Print
        keymap_edit[ "C-A-R" ] = "C-R"               # Update

        keymap_edit[ "C-Space" ] = "D-Shift"         # Select
        keymap_edit[ "C-G" ]     = "U-Shift"         # Release

        keymap_edit[ "C-A-D" ]           = "W-D"     # 
        keymap_edit[ "C-A-OpenBracket" ] = "W-Up"    # 
        keymap_edit[ "C-A-Slash" ]       = "W-Down"  # 
        keymap_edit[ "C-A-Colon" ]       = "W-Left"  # 
        keymap_edit[ "C-A-Doublequote" ] = "W-Right" # 

    # Application launcher using custom list window
    if 1:
        def command_PopWebpageList():

            # If the list window is already opened, just close it
            if keymap.isListWindowOpened():
                keymap.cancelListWindow()
                return

            def popWebpageList():

                websites1 = [
                    ( "  Google    ", keymap.ShellExecuteCommand( None, "https://www.google.co.jp/", "", "" ) ),
                    ( "  YouTube   ", keymap.ShellExecuteCommand( None, "https://www.youtube.com/", "", "" ) ),
                    ( "  Gmail     ", keymap.ShellExecuteCommand( None, "https://mail.google.com/mail/u/0/#inbox", "", "" ) ),
                ]
                websites2 = [
                    ( "  JMO       ", keymap.ShellExecuteCommand( None, "https://www.imojp.org/domestic/jmo_overview.html", "", "" ) ),
                    ( "  JJMO      ", keymap.ShellExecuteCommand( None, "https://www.imojp.org/domestic/jjmo_overview.html", "", "" ) ),
                    ( "  AoPS      ", keymap.ShellExecuteCommand( None, "https://artofproblemsolving.com/community/c13_contests", "", "" ) ),
                ]
                websites3 = [
                    ( "  Twitter   ", keymap.ShellExecuteCommand( None, "https://twitter.com/home", "", "" ) ),
                    ( "  note      ", keymap.ShellExecuteCommand( None, "https://note.com/sitesettings/stats", "", "" ) ),
                    ( "  studytube ", keymap.ShellExecuteCommand( None, "https://studytube.info/", "", "" ) ),
                    ( "  yutura    ", keymap.ShellExecuteCommand( None, "https://ytranking.net/channel/21278/", "", "" ) ),
                ]

                listers = [
                    ( "[Web] General", cblister_FixedPhrase(websites1) ),
                    ( "[Web] Math   ", cblister_FixedPhrase(websites2) ),
                    ( "[Web] Ads    ", cblister_FixedPhrase(websites3) ),

                ]

                item, mod = keymap.popListWindow(listers)

                if item:
                    item[1]()

            # Because the blocking procedure cannot be executed in the key-hook,
            # delayed-execute the procedure by delayedCall().
            keymap.delayedCall( popWebpageList, 0 )


        #keymap_global[ "C-A-W" ] = command_PopDirectoryList
        keymap_global[ "C-A-S" ] = command_PopWebpageList

        vscode = "C:\\Users\\T\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        keymap_global[ "C-A-V" ] = keymap.ShellExecuteCommand( None, vscode, "", "" )


    # Customizing clipboard history list
    if 1:
        # Enable clipboard monitoring hook (Default:Enabled)
        keymap.clipboard_history.enableHook(True)

        # Maximum number of clipboard history (Default:1000)
        keymap.clipboard_history.maxnum = 1000

        # Total maximum size of clipboard history (Default:10MB)
        keymap.clipboard_history.quota = 10*1024*1024

        # Fixed phrases
        fixed_items = [
            ( "name@server.net",     "name@server.net" ),
            ( "Address",             "San Francisco, CA 94128" ),
            ( "Phone number",        "03-4567-8901" ),
        ]

        # Return formatted date-time string
        def dateAndTime(fmt):
            def _dateAndTime():
                return datetime.datetime.now().strftime(fmt)
            return _dateAndTime

        # Date-time
        datetime_items = [
            ( "YYYY/MM/DD HH:MM:SS",   dateAndTime("%Y/%m/%d %H:%M:%S") ),
            ( "YYYY/MM/DD",            dateAndTime("%Y/%m/%d") ),
            ( "HH:MM:SS",              dateAndTime("%H:%M:%S") ),
            ( "YYYYMMDD_HHMMSS",       dateAndTime("%Y%m%d_%H%M%S") ),
            ( "YYYYMMDD",              dateAndTime("%Y%m%d") ),
            ( "HHMMSS",                dateAndTime("%H%M%S") ),
        ]

        # Add quote mark to current clipboard contents
        def quoteClipboardText():
            s = getClipboardText()
            lines = s.splitlines(True)
            s = ""
            for line in lines:
                s += keymap.quote_mark + line
            return s

        # Indent current clipboard contents
        def indentClipboardText():
            s = getClipboardText()
            lines = s.splitlines(True)
            s = ""
            for line in lines:
                if line.lstrip():
                    line = " " * 4 + line
                s += line
            return s

        # Unindent current clipboard contents
        def unindentClipboardText():
            s = getClipboardText()
            lines = s.splitlines(True)
            s = ""
            for line in lines:
                for i in range(4+1):
                    if i>=len(line) : break
                    if line[i]=='\t':
                        i+=1
                        break
                    if line[i]!=' ':
                        break
                s += line[i:]
            return s

        full_width_chars = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！”＃＄％＆’（）＊＋，−．／：；＜＝＞？＠［￥］＾＿‘｛｜｝～０１２３４５６７８９　"
        half_width_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}～0123456789 "

        # Convert to half-with characters
        def toHalfWidthClipboardText():
            s = getClipboardText()
            s = s.translate(str.maketrans(full_width_chars,half_width_chars))
            return s

        # Convert to full-with characters
        def toFullWidthClipboardText():
            s = getClipboardText()
            s = s.translate(str.maketrans(half_width_chars,full_width_chars))
            return s

        # Save the clipboard contents as a file in Desktop directory
        def command_SaveClipboardToDesktop():

            text = getClipboardText()
            if not text: return

            # Convert to utf-8 / CR-LF
            utf8_bom = b"\xEF\xBB\xBF"
            text = text.replace("\r\n","\n")
            text = text.replace("\r","\n")
            text = text.replace("\n","\r\n")
            text = text.encode( encoding="utf-8" )

            # Save in Desktop directory
            fullpath = os.path.join( getDesktopPath(), datetime.datetime.now().strftime("clip_%Y%m%d_%H%M%S.txt") )
            fd = open( fullpath, "wb" )
            fd.write(utf8_bom)
            fd.write(text)
            fd.close()

            # Open by the text editor
            keymap.editTextFile(fullpath)

        # Menu item list
        other_items = [
            ( "Quote clipboard",            quoteClipboardText ),
            ( "Indent clipboard",           indentClipboardText ),
            ( "Unindent clipboard",         unindentClipboardText ),
            ( "",                           None ),
            ( "To Half-Width",              toHalfWidthClipboardText ),
            ( "To Full-Width",              toFullWidthClipboardText ),
            ( "",                           None ),
            ( "Save clipboard to Desktop",  command_SaveClipboardToDesktop ),
            ( "",                           None ),
            ( "Edit config.py",             keymap.command_EditConfig ),
            ( "Reload config.py",           keymap.command_ReloadConfig ),
        ]

        # Clipboard history list extensions
        keymap.cblisters += [
            ( "Fixed phrase", cblister_FixedPhrase(fixed_items) ),
            ( "Date-time", cblister_FixedPhrase(datetime_items) ),
            ( "Others", cblister_FixedPhrase(other_items) ),
        ]

