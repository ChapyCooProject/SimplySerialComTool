Simple Serial Communication Software (Japanese Edition)
=======================================================

Development Environment
-----------------------

   * Python 3.8
   * Tkinter
   * Pyinstaller
   * Windows 10 64-bit

Introduction
------------

   * This software is a basic tool for serial communication testing.
   * No installation is required; it runs as a standalone executable.
   * It is compatible with 64-bit versions of Windows; it will not run on 32-bit versions.

About the Executable File
-------------------------

   * The executable file is located in the "exe" folder.
     The filename is "SimpleSerialCommunicationSoftware.exe".

Usage (Serial Communication Connection)
---------------------------------------

   1. Launch the executable file "SimpleSerialCommunicationSoftware.exe".
   2. Configure the settings in the "Communication Settings" at the top left of the screen, then click the "Connect" button.
   3. In the "Flow Control & Monitor" section at the top left of the screen, you can confirm the connection status.

Usage (Serial Communication Disconnection and Exit)
---------------------------------------------------

   1. Click the "Disconnect" button in the "Communication Settings" at the top left of the screen.
   2. Click "Exit" at the top left of the screen.

Usage (Serial Communication - Server Send/Receive Mode)
-------------------------------------------------------

   1. Enter the data you want to send in the "Send Data" text box at the top right of the screen. (Multiple lines possible)
   2. Click the "[SV] Start Listening" button to begin the server send/receive mode.
   3. In this mode, each click of the "[SV] Send Data" button will send the data from the "Send Data" box line by line.
   4. When the last line of data is sent, a message indicating completion will be displayed.
   5. Click the "[SV] Stop Listening" button to end the server send/receive mode.

Usage (Serial Communication - Client Send Mode)
-----------------------------------------------

   1. Enter the data you want to send in the "Send Data" text box at the top right of the screen. (Multiple lines possible)
   2. Set the "Data Send Method" in the bottom left corner of the screen.
      - [Send the entire text at once]
        - Send the content of the "Send Data" text box all at once.
      - [Send one line of text at a time]
        - If "ACK" or "NAK" is received from the other party, automatically send the next line of data.
        - Send data automatically at specified time intervals.
   3. Click the "[CL] Send Data" button to send the data according to the configured method.

Notes on Data Transmission
--------------------------

   * Line breaks in the "Send Data" text box will not be transmitted.
     If you want to transmit line breaks, include "\<CR\>\<LF\>" or similar in the message.
   * When using control codes, represent them in bracketed characters.
     The supported control codes are as follows:

      - 0x00:\<NUL\>
      - 0x01:\<SOH\>
      - 0x02:\<STX\>
      - 0x03:\<ETX\>
      - 0x04:\<EOT\>
      - 0x05:\<ENQ\>
      - 0x06:\<ACK\>
      - 0x07:\<BEL\>
      - 0x08:\<BS\>
      - 0x09:\<HT\>
      - 0x0A:\<LF\>
      - 0x0B:\<VT\>
      - 0x0C:\<FF\>
      - 0x0D:\<CR\>
      - 0x0E:\<SO\>
      - 0x0F:\<SI\>
      - 0x10:\<DLE\>
      - 0x11:\<DC1\>
      - 0x12:\<DC2\>
      - 0x13:\<DC3\>
      - 0x14:\<DC4\>
      - 0x15:\<NAK\>
      - 0x16:\<SYN\>
      - 0x17:\<ETB\>
      - 0x18:\<CAN\>
      - 0x19:\<EM\>
      - 0x1A:\<SUB\>
      - 0x1B:\<ESC\>
      - 0x1C:\<FS\>
      - 0x1D:\<GS\>
      - 0x1E:\<RS\>
      - 0x1F:\<US\>
      - 0x7F:\<DEL\>

Downloading the Executable File
-------------------------------

   * The executable file can be downloaded from the following URL.

      - [Download](https://drive.google.com/drive/folders/1UGaaVB4WEtTmSkVfm9mhlPtAWaU0CFEB?usp=sharing)

