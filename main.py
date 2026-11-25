import json, random, time, threading, urllib.request, urllib.parse, math
from pathlib import Path
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line, Ellipse, Triangle
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
GOLD=(1,.77,.36,1); BG=(.025,.045,.09,1); PANEL=(.075,.14,.22,1); CYAN=(.22,.92,.88,1)
Window.clearcolor=BG
if platform not in ('android','ios'): Window.size=(400,740)
# Onset timing for the 127.7-second Aday test recording (not audio).
ADAY_CHART={"easy":[1.67,2.6,3.4,4.48,5.22,6.13,6.86,7.78,8.52,9.66,10.9,11.98,12.77,14,14.73,15.64,16.45,17.18,17.8,18.7,19.45,20.07,20.68,21.3,21.9,22.51,23.28,23.91,24.66,25.25,25.88,26.47,27.08,27.7,28.34,29.1,29.72,30.33,30.94,31.7,32.31,33.08,33.69,34.31,34.92,35.68,36.3,36.91,37.66,38.29,38.9,39.51,40.28,40.9,41.5,42.09,42.71,43.34,43.96,44.54,45.16,45.79,46.41,46.99,47.61,48.21,48.84,49.62,50.22,50.83,51.46,52.08,52.68,53.29,53.89,54.49,55.12,55.74,56.35,56.96,57.58,58.18,58.79,59.56,60.17,60.82,61.43,62.03,62.63,63.23,63.8,64.46,65.06,65.7,66.46,67.07,67.67,68.28,68.89,69.5,70.11,70.73,71.36,71.96,72.57,73.31,73.92,74.55,75.18,75.94,76.56,77.17,77.77,78.39,79,79.61,80.22,80.84,81.45,82.06,82.67,83.29,83.9,84.51,85.12,85.74,86.34,86.96,87.57,88.18,88.8,89.39,90.02,90.63,91.24,91.86,92.47,93.08,93.69,94.3,94.92,95.53,96.15,96.76,97.36,97.97,98.6,99.2,100.11,100.73,101.5,102.1,102.71,103.33,104.1,104.72,105.33,105.93,106.55,107.17,107.78,108.39,109,109.62,110.22,110.84,111.42,112.06,112.67,113.29,113.9,114.52,115.12,115.74,116.35,116.96,117.58,118.18,118.8,119.41,120.02,120.63,121.24,122.02],"normal":[1.67,2.03,2.6,2.94,3.4,3.71,4.48,4.93,5.22,5.53,6.13,6.56,6.86,7.25,7.78,8.14,8.52,9.04,9.66,10.44,10.9,11.32,11.98,12.41,12.77,13.5,14,14.38,14.73,15.22,15.64,16.14,16.45,16.77,17.18,17.49,17.8,18.21,18.7,19.01,19.45,19.74,20.07,20.38,20.68,20.99,21.3,21.6,21.9,22.2,22.51,22.97,23.28,23.6,23.91,24.36,24.66,24.97,25.25,25.58,25.88,26.19,26.47,26.8,27.08,27.4,27.7,28.03,28.34,28.63,29.1,29.41,29.72,30.06,30.33,30.64,30.94,31.24,31.7,32.01,32.31,32.78,33.08,33.38,33.69,33.99,34.31,34.62,34.92,35.36,35.68,35.98,36.3,36.61,36.91,37.21,37.66,37.98,38.29,38.59,38.9,39.21,39.51,39.83,40.28,40.6,40.9,41.17,41.5,41.8,42.09,42.38,42.71,43.03,43.34,43.65,43.96,44.26,44.54,44.83,45.16,45.47,45.79,46.11,46.41,46.7,46.99,47.31,47.61,47.92,48.21,48.53,48.84,49.11,49.62,49.91,50.22,50.53,50.83,51.15,51.46,51.76,52.08,52.37,52.68,52.97,53.29,53.58,53.89,54.2,54.49,54.83,55.12,55.44,55.74,56.04,56.35,56.67,56.96,57.26,57.58,57.88,58.18,58.48,58.79,59.24,59.56,59.86,60.17,60.49,60.82,61.1,61.43,61.73,62.03,62.32,62.63,62.93,63.23,63.52,63.8,64.12,64.46,64.74,65.06,65.38,65.7,66,66.46,66.77,67.07,67.38,67.67,67.98,68.28,68.58,68.89,69.2,69.5,69.82,70.11,70.42,70.73,71.04,71.36,71.65,71.96,72.27,72.57,72.87,73.31,73.62,73.92,74.24,74.55,74.81,75.18,75.62,75.94,76.24,76.56,76.84,77.17,77.44,77.77,78.07,78.39,78.7,79,79.31,79.61,79.93,80.22,80.54,80.84,81.15,81.45,81.77,82.06,82.38,82.67,82.98,83.29,83.6,83.9,84.21,84.51,84.82,85.12,85.44,85.74,86.03,86.34,86.66,86.96,87.26,87.57,87.88,88.18,88.49,88.8,89.08,89.39,89.71,90.02,90.31,90.63,90.94,91.24,91.55,91.86,92.17,92.47,92.78,93.08,93.39,93.69,94,94.3,94.61,94.92,95.22,95.53,95.84,96.15,96.45,96.76,97.06,97.36,97.66,97.97,98.29,98.6,98.9,99.2,99.64,100.11,100.42,100.73,101.04,101.5,101.79,102.1,102.4,102.71,103.02,103.33,103.79,104.1,104.41,104.72,105.02,105.33,105.63,105.93,106.25,106.55,106.86,107.17,107.47,107.78,108.08,108.39,108.69,109,109.31,109.62,109.92,110.22,110.53,110.84,111.14,111.42,111.76,112.06,112.37,112.67,112.98,113.29,113.6,113.9,114.22,114.52,114.84,115.12,115.44,115.74,116.05,116.35,116.66,116.96,117.27,117.58,117.88,118.18,118.49,118.8,119.1,119.41,119.72,120.02,120.33,120.63,120.94,121.24,121.59,122.02],"hard":[1.67,1.88,2.03,2.29,2.6,2.76,2.94,3.22,3.4,3.54,3.71,4.36,4.48,4.75,4.93,5.1,5.22,5.4,5.53,5.84,6.13,6.37,6.56,6.72,6.86,7.07,7.25,7.62,7.78,7.95,8.14,8.29,8.52,8.71,9.04,9.38,9.66,9.85,10.44,10.74,10.9,11.05,11.32,11.55,11.98,12.28,12.41,12.55,12.77,13.19,13.5,13.69,14,14.24,14.38,14.5,14.73,14.94,15.22,15.38,15.64,15.95,16.14,16.27,16.45,16.58,16.77,16.98,17.18,17.33,17.49,17.66,17.8,18.09,18.21,18.4,18.7,18.82,19.01,19.26,19.45,19.62,19.74,19.87,20.07,20.2,20.38,20.53,20.68,20.83,20.99,21.14,21.3,21.45,21.6,21.75,21.9,22.04,22.2,22.36,22.51,22.67,22.97,23.13,23.28,23.44,23.6,23.74,23.91,24.2,24.36,24.51,24.66,24.82,24.97,25.12,25.25,25.44,25.58,25.74,25.88,26.05,26.19,26.35,26.47,26.65,26.8,26.96,27.08,27.26,27.4,27.57,27.7,27.88,28.03,28.18,28.34,28.5,28.63,28.8,29.1,29.24,29.41,29.56,29.72,29.92,30.06,30.19,30.33,30.49,30.64,30.79,30.94,31.09,31.24,31.55,31.7,31.85,32.01,32.16,32.31,32.47,32.78,32.92,33.08,33.23,33.38,33.54,33.69,33.81,33.99,34.15,34.31,34.47,34.62,34.75,34.92,35.21,35.36,35.53,35.68,35.84,35.98,36.14,36.3,36.45,36.61,36.76,36.91,37.06,37.21,37.37,37.66,37.81,37.98,38.14,38.29,38.43,38.59,38.75,38.9,39.05,39.21,39.35,39.51,39.66,39.83,40.12,40.28,40.43,40.6,40.75,40.9,41.04,41.17,41.36,41.5,41.64,41.8,41.95,42.09,42.26,42.38,42.57,42.71,42.88,43.03,43.19,43.34,43.49,43.65,43.8,43.96,44.1,44.26,44.41,44.54,44.71,44.83,45.02,45.16,45.33,45.47,45.63,45.79,45.94,46.11,46.25,46.41,46.55,46.7,46.85,46.99,47.15,47.31,47.46,47.61,47.77,47.92,48.07,48.21,48.37,48.53,48.69,48.84,48.97,49.11,49.41,49.62,49.74,49.91,50.06,50.22,50.34,50.53,50.69,50.83,50.98,51.15,51.3,51.46,51.6,51.76,51.9,52.08,52.2,52.37,52.52,52.68,52.8,52.97,53.12,53.29,53.41,53.58,53.72,53.89,54.02,54.2,54.35,54.49,54.67,54.83,54.98,55.12,55.29,55.44,55.58,55.74,55.9,56.04,56.2,56.35,56.51,56.67,56.81,56.96,57.13,57.26,57.42,57.58,57.73,57.88,58.03,58.18,58.33,58.48,58.63,58.79,59.08,59.24,59.4,59.56,59.71,59.86,60.02,60.17,60.32,60.49,60.63,60.82,60.97,61.1,61.26,61.43,61.58,61.73,61.86,62.03,62.17,62.32,62.47,62.63,62.78,62.93,63.08,63.23,63.39,63.52,63.68,63.8,63.98,64.12,64.28,64.46,64.6,64.74,64.91,65.06,65.22,65.38,65.53,65.7,65.84,66,66.25,66.46,66.6,66.77,66.89,67.07,67.21,67.38,67.5,67.67,67.82,67.98,68.11,68.28,68.42,68.58,68.71,68.89,69.02,69.2,69.32,69.5,69.65,69.82,69.96,70.11,70.27,70.42,70.58,70.73,70.89,71.04,71.2,71.36,71.49,71.65,71.81,71.96,72.11,72.27,72.42,72.57,72.71,72.87,73.16,73.31,73.47,73.62,73.78,73.92,74.08,74.24,74.39,74.55,74.69,74.81,75.01,75.18,75.31,75.62,75.79,75.94,76.08,76.24,76.39,76.56,76.72,76.84,76.99,77.17,77.29,77.44,77.59,77.77,77.89,78.07,78.22,78.39,78.52,78.7,78.85,79,79.16,79.31,79.46,79.61,79.74,79.93,80.07,80.22,80.38,80.54,80.69,80.84,80.97,81.15,81.29,81.45,81.6,81.77,81.92,82.06,82.22,82.38,82.52,82.67,82.82,82.98,83.13,83.29,83.41,83.6,83.74,83.9,84.05,84.21,84.37,84.51,84.68,84.82,84.99,85.12,85.28,85.44,85.58,85.74,85.86,86.03,86.19,86.34,86.49,86.66,86.81,86.96,87.08,87.26,87.42,87.57,87.72,87.88,88.03,88.18,88.31,88.49,88.63,88.8,88.94,89.08,89.23,89.39,89.51,89.71,89.85,90.02,90.17,90.31,90.46,90.63,90.77,90.94,91.1,91.24,91.4,91.55,91.7,91.86,91.98,92.17,92.31,92.47,92.62,92.78,92.93,93.08,93.23,93.39,93.54,93.69,93.85,94,94.14,94.3,94.44,94.61,94.76,94.92,95.07,95.22,95.39,95.53,95.7,95.84,96,96.15,96.3,96.45,96.6,96.76,96.9,97.06,97.2,97.36,97.5,97.66,97.81,97.97,98.14,98.29,98.44,98.6,98.75,98.9,99.04,99.2,99.5,99.64,99.81,100.11,100.25,100.42,100.55,100.73,100.88,101.04,101.35,101.5,101.66,101.79,101.96,102.1,102.27,102.4,102.57,102.71,102.88,103.02,103.19,103.33,103.49,103.79,103.93,104.1,104.23,104.41,104.55,104.72,104.85,105.02,105.17,105.33,105.45,105.63,105.76,105.93,106.06,106.25,106.4,106.55,106.69,106.86,107.01,107.17,107.29,107.47,107.61,107.78,107.89,108.08,108.23,108.39,108.51,108.69,108.83,109,109.12,109.31,109.45,109.62,109.74,109.92,110.05,110.22,110.35,110.53,110.67,110.84,110.96,111.14,111.3,111.42,111.57,111.76,111.89,112.06,112.22,112.37,112.52,112.67,112.83,112.98,113.13,113.29,113.41,113.6,113.74,113.9,114.06,114.22,114.38,114.52,114.66,114.84,114.97,115.12,115.27,115.44,115.59,115.74,115.87,116.05,116.2,116.35,116.5,116.66,116.82,116.96,117.14,117.27,117.43,117.58,117.73,117.88,118.03,118.18,118.31,118.49,118.65,118.8,118.95,119.1,119.25,119.41,119.57,119.72,119.87,120.02,120.18,120.33,120.48,120.63,120.79,120.94,121.1,121.24,121.43,121.59,121.87,122.02,122.36]}
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
class ThemeRoot(BoxLayout):
    def __init__(self,**kw):
        super().__init__(**kw)
        self.bind(pos=self.paint,size=self.paint)
        self.paint()
    def paint(self,*_):
        self.canvas.before.clear()
        x,y=self.pos; w,h=self.size
        with self.canvas.before:
            Color(*BG); Rectangle(pos=self.pos,size=self.size)
            for i in range(16):
                f=i/15
                Color(.025+.035*f,.045+.06*f,.09+.075*f,1)
                Rectangle(pos=(x,y+h*i/16),size=(w,h/16+1))
            Color(.09,.45,.65,.10); Ellipse(pos=(x-w*.44,y+h*.5),size=(w*1.2,h*.65))
            Color(.24,.12,.55,.11); Ellipse(pos=(x+w*.52,y-h*.25),size=(w,h*.8))
            Color(.09,.68,.64,.07); Ellipse(pos=(x+w*.55,y+h*.58),size=(w*.75,h*.5))
            Color(.93,.72,.34,.28); Line(points=[x+dp(7),y+dp(12),x+dp(7),y+h-dp(12)],width=1)
            Line(points=[x+w-dp(7),y+dp(12),x+w-dp(7),y+h-dp(12)],width=1)

