import json, random, time, threading, urllib.request, urllib.parse
from pathlib import Path
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
BASE=Path(__file__).parent
SONGS=[('aday','Адай'),('balbyrauyn','Балбырауын'),('saryarka','Сарыарқа'),('konyil','Көңіл ашар'),('erke','Ерке сылқым'),('aksak','Ақсақ құлан'),('kishkentai','Кішкентай')]
GOLD=(.93,.72,.34,1); BG=(.035,.065,.12,1); PANEL=(.09,.15,.23,1)
Window.clearcolor=BG
if platform not in ('android','ios'): Window.size=(400,740)
# Onset timing for the 127.7-second Aday test recording (not audio).
ADAY_CHART={"easy":[1.67,5.54,6.73,10.44,11.55,12.29,13.5,14.73,15.96,17.18,18.09,19.01,20.21,21.3,22.04,23.29,24.52,25.74,26.96,28.19,29.11,30.33,31.09,32.47,33.7,34.75,35.53,36.76,37.98,38.76,39.51,40.43,41.36,42.1,42.88,44.1,45.33,46.25,47,47.76,48.69,49.42,50.23,50.99,51.77,52.52,53.29,54.2,54.98,55.74,56.96,57.88,58.86,60.02,61.1,61.86,63.09,64.6,65.53,66.6,67.82,68.59,69.82,70.89,72.27,73.17,74.08,75.01,75.79,76.56,77.77,78.69,79.47,80.23,81.45,82.68,83.6,84.51,85.44,86.2,87.57,88.8,89.71,90.47,91.25,92.47,93.7,94.92,95.71,96.45,97.2,97.98,98.9,99.65,100.43,101.66,102.72,103.49,104.42,105.33,106.25,107.01,107.78,109.01,109.92,110.84,111.76,112.52,113.9,114.67,115.74,116.97,118.04,119.41,120.18,121.25],"normal":[1.67,5.54,6.73,9.85,10.44,11.05,11.65,12.29,12.77,13.5,14.12,14.73,15.33,15.96,16.58,17.18,17.67,18.4,19.01,19.62,20.21,20.84,21.45,22.04,22.67,23.29,23.91,24.52,25.13,25.74,26.35,26.96,27.57,28.19,29.11,29.72,30.33,31.09,31.86,32.47,33.09,33.7,34.31,34.91,35.53,36.15,36.76,37.44,37.98,38.9,39.51,40.43,41.05,41.64,42.26,42.88,43.49,44.1,44.72,45.33,45.94,46.56,47.16,47.76,48.37,48.97,49.62,50.23,51.31,51.91,52.52,53.29,53.9,54.49,54.98,55.74,56.36,56.96,57.88,58.86,59.86,60.5,61.1,61.86,62.47,63.09,63.68,64.6,65.53,66.6,67.21,67.82,68.59,69.33,69.82,70.89,71.66,72.27,72.88,73.47,74.08,75.01,75.94,76.56,77.14,77.77,78.69,79.62,80.23,80.84,81.45,82.07,82.68,83.29,83.9,84.51,85.13,86.2,86.97,87.57,88.18,88.8,89.71,90.64,91.25,91.86,92.47,93.08,93.7,94.31,94.92,95.54,96.45,97.06,97.98,98.59,99.21,99.81,100.43,101.04,101.66,102.72,103.49,104.11,104.72,105.33,106.25,107.17,107.78,108.39,109.01,109.92,110.84,111.76,112.52,113.3,113.9,114.53,115.12,115.74,116.35,116.97,117.58,118.18,118.8,119.41,120.03,120.63,121.25],"hard":[1.67,5.54,6.73,9.85,10.44,11.05,11.65,12.29,12.77,13.5,14.12,14.73,15.33,15.96,16.58,17.18,17.67,18.4,19.01,19.62,20.21,20.69,21.45,22.04,22.67,23.29,23.91,24.52,25.13,25.74,26.35,26.96,27.57,28.19,28.64,29.11,29.57,29.92,30.33,31.09,31.55,32.01,32.47,33.09,33.7,34.31,34.91,35.53,36.15,36.76,37.21,37.98,38.59,38.9,39.51,39.91,40.43,41.05,41.64,42.26,42.88,43.49,44.1,44.72,45.33,45.94,46.56,47.16,47.76,48.37,48.69,49.15,49.52,49.91,50.23,50.69,51.31,51.91,52.52,53.29,53.9,54.35,54.98,55.3,55.74,56.51,56.96,57.42,57.88,58.49,58.86,59.41,60.02,60.64,61.1,61.43,61.86,62.47,63.09,63.68,64.28,64.6,65.07,65.53,66.25,66.6,67.21,67.82,68.59,69.03,69.51,69.82,70.43,70.89,71.21,71.66,72.27,72.88,73.47,74.08,74.55,75.01,75.41,75.94,76.56,76.99,77.45,77.77,78.22,78.69,79.16,79.62,80.23,80.69,81.45,82.07,82.68,83.29,83.9,84.51,85.13,85.74,86.2,86.97,87.57,88.18,88.8,89.39,89.71,90.17,90.64,91.25,91.86,92.47,93.08,93.7,94.31,94.92,95.54,96.01,96.45,97.06,97.66,97.98,98.44,99.21,99.81,100.43,101.04,101.66,102.27,102.72,103.49,104.11,104.72,105.33,105.93,106.25,106.69,107.17,107.78,108.39,109.01,109.45,109.92,110.35,110.84,111.3,111.76,112.52,112.84,113.3,113.9,114.22,114.67,115.12,115.74,116.35,116.97,117.58,118.04,118.8,119.41,120.18,120.63,121.25]}
class AndroidTrack:
    def __init__(self, uri, volume):
        from jnius import autoclass
        activity=autoclass('org.kivy.android.PythonActivity').mActivity
        self.player=autoclass('android.media.MediaPlayer')()
        try:
            self.player.setDataSource(activity,autoclass('android.net.Uri').parse(uri))
            self.player.prepare()
            self.length=self.player.getDuration()/1000.0
            self.player.setVolume(float(volume),float(volume))
            self.player.start()
        except Exception:
            self.player.release()
            raise
    def elapsed(self):return self.player.getCurrentPosition()/1000.0
    def stop(self):
        try:self.player.stop()
        except Exception:pass
    def unload(self):self.player.release()
