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

import os, re, sys
import argparse
from xmlrpclib import ServerProxy
import gzip,urllib2,StringIO,glob
#at the moment main version doesn't suport multi color/encoding
#pip install --upgrade git+https://github.com/xecgr/srtmerge.git
from srtmerge import srtmerge

#check if srtmerge accept srt-encoding dict arg
try:
    from srtmerge.srt import ACCEPT_SRT_ENCODING
except ImportError:
    ACCEPT_SRT_ENCODING=False
#check if srtmerge accept color-lang stuff

try:
    from srtmerge.srt import ACCEPT_IDENTIFY_LANGS
except ImportError:
    ACCEPT_IDENTIFY_LANGS=False 
        


DEFAULT_VIDEO_EXTS   = ['.avi','.mkv','.mp4']
OPENSUBTITLES_SERVER = 'http://api.opensubtitles.org/xml-rpc'
USER_AGENT           = 'Anaar SubsLauncher v1'
LANGUAGE             = 'en'
DEFAULT_LANGS        = ['es','en']
DEFAULT_REGEXS       = [
    'S(\d{1,2})E(\d{1,2})', #S0xE0y
    '(\d{1,2})x(\d{1,2})' , #0x00
    '(\d{1,2})\.(\d{1,2})'  #0.00
    '(\d)(\d{1,2})'         #201
] 

def get_season_episode(name, custom_regexs = []): 
    #let user pass more regexs
    custom_regexs.extend(DEFAULT_REGEXS)
    season,episode=0,0
    for pattern in custom_regexs:
        matches = re.search(pattern,name.upper())
        if matches:
            groups = matches.groups()
            if len(groups)==2:
                season,episode = str(int(groups[0])),str(int(groups[1]))
                break
    return season,episode

def get_queries(path='',video_extensions=DEFAULT_VIDEO_EXTS):
    queries   = []
    show_name = path
    if not path:
        path = os.getcwd()
        show_name = os.path.split(path)[-1]
    path = os.path.join(path,'*{}')
    for ve in video_extensions:
        if not ve.startswith("."):
            ve = "."+ve
        for f in glob.glob(path.format(ve)):
            queries.append(f)
    return show_name,queries

def downmergesubs(**kwargs):
    video_extensions  = kwargs.get('video_extensions',DEFAULT_VIDEO_EXTS)
    subs_languages    = kwargs.get('subs_languages',DEFAULT_LANGS)
    regexs            = kwargs.get('regexs',[])
    show_name         = kwargs.get('show_name','').strip()
    
    show_name,queries = get_queries(path=show_name,video_extensions=video_extensions)
    xmlrpc            = ServerProxy(OPENSUBTITLES_SERVER,allow_none=True)
    username          = ''
    password          = ''
    
    data              = xmlrpc.LogIn(username, password,subs_languages[0], USER_AGENT)
    token             = data.get('token','')
    if not token:
        print "Invalid OPENSUBTITLES credentials"
        sys.exit()
    
    for query in queries:
        query = os.path.split(query)[-1]
        season,episode = get_season_episode(query, custom_regexs=regexs)
        print u"Getting season and episode: {},{}".format(season,episode)
        _query = query
        if not show_name or show_name.lower() not in query.lower():
            _query = show_name + " " + query
        params = [{'sublanguageid': subs_languages[0], 'query': _query}]
        #(array('sublanguageid' => $sublanguageid, 'moviehash' => $moviehash, 'moviebytesize' => $moviesize, imdbid => $imdbid, query => 'movie name', "season" => 'season number', "episode" => 'episode number', 'tag' => tag
        print u"Searching subs for: {}".format(_query)
        data = xmlrpc.SearchSubtitles(token, params)
        lang_subinfo    = {}
        #sorted by download count
        for d in data['data']:
            lang = d.get('ISO639','')
            if lang in subs_languages and d.get('SeriesSeason',0)==season and d.get('SeriesEpisode',0)==episode and not lang_subinfo.get(lang,{}):
                lang_subinfo[lang]=d
        
        srt_encoding = {}
        for l,d in lang_subinfo.iteritems():
            response = urllib2.urlopen(d['SubDownloadLink'])
            compressedFile = StringIO.StringIO()
            compressedFile.write(response.read())
            #
            # Set the file's current position to the beginning
            # of the file so that gzip.GzipFile can read
            # its contents from the top.
            #
            compressedFile.seek(0)
            decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
            outFilePath=d['SubFileName']
            srt_encoding[outFilePath] = d['SubEncoding']
            with open(outFilePath, 'w') as outfile:
                outfile.write(decompressedFile.read())
        out_filepath, out_filepath_ext = os.path.splitext(query)
        out_filepath = out_filepath +".srt"
        #prepare args and kwargs depending of srtmerge version
        srt_args = [
            srt_encoding.keys(),
            out_filepath
        ]
        if ACCEPT_SRT_ENCODING:
            srt_args[0] = srt_encoding
        
        srt_kwargs = {
            'offset' :1
        }
        if ACCEPT_IDENTIFY_LANGS:
            srt_kwargs = {
                'identify_langs' :True
            }
        
        srtmerge(*srt_args, **srt_kwargs)
        for srt in srt_encoding:
            os.remove(srt)
        
    xmlrpc.LogOut(token)