# DownmergeSubs

Developed using Python 2.7

This script download your tv shows episodes subtitles in as many languages you need, and merge them to get a unique .srt file with all translations inside it

It uses opensubtitles API to get desired langs subtitles and srtmerge to put them all in a single file

Script params are useful to get a custom behavior, but default's for common cases, here you are some examples:

```
xecgr@carteras:~/$ downmergesubs --help
usage: downmergesubs [-h] [--langs LANGS [LANGS ...]] [--exts EXTS [EXTS ...]]
                     [--regexs REGEXS [REGEXS ...]] [-v] [-n N]

optional arguments:
  -h, --help            show this help message and exit
  --langs LANGS [LANGS ...]
                        list of ISO639 language codes
  --exts EXTS [EXTS ...]
                        list of video file extensions
  --regexs REGEXS [REGEXS ...]
                        custom regex to dectect season and episode from file
                        name
  -v, --verbosity
  -n N                  tv show name [default current directory name]
```

Let's say that you want to download Game of Thrones subs:

```
xecgr@carteras:~/Game of thrones$ ls -l
S01E01 - Winter Is Coming.avi
S01E02 - The Kingsroad.avi
S01E03 - Lord Snow.avi
```

If you have all files wrapped in a folder with show's name, you can omit the `-n` parameter, because folder's name is set as the show name

In order to extract season and episode, the script's defined a list of regex to extract them. If your episodes are coded in the standard way, you can also omit the `-regexs` parameter

You can also define the desired languages you want to download and merge. Default are EN and ES, but you can download as many as you want and need.

And finaly there's a list of video file extensions that allow script to discover the episodes in current dir. Default list values are: `['.avi','.mkv','.mp4']`. If you need to specify another extension, use `-exts` parameter.

So, let's put it all together. In this case we have a folder named as desired show, and, fortunately, season and episodes are coded in standard way and their extensions is a script-known one, so de default execution will work

```
xecgr@carteras:~/Game of thrones$ downmergesubs 
Getting season and episode: 1,1
Searching subs for: Game of thrones S01E01 - Winter Is Coming.avi
Getting season and episode: 1,3
Searching subs for: Game of thrones S01E03 - Lord Snow.avi
Getting season and episode: 1,2
Searching subs for: Game of thrones S01E02 - The Kingsroad.avi
xecgr@carteras:~/dev/github/downmergesubs/Game of thrones$ ls -l
S01E01 - Winter Is Coming.avi
S01E01 - Winter Is Coming.srt
S01E02 - The Kingsroad.avi
S01E02 - The Kingsroad.srt
S01E03 - Lord Snow.avi
S01E03 - Lord Snow.srt
```

As you can see, the script uses its default values to get show's name, to get video files using default video extensions, and it gets default language subtitles.

```
xecgr@carteras:~/Game of thrones$ head -n 30 S01E03\ -\ Lord\ Snow.srt 
1
00:00:06,001 --> 00:00:12,075
Advertise your product or brand here
contact www.OpenSubtitles.org today
Anuncie su producto o marca aquí
contáctenos www.OpenSubtitles.org hoy

2
00:01:35,927 --> 00:01:46,001
www.SUBTITULOS.es
-DIFUNDE LA PALABRA-

3
00:02:13,538 --> 00:02:14,854
Welcome, Lord Stark.
Bienvenido, Lord Stark.

4
00:02:14,974 --> 00:02:18,274
Grand Maester Pycelle has called
a meeting of the Small Council.
El Gran Maestre Pycelle ha convocado
una reunión del consejo.

5
00:02:18,309 --> 00:02:20,409
The honor of your presence is requested.
Se requiere el honor de su presencia.
```

#Installation
`pip install --upgrade git+https://github.com/xecgr/downmergesubs.git`
In near future it will be available via `pip install`

#Possible issue
Maybe, downloaded subtitles are note synchronized between them. I have not been able to reproduce it, but if you do, open an issue with concrete examples and maybe we can fix it

