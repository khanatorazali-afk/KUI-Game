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
class Board(Widget):
    def __init__(self,app,**kw):
        super().__init__(**kw); self.app=app; self.start=time.monotonic(); self.score=0; self.index=0; self.dead=False
        rng=random.Random(app.song); self.lanes=[rng.randrange(4) for _ in range(40)]; self.interval=app.interval; self.event=Clock.schedule_interval(self.tick,1/60)
    def pos_y(self,i): return .14+(1.7+i*self.interval-(time.monotonic()-self.start))*.48
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
        self.player=self.data.get('player','Ойыншы'); self.url=self.data.get('url',''); self.volume=self.data.get('volume',.7); self.interval=.66; self.song='aday'; self.records=self.data.get('records',{}); self.room=None; self.poll=None; self.board=None; self.pending=False; self.sound=None; self.session=0
        self.root_box=BoxLayout(orientation='vertical',padding=dp(18),spacing=dp(10)); self.menu(); return self.root_box
    def save(self):self.path.write_text(json.dumps({'player':self.player,'url':self.url,'volume':self.volume,'records':self.records},ensure_ascii=False),encoding='utf8')
    def clear(self,title):
        self.root_box.clear_widgets(); self.label('◇   K Ü I   ◇',32,64,GOLD); self.label(title,21,42)
    def label(self,text,size=16,height=38,color=(.92,.94,.98,1)):
        a=Label(text=text,font_size=dp(size),color=color,size_hint_y=None,height=dp(height),halign='center',valign='middle'); a.bind(size=lambda w,s:setattr(w,'text_size',s)); self.root_box.add_widget(a); return a
    def button(self,text,fn):
        b=Button(text=text,font_size=dp(17),size_hint_y=None,height=dp(52),background_normal='',background_color=PANEL,color=GOLD); b.bind(on_release=lambda *_:fn()); self.root_box.add_widget(b); return b
    def leave(self):
        self.session+=1
        if self.poll:self.poll.cancel(); self.poll=None
        if self.board and not self.board.dead:self.board.dead=True; self.board.event.cancel()
        self.board=None; self.room=None; self.pending=False
    def menu(self):
        self.leave(); self.clear('Домбыра  •  ырғақ ойыны'); self.button('Ойнау / Күй таңдау',lambda:self.choose('solo')); self.button('Онлайн дуэль',lambda:self.choose('duel')); self.button('Доспен жарысу',self.friend); self.button('Әлемдік рейтинг',lambda:self.choose('rank')); self.button('Профиль және баптаулар',self.settings); self.label('ДЕМО • түпнұсқа күй аудиосы қосылмаған',13,45)
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
        for name,v in [('Жеңіл',.88),('Орташа',.66),('Қиын',.48)]:self.button(name,lambda v=v:self.start_game(v))
        self.button('Артқа',lambda:self.choose('solo'))
    def start_game(self,interval=.66):
        self.interval=interval; self.clear(dict(SONGS)[self.song]); self.score_label=self.label('Ұпай: 0',21,35); self.opponent=self.label('Алтын сызыққа жеткенде бас',14,35); self.board=Board(self); self.root_box.add_widget(self.board); self.button('Шығу',self.menu)
    def play_note(self,i):
        if self.sound:self.sound.stop()
        self.sound=SoundLoader.load(str(BASE/'assets'/f'{i%8}.wav'))
        if self.sound:self.sound.volume=self.volume; self.sound.play()
    def finished(self,score,won):
        self.last_score=score; self.last_done=True; self.records[self.song]=max(score,self.records.get(self.song,0)); self.save(); self.clear('Күй аяқталды!' if won else 'Ойын аяқталды'); self.label(f'Ұпай: {score}  |  Рекорд: {self.records[self.song]}',20,60); self.label('★ ★ ★' if won else 'Қайта байқап көр',23,45,GOLD)
        if self.interval==.66 and self.url:self.request('/scores',{'song':self.song,'player':self.player,'score':score},lambda _:None)
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
if __name__=='__main__':Kui().run()
