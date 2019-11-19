# tixel_botter
Botting script for getting Tixel second hand tickets, written in Python, customisable

 - Notifications when a ticket is detected to have gone on sale for a particular event (no auto buying)
 - Customise refresh time, url, and search query
 - Logging and config file
 - No requirement for python installation

Source code can be found in the directory as **tixel_botter.py**, which will also work if all the dependencies are installed with your python installation.
**For non python users, run dist/tixel_botter/tixel_botter.exe.** This will generate a config file which can be used to customise running of the program, called **config.ini**.

Known errors:

 - alert may be sent if the ticket is sold privately and listed in the sell history of the page, or if a ticket gets pushes out of the sell history box. This is due to how the program detects page changes - it is not very smart. Should give a legitimate notification 70% of the time though at least.
