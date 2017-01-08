#! /usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyleft 2016 xecgr <xecgr at gmail com>
#
#    This is a free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__ = 'xecgr'
__version__ = '1.0'
__release_date__ = "01/09/2016"

import argparse

import os
import sys

from downmergesubs import DEFAULT_VIDEO_EXTS,DEFAULT_LANGS,downmergesubs



def print_version():
    print("downmergesubs: version %s (%s)" % (__version__, __release_date__))


def print_error(message):
    print("downmergesubs error: {0}".format(message))


def _check_argv(args):
    return True


def main():
    parser = argparse.ArgumentParser()
    # To make the input integers
    parser.add_argument(
        '--langs',
        nargs='+', 
        type=str,
        default=DEFAULT_LANGS,
        help = "list of ISO639 language codes"
    )
    parser.add_argument(
        '--exts',
        nargs='+', 
        type=str,
        default=DEFAULT_VIDEO_EXTS ,
        help = "list of video file extensions"
    )
    parser.add_argument(
        '--regexs',
        nargs='+', 
        type=str,
        default=[],
        help = "custom regex to dectect season and episode from file name"
    )
    parser.add_argument(
        '--keep-partial-subs',
        type=bool,
        default=False,
        help = "keep merged srt files"
    )
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    parser.add_argument("-n", type=str, help="tv show name [default current directory name]")
    
    
    video_extensions = parser.parse_args().exts
    subs_languages   = parser.parse_args().langs
    regexs           = parser.parse_args().regexs
    keep_partial_subs= parser.parse_args().keep_partial_subs
    show_name        = parser.parse_args().n or ''
    if '--version' in sys.argv:
        print_version()
        sys.exit(0)
    args = vars(parser.parse_args())
    if _check_argv(args):
        downmergesubs(
            video_extensions = video_extensions,
            subs_languages   = subs_languages,
            regexs           = regexs,
            keep_partial_subs=keep_partial_subs,
            show_name        = show_name
        )
    
if __name__ == '__main__':
    main()
