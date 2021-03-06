from flask import Flask,request,render_template
import os
import sys
import thread
import threading
import subprocess
import commands
import time
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
# change the path after the '+' to the parent dir of all .mp3 files
root_dir = os.environ['HOME']+'/mini/Music/Media.localized/Music'
playing = None
player='mpg123'
lists = []
current = root_dir

def list_play():
    global playing
    print "list_play() executing"
    while True:
        if lists and not playing:
            playing = lists.pop()
            t = threading.Thread(target=os.system, args=(player +'"'+ playing +'" ',))
            #os.system(player +'"'+ playing +'" ')    
            #time.sleep(5)
            #os.system("killall omxplayer.bin" )
            t.start()
            t.join()
            time.sleep(3)
        else :    
            time.sleep(10)
        stat = subprocess.check_output('ps aux | grep mpg123  | wc -l',shell=True)
        if int(stat) <= 2 :
             playing = None
        print "printing 'lists' inside list_play()"
        print lists

def get_cur_music(cmd):
    print "get_cur_music() executing"
    info=subprocess.check_output("ps aux | grep  "+cmd,shell=True)
    infos = info.split('\n')
    l = len(info.split('\n'))
    if l > 3:
        return os.path.basename(infos[1])[:-4]


thread.start_new_thread(list_play,())

@app.route('/')
def index():
    global playing
    global lists
    global current
    global root_dir
    #df = commands.getoutput('df -h')
    #if root_dir not in df:
    #    os.system('sudo mount /dev/sda1 '+root_dir)
    if request.args.get('path') and os.path.isdir(request.args.get('path')):
        current = request.args.get('path') 
    music = request.args.get('music')
    add = request.args.get('add')
    cmd = request.args.get('cmd')
    rm = request.args.get('rm')
    files = os.listdir(current)
    musics = []
    dirs = []
    playing = get_cur_music("mpg123")
    stat = subprocess.check_output('ps aux | grep mpg123  | wc -l',shell=True)
    if stat == 1 :
        playing = None
    for file in files:
        if os.path.isdir(current + '/' + file):
            dirs.append(file)
        elif file[-4:] == '.mp3':
            musics.append(file)
    if os.path.abspath(current) != root_dir:
        dirs.append('..')
    musics.sort()
    dirs.sort()
    if music:
        print "printing 'music' inside 'index()'" 
        print music
        
    #    thread.start_new_thread(os.system,player +'"'+ music+'" &')
        os.system("killall mpg123" )
        print "issuing 'os.system(player +'\"'+ music+'\" &')'"
        print "player: " + player
        print "music: " + music
        #os.system(player +'"'+ music+'" &')
        os.system(player +' "'+ music+'" &')
        playing = music
#        return music + 'is on playing\n' + render_template('views.html',current = path , dirs = dirs ,musics = musics)
    if cmd:
        if cmd == 'killall':
            os.system("killall mpg123" )
            playing =  None
    if add:
        print add
        lists.append(add)
    if rm:
        print rm
        lists.remove(rm)
    print playing
    mlists = []
    for list in lists:
        mlists.append(os.path.basename(list))
    return render_template('views.html',playing = playing,lists = lists ,mlists = mlists,current = current , dirs = dirs ,musics = musics)


if __name__ == '__main__':
    app.run("0.0.0.0")