class Brand(Widget):
    def __init__(self,**kw):
        super().__init__(**kw)
        self.phase=0.0; self.fx=None
        self.bind(pos=self.paint,size=self.paint,parent=self.parent_changed)
    def parent_changed(self,_,parent):
        if self.fx:self.fx.cancel(); self.fx=None
        if parent is not None:self.fx=Clock.schedule_interval(self.animate,1/24)
    def animate(self,dt):
        self.phase=(self.phase+dt)%100; self.paint()
    def paint(self,*_):
        self.canvas.clear(); x,y=self.center; w,h=self.size
        if w<10 or h<10:return
        u=min(w/16,h/5.2); p=self.phase
        def note(nx,ny,k):
            Ellipse(pos=(nx-.19*k,ny-.12*k),size=(.38*k,.24*k))
            Line(points=[nx+.15*k,ny,nx+.15*k,ny+.83*k,nx+.52*k,ny+.64*k],width=1.15)
        def ornament(ox,oy,scale,side):
            for j in range(2):
                z=scale*(1-.32*j)
                Line(points=[ox,oy,ox+side*.45*z,oy+.65*z,ox+side*.98*z,oy+.24*z,ox+side*.68*z,oy-.14*z,ox+side*.28*z,oy+.18*z],width=1.1)
                Line(points=[ox,oy,ox+side*.45*z,oy-.65*z,ox+side*.98*z,oy-.24*z,ox+side*.68*z,oy+.14*z],width=1.1)
        with self.canvas:
            for i in range(7,0,-1):
                r=u*(2.5+i*.38+.13*math.sin(p*1.6))
                Color(.08,.66,.79,.018+(7-i)*.008); Ellipse(pos=(x-r,y-r*.74),size=(r*2,r*1.48))
            Color(.26,.20,.70,.16); Ellipse(pos=(x+2*u,y-.8*u),size=(4.5*u,1.6*u))
            Color(.02,.12,.20,.94); RoundedRectangle(pos=(x-2.7*u,y-2.33*u),size=(5.4*u,4.66*u),radius=[u*.75])
            Color(*GOLD); Line(rounded_rectangle=(x-2.7*u,y-2.33*u,5.4*u,4.66*u,.75*u),width=1.2)
            Color(.22,.92,.88,.55); Line(circle=(x,y,2.02*u),width=1)
            # Dombra silhouette, warm wood and two strings.
            Color(.72,.40,.13,1); Ellipse(pos=(x-.92*u,y-1.74*u),size=(1.84*u,2.12*u))
            Color(*GOLD); Line(ellipse=(x-.92*u,y-1.74*u,1.84*u,2.12*u),width=1.5)
            Color(.92,.68,.33,1); RoundedRectangle(pos=(x-.20*u,y-.02*u),size=(.40*u,1.91*u),radius=[u*.08])
            Color(.98,.83,.49,1); RoundedRectangle(pos=(x-.32*u,y+1.50*u),size=(.64*u,.48*u),radius=[u*.08])
            Color(.18,.11,.07,1); Ellipse(pos=(x-.25*u,y-.72*u),size=(.5*u,.5*u))
            Color(.99,.94,.75,1)
            for off in (-.07,.07):Line(points=[x+off*u,y-1.40*u,x+off*u,y+1.86*u],width=.8)
            for j in range(6):
                fy=y+(.32+j*.19)*u; Line(points=[x-.19*u,fy,x+.19*u,fy],width=.7)
            for side in (-1,1):
                Color(.98,.74,.33,.83); ornament(x+side*3.2*u,y,.99*u,side)
                Color(.27,.92,.89,.60+.18*math.sin(p*2+side)); note(x+side*5.55*u,y-1.13*u+.23*u*math.sin(p+side),u*.86)
            Color(.78,.55,1,.58); note(x+5.25*u,y+1.0*u+.15*u*math.sin(p),u*.64)
            # Small stylized Kazakhstan flag motif.
            fx=x-6.3*u; fy=y+.58*u; fw=2.50*u; fh=1.25*u
            Color(.05,.72,.83,1); RoundedRectangle(pos=(fx,fy),size=(fw,fh),radius=[.10*u])
            Color(*GOLD); sx=fx+1.40*u; sy=fy+.79*u
            Ellipse(pos=(sx-.16*u,sy-.16*u),size=(.32*u,.32*u))
            for j in range(16):
                angle=j*math.pi/8
                Line(points=[sx+math.cos(angle)*.20*u,sy+math.sin(angle)*.20*u,sx+math.cos(angle)*.28*u,sy+math.sin(angle)*.28*u],width=.65)
            Line(points=[sx-.55*u,fy+.41*u,sx-.30*u,fy+.30*u,sx,fy+.36*u,sx+.30*u,fy+.30*u,sx+.55*u,fy+.41*u],width=1.1)
            Line(points=[sx-.12*u,fy+.34*u,sx,fy+.18*u,sx+.12*u,fy+.34*u],width=.9)
            for j in range(4):
                oy=fy+(.14+j*.30)*u
                Line(points=[fx+.12*u,oy,fx+.23*u,oy+.10*u,fx+.34*u,oy,fx+.23*u,oy-.10*u,fx+.12*u,oy],width=.65)
