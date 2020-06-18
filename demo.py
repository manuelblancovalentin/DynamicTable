""" Import basic modules """
import sys, time
import numpy as np

""" Import DynamicTable """
from DynamicTable import DynamicTable

""" Init table """
header = ['Epoch','Progress','loss_labels']
formatters = {'Epoch':'{:03d}', 'Progress':'%$', 'loss_labels':'{:.3f}'}
progress_table = DynamicTable(header, formatters)

""" Print header """
progress_table.print_header()

""" Loop thru iters """
for i in range(5):
    time.sleep(1)
    for b in range(100):
        """ Perform some action here

            ...

        """
        time.sleep(.01)

        """ Get updated values to be set into table """
        vals = {'Epoch': i, 'Progress': b/99, 'loss_labels': 100*np.random.randn()}

        """ Update and print line """
        progress_table.update_line(vals, append = b == 99, print = True)

""" As we exit the loop, print the bottom of the table """
progress_table.print_bottom()
