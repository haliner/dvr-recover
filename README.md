DVR-RECOVER
===========

Description
-----------

dvr-recover is an incredible Python-powered project helping you to recover
recordings of digital video recorders. In other words: The script is able to
find video files on the surface of the device's hard disk drive.

Practically, the process is much more complex. Have a look at the following
sections if you want to gain more knowledge about the details.

There are many devices on the market, not all models can be supported. See the
list of tested devices to see if your device has been already tested.


License
-------

> Copyright (C) 2010, 2011 Stefan Haller <haliner@gmail.com>
>
> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License
> along with this program.  If not, see <http://www.gnu.org/licenses/>.


Tested Devices
--------------

Currently only Panasonic DMR devices have been tested. If you successfully
recovered the content of your drive (completely or partly), please drop me a
mail!

Working devices:

 *  Panasonic DMR-EH55
 *  Panasonic DMR-EH56
 *  Panasonic DMR-EH57
 *  Panasonic DMR-EX77
 *  Panasonic DMR-EX80S
 *  Panasonic DMR-EX85
 *  Panasonic DMR-XW300
 *  Panasonic DVM-E80H
 *  Pioneer DVR-433H


System Requirements
-------------------

To run the script you need a Python interpreter (2.x, tested with 2.5 and
higher).


Usage
-----

If you execute the script without any parameters, the script will print the
usage message where all parameters, switches and settings are explained in
detail.

Executing the script is very easy: Simply open a terminal (on Windows: [Win] +
[R] -> enter "cmd" and press enter). At first you have to switch to the
directory where the script is located and then you can fire up the Python
interpreter.

Linux:

    cd /path/to/script/
    python dvr-recover.py [parameters]

Windows:

    cd C:\Path\to\script\
    python dvr-recover.py [parameters]



Guide
-----

This section will guide you through the complete process of recovering the data
from you hard disk drive.

Naturally the hard disk drive of the digital video recorder must be plugged
into the computer. So you need to open the device and fetch the hdd. You can
either attach the disk directly to the IDE ports of your motherboard or you can
use a IDE-USB-bridge.

It's recommended that you create an image of your disk, but if you think you're
lucky you can even use the hard disk drive directly as input on Linux. Note
that direct access to the hard disk drive on Windows is currently not supported
by dvr-recover. On Windows you have to use 3rd party programs to create the
image. On Linux you can use the standard tools (be sure that you have root
permissions):

    # (Assuming that your disc is labeled /dev/sdb)
    dd if=/dev/sdb of=disk.img bs=10M

This guide assumes that you have an exact bitwise copy of the hdd on your file
system. Note that it's also possible to split your image into smaller parts.
The script is able to handle this situation correctly. But you have to be sure
that you specify all parts in the correct order in the later process. If you
want to use the hdd directly, you will need to substitute the filenames in this
guide with the device identifier (/dev/sdb, ... on Linux).

The script will automatically create a sqlite3 database to store all settings
and gained information. If somethings goes heavily wrong, you will be able to
reset the state of the program by deleting the database. To do so delete the
file "dvr-recover.sqlite" in the working directory of the script.

Before you the script can analyze your hard disk drive, you have to go through
a initial setup first. The script needs at least the information about the
input filename(s). But there are many other settings to tweak -- most of them
have sensible default values. For more information read the usage message of
the script by passing "usage" as parameter.

If you call the script with passing "setup" as parameter, it will print the
current values of all settings:

    $ python dvr-recover.py setup
    input_file: /home/user/disk.img.0001
    [...]
    input_file: /home/user/disk.img.9999
    export_dir: /tmp/export
    blocksize: 2048
    min_chunk_size: 25600
    max_create_gap: 90000
    max_sort_gap: 90000

To change a setting you have to pass the "setup" parameter and additionally the
setting to change with the new value:

    $ python dvr-recover.py setup blocksize 2048

The only exception is the handling of input files:

    $ python dvr-recover.py setup input clear
    $ python dvr-recover.py setup input add disk.img.0001
    $ python dvr-recover.py setup input add disk.img.0002
    $ python dvr-recover.py setup input del disk.img.0001
    $ [and so on...]

Use the parameter "clear" to clear the list of input files. Also available are
the parameters "add" and "del" -- both take a filename as argument.

If you want to reset all settings, you have to use the parameter "reset":

    $ python dvr-recover.py setup reset

