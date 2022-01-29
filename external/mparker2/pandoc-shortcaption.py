#!/bin/env python3

# Based on fork from user mparker2, see https://github.com/martisak/pandoc-shortcaption/issues/1

from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from pandocfilters import toJSONFilter, RawInline, RawBlock
import logging
import re
FORMAT = "%(asctime)s %(levelname)-8s%(module)-10s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.ERROR)

# \begin{figure}[htbp]
# \centering
# \includegraphics{Image Source}
# \caption{Image Title}
# \end{figure}



def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever


def alt_caption_emph_strong(text):
    text = text.replace("_", "\_")
    boldified = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)
    italified = re.sub(r'\*(.*?)\*', r'\\textit{\1}', boldified)
    codified = re.sub(r'`(.*?)`', r'\\texttt{\1}', italified)
    return codified


def text(c):
    if type(c) == list:
        return ' '.join(text(d) for d in c)
    if c['t'] == 'Space':
        return ' '
    elif c['t'] == 'BulletList':
        return '\\begin{itemize}\n' + text(c['c']) + '\\end{itemize}'
    elif c['t'] == 'Plain':
        return '\\item' + text(c['c'])
    elif c['t'] == 'DoubleQuote':
        return '"'
    elif c['t'] == 'Strong':
        return '\\textbf{' + text(c['c']) + '}'
    elif c['t'] == 'Emph':
        return '\\textit{' + text(c['c']) + '}'
    elif c['t'] == 'Str':
        return c['c'].replace('{','\\{').replace('}','\\}')
    elif c['t'] == 'RawInline':
        return c['c'][1]
    elif c['t'] == 'Math':
        return '$'+c['c'][1]+'$'
    elif c['t'] == 'Code':
        return '\\texttt{' + c['c'][1].replace("_", "\_") + '}'
    elif c['t'] == 'SoftBreak':
        return ''
    else:
        eprint(c)
        return ''.join(text(d) for d in c['c'])


def shortcap(key, value, format, meta):
    if key == 'Image' and format == "latex":
        #logging.debug(value)
        label = value[0][0]
        src = value[2][0]
        alt = alt_caption_emph_strong(remove_prefix(value[2][1], "fig:"))
        attributes = value[0][2]
        height = None
        if isinstance(attributes, list):
            for attr in attributes:
                if attr[0].lower() == "height":
                    height = int(attr[1][:-2])

        logging.debug(height)

        if (alt != ""):

            caption = text(value[1])

            raw = r'\begin{figure}[!ht]' + '\n'
            raw += r'\centering' + '\n'
            if height is None:
                raw += '\\includegraphics[width=\\textwidth,height=562pt,keepaspectratio]{{{}}}'.format(src, alt) + '\n'
            else:
                raw += '\\includegraphics[width=\\textwidth,height={}pt,keepaspectratio]{{{}}}'.format(
                    int(round(height * 0.75)), src, alt) + '\n'

            raw += '\\caption[{}]{{{}}}'.format(alt, caption)
            if (label != ''):
                raw += '\label{{{}}}'.format(label)
            raw += '\n' + r'\end{figure}' + '\n'

            return RawInline('tex', raw)

    if key == "Table" and format == "latex":
        caption = text(value[0])
        short = (caption.split('.')[0]+'.')
        raw = "\\begin{longtable}[]{@{}ll@{}}\n"
        raw += "\\caption[{}]{{{}}}".format(short,caption)
        raw += '\\tabularnewline\n \\toprule\n'
        raw += ' & '.join(text(l) for l in value[3])
        raw += "\\tabularnewline\n \\midrule \\endfirsthead \\toprule\n"
        raw += ' & '.join(text(l) for l in value[3])
        raw += "\\tabularnewline\n \\midrule \\endhead\n"
        for line in value[4]:
            raw += ' & '.join(text(column) for column in line)
            raw += '\\tabularnewline\n'
        raw += '\\bottomrule \\end{longtable}'

        return RawBlock('tex',raw)

def main():
    toJSONFilter(shortcap)


if __name__ == "__main__":
    main()