class Board(Widget):
    def __init__(self,app,**kw):
        super().__init__(**kw); self.app=app; self.start=time.monotonic(); self.score=0; self.index=0; self.dead=False
        rng=random.Random(app.song); self.interval=app.interval
        self.times=app.note_times()
        self.lanes=[]; self.flash=[0.0]*4; self.misses=0; self.combo=0
        for i,when in enumerate(self.times):
            choices=list(range(4))
            if i and when-self.times[i-1]<.25:choices.remove(self.lanes[-1])
            self.lanes.append(rng.choice(choices))
        self.event=Clock.schedule_interval(self.tick,1/60)
    def pos_y(self,i,now=None): return .16+(self.times[i]-(self.app.game_elapsed(self.start) if now is None else now))*.56
    def tick(self,dt):
        if self.dead:return
        now=self.app.game_elapsed(self.start)
        while self.index<len(self.lanes) and now-self.times[self.index]>.16:
            self.misses+=1; self.combo=0; self.index+=1
            if not self.app.local_audio and not self.app.music:self.finish(False); return
        if self.index>=len(self.lanes):
            if not self.app.music or now>=self.app.music.length-.15:self.finish(True)
            return
        self.canvas.clear(); x,y=self.pos; w,h=self.size
        with self.canvas:
            Color(*BG); Rectangle(pos=self.pos,size=self.size)
            for k in range(4):
                Color(.08,.14,.23,1); RoundedRectangle(pos=(x+k*w/4+3,y+2),size=(w/4-6,h-4),radius=[dp(9)])
                if self.flash[k]>time.monotonic():
                    Color(.20,.87,.83,.30); RoundedRectangle(pos=(x+k*w/4+3,y),size=(w/4-6,h*.26),radius=[dp(8)])
            Color(.12,.8,.75,.14); Rectangle(pos=(x,y+.10*h),size=(w,.12*h))
            Color(*CYAN); Line(points=[x,y+.16*h,x+w,y+.16*h],width=2)
            for i in range(self.index,min(len(self.lanes),self.index+25)):
                cy=self.pos_y(i,now)
                if not 0<=cy<=1:continue
                px=x+self.lanes[i]*w/4+4; py=y+cy*h-.035*h
                Color(*GOLD); RoundedRectangle(pos=(px,py),size=(w/4-8,.055*h),radius=[dp(7)])
                Color(.99,.89,.58,1); RoundedRectangle(pos=(px+4,py+3),size=(w/4-16,.055*h-6),radius=[dp(5)])
    def on_touch_down(self,touch):
        if self.dead or not self.collide_point(*touch.pos):return super().on_touch_down(touch)
        if self.index>=len(self.lanes):return True
        lane=min(3,max(0,int((touch.x-self.x)/(self.width/4))))
        now=self.app.game_elapsed(self.start)
        error=now-self.times[self.index]
        if lane==self.lanes[self.index] and abs(error)<=.16:
            self.app.play_note(self.index); self.index+=1; self.score+=10; self.combo+=1
            self.flash[lane]=time.monotonic()+.12
            self.app.score_label.text=f'Ұпай: {self.score}    •    COMBO {self.combo}'
        elif not self.app.music:self.finish(False)
        else:self.combo=0
        return True
    def finish(self,won):
        if self.dead:return
        self.dead=True; self.event.cancel(); self.app.finished(self.score,won)