class Board(Widget):
    def __init__(self,app,**kw):
        super().__init__(**kw); self.app=app; self.start=time.monotonic(); self.score=0; self.index=0; self.dead=False
        rng=random.Random(app.song); self.interval=app.interval
        self.times=app.note_times()
        self.lanes=[rng.randrange(4) for _ in self.times]; self.event=Clock.schedule_interval(self.tick,1/60)
    def pos_y(self,i): return .14+(self.times[i]-self.app.game_elapsed(self.start))*.48
    def tick(self,dt):
        if self.dead:return
        if self.index<len(self.lanes) and self.pos_y(self.index)<.025: self.finish(False); return
        self.canvas.clear(); x,y=self.pos; w,h=self.size
        with self.canvas:
            Color(*BG); Rectangle(pos=self.pos,size=self.size)
            for k in range(4):
                Color(.12,.21,.30,1); Line(points=[x+k*w/4,y,x+k*w/4,y+h],width=1)
            Color(.85,.65,.3,.22); Rectangle(pos=(x,y+.07*h),size=(w,.15*h))
            Color(*GOLD); Line(points=[x,y+.14*h,x+w,y+.14*h],width=1.5)
            for i in range(self.index,min(len(self.lanes),self.index+12)):
                cy=self.pos_y(i)
                if not 0<=cy<=1:continue
                px=x+self.lanes[i]*w/4+4; py=y+cy*h-.035*h
                Color(*GOLD); RoundedRectangle(pos=(px,py),size=(w/4-8,.07*h),radius=[dp(8)])
                Color(*PANEL); RoundedRectangle(pos=(px+2,py+2),size=(w/4-12,.07*h-4),radius=[dp(6)])
    def on_touch_down(self,touch):
        if self.dead or not self.collide_point(*touch.pos):return super().on_touch_down(touch)
        lane=min(3,int((touch.x-self.x)/(self.width/4))); p=(touch.y-self.y)/self.height; cy=self.pos_y(self.index)
        if lane==self.lanes[self.index] and abs(p-cy)<.065 and abs(cy-.14)<.15:
            self.app.play_note(self.index); self.index+=1; self.score+=10; self.app.score_label.text=f'Ұпай: {self.score}'
            if self.index==len(self.lanes):self.finish(True)
        else:self.finish(False)
        return True
    def finish(self,won):
        if self.dead:return
        self.dead=True; self.event.cancel(); self.app.finished(self.score,won)