Now you should be able to start the main feature of the script: recovering your
hard disk drive.

At first let the script analyze your hard disk drive. Call the script with
passing the parameter "create". This process will take quite a long time to
complete. You can interrupt the process at any point by pressing [CTRL] + [C].
On the next call with the parameter "create" the script will automatically
resume the process where it was interrupted.

    $ python dvr-recover.py create
    [ 29.5%] 297457/1006929 blocks (9915.2 bl/s; 19.4 MiB/s): 5 chunks
    [ 65.0%] 654794/1006929 blocks (11911.2 bl/s; 23.3 MiB/s): 6 chunks
    [ 91.3%] 918841/1006929 blocks (8786.1 bl/s; 17.2 MiB/s): 6 chunks

    Finished.
    Read 1006929 of 1006929 blocks.
    Found 7 chunks.
    Took 100.97 seconds.
    Average speed was 9972.6 blocks/s (19.5 MiB/s).

(The file used for generating the output above was very very small.)

After finishing the analyze of the hdd the script will forbid all further calls
with the parameter "create", because this would cause data loss (all data of
the last analyze would be reseted first). You must explicitly reset the
information in the database by passing the parameter "clear":

    $ python dvr-recover.py clear

**(THIS WILL DELETE ALL GATHERED DATA FROM THE DATABASE!)**

dvr-recover has the ability to sort the chunks and find chunks of the same
recording. To start this process pass the paremter "sort" to the script:

    $ python dvr-recover.py sort

To revert the effect of "sort", pass "reset".

    $ python dvr-recover.py reset

At every stage you can display the chunk info by passing "show".

    $ python dvr-recover.py show
    ----+--------------+--------------+--------------+--------------+------------
        |  Block Start |   Block Size |  Clock Start |    Clock End | Concatenate
    ----+--------------+--------------+--------------+--------------+------------
      1 |       391379 |       615548 |    250031969 |    402836926 |     False
      2 |       223188 |       168189 |    401478251 |    484558534 |     False
      3 |       107989 |       115197 |    546892241 |    592303341 |     False
      4 |        80992 |        26995 |   1085209725 |   1100156779 |     False
      # |        53995 |        26995 |   1100157071 |   1115282776 |      True
      # |        26998 |        26995 |   1115283069 |   1129877061 |      True
      # |            0 |        26996 |   1129877208 |   1144930337 |      True

In the first column you can see the index of the chunk. A '#' is printed if the
chunk is concatenated to the previous one.

The last thing is exporting the recordings. If the scrit has found chunks of
the same recording, they will be automatically concatenated. You can either
export all recordings in the database or only a single one.

    $ python dvr-recover.py export

This will export all recordings. You can also specify a chunk id to export. In
this example the script would export only the chunk with the id 4 (including
the chunks which should be concatenated to this one).

    $ python dvr-recover.py export 4

All the basics are explained -- you should be able to use the script now. Of
course, there are a lot of other things that were not mentioned in this guide.
For more details have a look at the usage message or the source code.


Tuning the parameters
---------------------

Is there any possibility to tune the script and recover more files? Yes, it is!

You can tune the process of chunk detection with parameters. The most important
parameter is "min_chunk_size". The smaller the value is, the more the script
finds. But the problem is that the possibility to find "garbage" is even
higher.

The default setting is that the program ignores chunks smaller than 50 MB
(25600 blocks). If you set it to 0, the script will find everything, even if
it's only one frame of a recording. If you play a bit with this parameter you
maybe will recover more recordings completely.

*IMPORTANT*: After changing the parameters run the complete scan again
(parameter "create")!

To change the setting run:

    $ python dvr-recover.py setup min_chunk_size [NEW_VALUE]

[NEW_VALUE] must be given in blocks. Blocks * blocks size = size in byte. The
default block size is 2048 byte.

I tried to set the default value to a sensible default. If somebody can prove
that a smaller value is better, I'll set the default value for later releases
to a lower value.


Homepage and Contact
--------------------

Stefan Haller <haliner@gmail.com>

https://github.com/haliner/dvr-recover

Feel free to contact me if you have any additional suggestions or you've
found a bug. Feedback is always welcome! IF YOU THINK THE SCRIPT IS TERRIFIC,
I WOULD BE VERY GLAD IF YOU LET ME KNOW THAT.