class Kui(App):
    def build(self):
        self.title='KÜI'; self.path=Path(self.user_data_dir)/'settings.json'; self.path.parent.mkdir(parents=True,exist_ok=True)
        try:self.data=json.loads(self.path.read_text(encoding='utf8'))
        except Exception:self.data={}
        self.player=self.data.get('player','Ойыншы'); self.url=self.data.get('url',''); self.volume=self.data.get('volume',.7); self.interval=.66; self.song='aday'; self.records=self.data.get('records',{}); self.room=None; self.poll=None; self.board=None; self.pending=False; self.sound=None; self.music=None; self.local_audio=False; self.audio_uris=self.data.get('audio_uris',{}); self.audio_uris.setdefault('aday',self.data.get('aday_uri','')); self.session=0
        self.root_box=ThemeRoot(orientation='vertical',padding=dp(16),spacing=dp(7)); self.menu(); return self.root_box
    def save(self):self.path.write_text(json.dumps({'player':self.player,'url':self.url,'volume':self.volume,'records':self.records,'audio_uris':self.audio_uris},ensure_ascii=False),encoding='utf8')
    def clear(self,title):
        self.root_box.clear_widgets()
        if title=='Домбыра  •  ырғақ ойыны':
            self.root_box.add_widget(Brand(size_hint_y=None,height=dp(88)))
        self.label('K Ü I',34,46,GOLD); self.label(title,19,35,CYAN)
    def label(self,text,size=16,height=38,color=(.92,.94,.98,1)):
        a=Label(text=text,font_size=dp(size),color=color,size_hint_y=None,height=dp(height),halign='center',valign='middle'); a.bind(size=lambda w,s:setattr(w,'text_size',s)); self.root_box.add_widget(a); return a
    def button(self,text,fn):
        b=Button(text=text,font_size=dp(16),size_hint_y=None,height=dp(49),background_normal='',background_down='',background_color=(0,0,0,0),color=(.94,.96,1,1))
        with b.canvas.before:
            c=Color(*PANEL); shape=RoundedRectangle(pos=b.pos,size=b.size,radius=[dp(12)])
            Color(.17,.39,.47,1); outline=Line(rounded_rectangle=(*b.pos,*b.size,dp(12)),width=1)
        def resize(*_):
            shape.pos=b.pos; shape.size=b.size; outline.rounded_rectangle=(*b.pos,*b.size,dp(12))
        b.bind(pos=resize,size=resize)
        b.bind(on_press=lambda *_:Animation(rgba=(.12,.42,.46,1),d=.07).start(c))
        def release(*_):
            Animation(rgba=PANEL,d=.16).start(c); fn()
        b.bind(on_release=release); self.root_box.add_widget(b); return b
    def leave(self):
        self.stop_music()
        self.session+=1
        if self.poll:self.poll.cancel(); self.poll=None
        if self.board and not self.board.dead:self.board.dead=True; self.board.event.cancel()
        self.board=None; self.room=None; self.pending=False
    def menu(self):
        self.leave(); self.clear('Домбыра  •  ырғақ ойыны'); self.button('Ойнау / Күй таңдау',lambda:self.choose('solo')); self.button('Онлайн дуэль',lambda:self.choose('duel')); self.button('Доспен жарысу',self.friend); self.button('Әлемдік рейтинг',lambda:self.choose('rank')); self.button('Профиль және баптаулар',self.settings); self.root_box.add_widget(Widget(size_hint_y=1)); footer=self.label('orazaly',11,22,(.76,.83,.88,1)); footer.halign='left'
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
        if platform=='android':
            self.button('Күйдің MP3 файлын таңдау',self.pick_aday)
            self.label('Жазба сақталған • қайта таңдау қажет емес' if self.audio_uris.get(self.song) else 'Аудиожазбаны бір рет таңдаңыз',13,35)
        for name,v in [('Жеңіл',.88),('Орташа',.66),('Қиын',.48)]:self.button(name,lambda v=v:self.start_game(v))
        self.button('Артқа',lambda:self.choose('solo'))
    def pick_aday(self):
        selected_song=self.song
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
                    self.audio_uris[selected_song]=value; self.save(); self.difficulty()
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
        if platform=='android' and self.audio_uris.get(self.song) and not self.room:
            try:
                self.music=AndroidTrack(self.audio_uris[self.song],self.volume)
                self.local_audio=True
                return
            except Exception:
                self.opponent.text='MP3 ашылмады. Сынақ дыбысы.'
        path=next((BASE/'assets'/f'{self.song}.{ext}' for ext in ('wav','mp3') if (BASE/'assets'/f'{self.song}.{ext}').is_file()),BASE/'assets'/f'{self.song}.wav')
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
            if self.song=='aday' and abs(self.music.length-127.707)<.5:
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