class Kui(App):
    def build(self):
        self.title='KÜI'; self.path=Path(self.user_data_dir)/'settings.json'; self.path.parent.mkdir(parents=True,exist_ok=True)
        try:self.data=json.loads(self.path.read_text(encoding='utf8'))
        except Exception:self.data={}
        self.player=self.data.get('player','Ойыншы'); self.url=self.data.get('url',''); self.volume=self.data.get('volume',.7); self.interval=.66; self.song='aday'; self.records=self.data.get('records',{}); self.room=None; self.poll=None; self.board=None; self.pending=False; self.sound=None; self.music=None; self.local_audio=False; self.aday_uri=self.data.get('aday_uri',''); self.session=0
        self.root_box=BoxLayout(orientation='vertical',padding=dp(18),spacing=dp(10)); self.menu(); return self.root_box
    def save(self):self.path.write_text(json.dumps({'player':self.player,'url':self.url,'volume':self.volume,'records':self.records,'aday_uri':self.aday_uri},ensure_ascii=False),encoding='utf8')
    def clear(self,title):
        self.root_box.clear_widgets(); self.label('◇   K Ü I   ◇',32,64,GOLD); self.label(title,21,42)
    def label(self,text,size=16,height=38,color=(.92,.94,.98,1)):
        a=Label(text=text,font_size=dp(size),color=color,size_hint_y=None,height=dp(height),halign='center',valign='middle'); a.bind(size=lambda w,s:setattr(w,'text_size',s)); self.root_box.add_widget(a); return a
    def button(self,text,fn):
        b=Button(text=text,font_size=dp(17),size_hint_y=None,height=dp(52),background_normal='',background_color=PANEL,color=GOLD); b.bind(on_release=lambda *_:fn()); self.root_box.add_widget(b); return b
    def leave(self):
        self.stop_music()
        self.session+=1
        if self.poll:self.poll.cancel(); self.poll=None
        if self.board and not self.board.dead:self.board.dead=True; self.board.event.cancel()
        self.board=None; self.room=None; self.pending=False
    def menu(self):
        self.leave(); self.clear('Домбыра  •  ырғақ ойыны'); self.button('Ойнау / Күй таңдау',lambda:self.choose('solo')); self.button('Онлайн дуэль',lambda:self.choose('duel')); self.button('Доспен жарысу',self.friend); self.button('Әлемдік рейтинг',lambda:self.choose('rank')); self.button('Профиль және баптаулар',self.settings); self.label('Адай: файл таңдалған' if self.aday_uri else 'Адай: MP3 файлын таңдаңыз',13,45)
    def choose(self,mode):
        self.clear('Күй таңдау'); scroll=ScrollView(); box=BoxLayout(orientation='vertical',size_hint_y=None,spacing=dp(6)); box.bind(minimum_height=box.setter('height'))
        for key,name in SONGS:
            b=Button(text=f'{name}   |   рекорд: {self.records.get(key,0)}',size_hint_y=None,height=dp(49),background_normal='',background_color=PANEL,color=GOLD,font_size=dp(16)); b.bind(on_release=lambda _,k=key:self.select(k,mode)); box.add_widget(b)
        scroll.add_widget(box); self.root_box.add_widget(scroll); self.button('Артқа',self.menu)
    def select(self,k,mode):
        self.song=k
        if mode=='solo':self.difficulty()
        elif mode=='rank':self.rank()
        else:self.join_room('random')
    def difficulty(self):
        self.clear(dict(SONGS)[self.song]); self.label('Жарыс рейтингі: орташа деңгей ғана',13,45)
        if self.song=='aday' and platform=='android':
            self.button('Адай MP3 файлын таңдау',self.pick_aday)
            self.label('Таңдалған жазба бар' if self.aday_uri else 'Алдымен өз MP3 файлыңызды таңдаңыз',13,40)
        for name,v in [('Жеңіл',.88),('Орташа',.66),('Қиын',.48)]:self.button(name,lambda v=v:self.start_game(v))
        self.button('Артқа',lambda:self.choose('solo'))
    def pick_aday(self):
        from android import activity
        from jnius import autoclass
        Intent=autoclass('android.content.Intent')
        owner=autoclass('org.kivy.android.PythonActivity').mActivity
        intent=Intent(Intent.ACTION_OPEN_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType('audio/*')
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION)
        def result(request, code, data):
            if request!=4071:return
            activity.unbind(on_activity_result=result)
            if code!=-1 or data is None:return
            try:
                uri=data.getData()
                owner.getContentResolver().takePersistableUriPermission(uri,Intent.FLAG_GRANT_READ_URI_PERMISSION)
                value=str(uri.toString())
                def apply(dt):
                    self.aday_uri=value; self.save(); self.difficulty()
                Clock.schedule_once(apply)
            except Exception:
                Clock.schedule_once(lambda dt:self.label('Файлды ашуға рұқсат берілмеді',13,35))
        activity.bind(on_activity_result=result)
        try:owner.startActivityForResult(intent,4071)
        except Exception:
            activity.unbind(on_activity_result=result)
            self.label('Файл таңдағыш ашылмады',13,35)
    def game_elapsed(self,start):
        if isinstance(self.music,AndroidTrack):
            try:return self.music.elapsed()
            except Exception:pass
        return time.monotonic()-start
    def start_game(self,interval=.66):
        self.interval=interval; self.clear(dict(SONGS)[self.song]); self.score_label=self.label('Ұпай: 0',21,35); self.opponent=self.label('Алтын сызыққа жеткенде бас',14,35); self.start_music(); self.board=Board(self); self.root_box.add_widget(self.board); self.button('Шығу',self.menu)
    def start_music(self):
        self.stop_music()
        self.local_audio=False
        if platform=='android' and self.song=='aday' and self.aday_uri and not self.room:
            try:
                self.music=AndroidTrack(self.aday_uri,self.volume)
                self.local_audio=True
                return
            except Exception:
                self.opponent.text='MP3 ашылмады. Сынақ дыбысы.'
        path=BASE/'assets'/f'{self.song}.wav'
        if path.is_file():
            try:
                self.music=SoundLoader.load(str(path))
                if self.music:
                    self.music.volume=self.volume
                    self.music.play()
            except Exception:
                self.stop_music()
    def stop_music(self):
        if self.music:
            self.music.stop(); self.music.unload(); self.music=None
        if self.sound:
            self.sound.stop(); self.sound.unload(); self.sound=None
    def note_times(self):
        # Optional chart: onset times in seconds, per difficulty, measured from recording start.
        if self.music:
            if self.local_audio and abs(self.music.length-127.7)<1.0:
                return ADAY_CHART[{.88:'easy',.66:'normal',.48:'hard'}.get(self.interval,'normal')]
            try:
                chart=json.loads((BASE/'assets'/f'{self.song}.json').read_text(encoding='utf8'))
                key={.88:'easy',.66:'normal',.48:'hard'}.get(self.interval,'normal')
                times=[float(t) for t in chart[key]]
                if times and times[0]>=0 and all(b>a for a,b in zip(times,times[1:])):
                    return times
            except (OSError, ValueError, TypeError, KeyError):
                pass
            length=self.music.length
            if length>2:
                return [1.7+i*self.interval for i in range(max(1,int((length-1.7)/self.interval)+1))]
        return [1.7+i*self.interval for i in range(40)]
    def play_note(self,i):
        if self.music:return
        if self.sound:self.sound.stop(); self.sound.unload()
        self.sound=SoundLoader.load(str(BASE/'assets'/f'{i%8}.wav'))
        if self.sound:self.sound.volume=self.volume; self.sound.play()
    def finished(self,score,won):
        self.stop_music()
        self.last_score=score; self.last_done=True; self.records[self.song]=max(score,self.records.get(self.song,0)); self.save(); self.clear('Күй аяқталды!' if won else 'Ойын аяқталды'); self.label(f'Ұпай: {score}  |  Рекорд: {self.records[self.song]}',20,60); self.label('★ ★ ★' if won else 'Қайта байқап көр',23,45,GOLD)
        if self.interval==.66 and self.url and not self.local_audio:self.request('/scores',{'song':self.song,'player':self.player,'score':score},lambda _:None)
        if self.room:self.opponent=self.label('Қарсылас нәтижесі күтілуде',15,65)
        else:self.button('Қайта ойнау',self.difficulty)
        self.button('Басты мәзір',self.menu)
    def request(self,path,payload,callback,fail=None):
        url=self.url.rstrip('/'); session=self.session
        def work():
            try:
                if not url:raise ValueError('Сервер мекенжайын баптауларда енгізіңіз')
                data=None if payload is None else json.dumps(payload).encode(); req=urllib.request.Request(url+path,data=data,headers={'Content-Type':'application/json'}); result=json.load(urllib.request.urlopen(req,timeout=4)); Clock.schedule_once(lambda dt:callback(result) if self.session==session else None)
            except Exception as e:
                msg=str(e); Clock.schedule_once(lambda dt:fail(msg) if fail and self.session==session else None)
        threading.Thread(target=work,daemon=True).start()
    def rank(self):
        self.clear('Рейтинг • '+dict(SONGS)[self.song]); status=self.label('Жүктелуде…',15,380); self.button('Артқа',lambda:self.choose('rank'))
        def show(r):status.text='\n'.join(f'{i+1}. {n} — {s}' for i,(n,s) in enumerate(r['scores'][:10])) or 'Әзірге ойыншы жоқ'
        self.request('/scores?'+urllib.parse.urlencode({'song':self.song}),None,show,lambda e:setattr(status,'text','Серверге қосылмады.\n'+e))
    def settings(self):
        self.clear('Профиль және баптаулар'); self.label('Ойыншы аты'); name=TextInput(text=self.player,multiline=False,size_hint_y=None,height=dp(48)); self.root_box.add_widget(name); self.label('Сервер URL (http://IP:8080)'); url=TextInput(text=self.url,multiline=False,size_hint_y=None,height=dp(48)); self.root_box.add_widget(url); self.label('Дыбыс деңгейі (0–100)'); vol=TextInput(text=str(int(self.volume*100)),multiline=False,input_filter='int',size_hint_y=None,height=dp(48)); self.root_box.add_widget(vol)
        def store():self.player=name.text.strip()[:24] or 'Ойыншы'; self.url=url.text.strip(); self.volume=min(100,max(0,int(vol.text or '0')))/100; self.save(); self.menu()
        self.button('Сақтау',store); self.button('Артқа',self.menu)
    def friend(self):
        self.clear('Доспен жарысу'); code=TextInput(hint_text='Бөлме коды',multiline=False,size_hint_y=None,height=dp(50)); self.root_box.add_widget(code); self.button('Бөлмеге кіру',lambda:self.join_room('join',code.text.strip())); self.button('Бөлме ашу (Адай)',lambda:(setattr(self,'song','aday'),self.join_room('create'))); self.button('Артқа',self.menu)
    def join_room(self,mode,code=''):
        self.clear('Онлайн дуэль'); self.status=self.label('Серверге қосылу…',16,130); self.button('Бас тарту',self.menu)
        def joined(r):
            self.room=r; self.song=r['song']; self.last_score=0; self.last_done=False; self.started=False; self.status.text='Бөлме: '+r['code']+'\nҚарсылас күтілуде'; self.poll=Clock.schedule_interval(self.poll_room,.6)
        self.request('/room',{'mode':mode,'code':code,'song':self.song,'player':self.player},joined,lambda e:setattr(self.status,'text','Қосылмады: '+e))
    def poll_room(self,dt):
        if not self.room or self.pending:return
        self.pending=True; score=self.board.score if self.board else self.last_score
        def state(r):
            self.pending=False
            if not self.started:
                if r['start'] is None:return
                delay=r['start']-r['now']; self.status.text='Басталуына: '+str(max(0,int(delay+1)))+' сек.'
                if delay<=0:self.started=True; self.start_game(.66)
            else:
                self.opponent.text='  |  '.join(f"{p['name']}: {p['score']}" for p in r['players'])
                if all(p['done'] for p in r['players']):
                    scores=[p['score'] for p in r['players']]; self.opponent.text+='\n'+('Тең ойын' if len(set(scores))==1 else 'Жеңімпаз: '+max(r['players'],key=lambda p:p['score'])['name']); self.poll.cancel(); self.poll=None
        def failed(e):self.pending=False
        self.request('/state',{'song':self.song,'player':self.player,'code':self.room['code'],'token':self.room['token'],'score':score,'done':self.last_done},state,failed)
    def on_pause(self):
        if self.board and not self.board.dead:self.menu()
        return True
    def on_stop(self):
        self.stop_music()
if __name__=='__main__':Kui().run()
