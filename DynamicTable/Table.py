# -*- coding: utf-8 -*-
"""
Created on Sun May 5 09:57:22 2013

@author: Manu Blanco Valentín
@email: manuel.blanco.valentin@gmail.com
@github: github.com/manuelblancovalentin

"""

""" Basic modules """
import numpy as np


""" Printable Table used for several purposes, such as showing progress during training 
    HOW TO USE SNIPPET:
        header = ['Epoch','Progress','loss_labels']
        formatters = {'Epoch':'{:03d}', 'Progress':'%$', 'loss_labels':'{:3f}'}
        progress_table = Printable_Table(header, formatters)
        import sys, time
        ### Print header
        sys.stdout.write(progress_table.header)
        sys.stdout.flush()
        for i in range(5):
            time.sleep(1)
            for b in range(100):
                time.sleep(.01)
                vals = {'Epoch': i, 'Progress': b/99, 'loss_labels': 100*np.random.randn()}
                line = progress_table.update_line(vals, append = b == 99)
                if b != 99:
                    sys.stdout.write(line + '\r')
                else:
                    sys.stdout.write(line + '\n')
        ### Print bottom of the table
        sys.stdout.write(progress_table.bottom_border + '\n')
"""
class DynamicTable(object):
    def __init__(self, header, formatters=None, column_width='auto', column_ratio=1.):
        """."""
        """ Forward compat """
        super().__init__()

        """ calculate each column size """
        self.entries = header
        self.formatters = formatters if formatters is not None else {xn: '{}' for xn in self.entries}

        """ Make sure column_ratio is a dict """
        if not hasattr(column_ratio,'__len__'):
            column_ratio = [column_ratio]*len(self.entries)
        if isinstance(column_ratio,list):
            if len(column_ratio) > len(self.entries):
                column_ratio = column_ratio[:len(self.entries)]
            elif len(column_ratio) < len(self.entries):
                column_ratio = column_ratio + [1]*(len(self.entries) - len(column_ratio))
            """ make dict """
            column_ratio = {xn: cr for (xn,cr) in zip(self.entries,column_ratio)}
        """ Assert we have all entries in column_ratio """
        column_ratio = {xn: column_ratio[xn] if xn in column_ratio else 1 for xn in self.entries}
        self.column_ratio = column_ratio

        """ Make sure column_width is a dict """
        if isinstance(column_width,str):
            column_width = [column_width]*len(self.entries)
        if isinstance(column_width,list):
            if len(column_width) > len(self.entries):
                column_width = column_width[:len(self.entries)]
            elif len(column_width) < len(self.entries):
                column_width = column_width + ['auto']*(len(self.entries) - len(column_width))
            """ make dict """
            column_width = {xn: cr for (xn,cr) in zip(self.entries,column_width)}
        """ Assert we have all entries in column_ratio """
        column_width = {xn: column_width[xn] if xn in column_width else 'auto' for xn in self.entries}
        self.column_width = column_width

        self.column_width = {xn: self.__calculate_column_width__(xn,self.formatters[xn],column_width[xn], column_ratio[xn]) \
                                for xn in self.entries}

        """ Init lines """
        self.lines = []

        """ Counter """
        self.printed_lines = 0

        """ Compile header now """
        self.header, self.bottom_border = self.compile_header()

    """ Calculate auto column width """
    def __calculate_column_width__(self, title, formatter, width, ratio):

        if width != 'auto':
            return width

        """ Calculate title length """
        width = len(f' {title} ')

        """ Now format example """
        if '%$' not in title:
            val_length = len(formatter.format(1))
            val_length = (ratio + 1) + val_length*ratio
            width = np.maximum(width, val_length)

        """ Return width """
        return width

    """ compile header """
    def compile_header(self):
        """."""
        pre = '|' + '='.join([''.join(['='] * self.column_width[xn]) for xn in self.column_width]) + '|\n'
        _h = self.compile_line({xn: xn for xn in self.entries},
                               formatters={xn: '{}' for xn in self.entries}) + '\n'
        post = '|' + '|'.join([''.join(['='] * self.column_width[xn]) for xn in self.column_width]) + '|\n'
        return pre + _h + post, pre

    """ compile line from values """
    def compile_line(self, values, formatters=None):
        """."""
        if formatters is None:
            formatters = self.formatters

        """ Compile line """
        cols = {}
        for xn in self.entries:

            """ Column width """
            _width = self.column_width[xn]

            _val = values[xn]
            if not isinstance(_val, list):
                _val = [_val]

            if '%$' not in formatters[xn]:
                _col = '  '.join([formatters[xn].format(_v) for _v in _val])
                """ Check if we have to trim according to max size of column """
                _col = _col[:_width - 2] if (len(_col) > (_width - 2)) else _col
                _col = _col.strip()
                lspace = int(np.maximum(1, _width // 2 - len(_col) // 2))
                rspace = int(np.maximum(1, _width - len(_col) - lspace))
                lspace = ''.join([' '] * lspace)
                rspace = ''.join([' '] * rspace)
                _col = '{}{}{}'.format(lspace, _col, rspace)
            else:
                bar_length = _width - 2
                _col = ''.join(['█'] * int(bar_length * _val[0]))
                _anticol = ''.join(['░'] * (bar_length - len(_col)))
                _col = ' {}{} '.format(_col, _anticol)

            """ Place in dict """
            cols[xn] = _col

        """ Now place cols altogether """
        cols = '|' + '|'.join([cols[xn] for xn in cols]) + '|'

        return cols

    """ update_line method """
    def update_line(self, values, append=False):
        """."""

        """ Compile line """
        cols = self.compile_line(values)

        """ check if we have to append or update last line """
        append |= (not (self.printed_lines > 0))

        if append:
            self.lines.append(cols)
        else:
            self.lines[-1] = cols

        return cols

    """ print method """
    def __str__(self):
        out = self.header
        for line in self.lines:
            out += line + '\n'
        out += self.bottom_border + '\n'
        return out
