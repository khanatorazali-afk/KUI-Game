"""Prototype leaderboard and invitation-code duels. Run: python server.py"""
import json, sqlite3, time, threading, secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
DB=Path(__file__).with_name('scores.db'); LOCK=threading.Lock(); ROOMS={}
SONGS={'aday','balbyrauyn','saryarka','konyil','erke','aksak','kishkentai'}
def db():
    c=sqlite3.connect(DB); c.execute('CREATE TABLE IF NOT EXISTS scores(song TEXT, player TEXT, score INTEGER, PRIMARY KEY(song,player))'); return c
class Handler(BaseHTTPRequestHandler):
    def send(self,data,status=200):
        raw=json.dumps(data,ensure_ascii=False).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        u=urlparse(self.path); q=parse_qs(u.query)
        if u.path=='/scores':
            with db() as c: rows=c.execute('SELECT player,score FROM scores WHERE song=? ORDER BY score DESC,player LIMIT 50',(q.get('song',['aday'])[0],)).fetchall()
            return self.send({'scores':rows})
        return self.send({'error':'not found'},404)
    def do_POST(self):
        try:
            n=int(self.headers.get('Content-Length',0)); assert 0<n<8192; p=json.loads(self.rfile.read(n)); song=p.get('song','aday'); name=str(p.get('player','')).strip()[:24]; assert song in SONGS and name
            score=p.get('score',0); assert type(score) is int and 0<=score<=2000
            if self.path=='/scores':
                with db() as c: c.execute('INSERT INTO scores VALUES(?,?,?) ON CONFLICT(song,player) DO UPDATE SET score=max(score,excluded.score)',(song,name,score))
                return self.send({'ok':True})
            with LOCK:
                now=time.time()
                for k in list(ROOMS):
                    if now-ROOMS[k]['created']>3600: del ROOMS[k]
                if self.path=='/room':
                    code=p.get('code','').upper(); mode=p.get('mode','create'); token=secrets.token_hex(16)
                    if mode=='random':
                        code=next((k for k,r in ROOMS.items() if r['song']==song and len(r['players'])==1 and r['public']), '')
                    if mode=='create' or (mode=='random' and not code):
                        code=secrets.token_hex(3).upper(); ROOMS[code]={'song':song,'players':{},'start':None,'public':mode=='random','created':now}
                    r=ROOMS.get(code); assert r and len(r['players'])<2
                    r['players'][token]={'name':name,'score':0,'done':False}
                    if len(r['players'])==2: r['start']=now+5
                    return self.send({'code':code,'token':token,'song':r['song']})
                if self.path=='/state':
                    r=ROOMS.get(p.get('code')); assert r and p.get('token') in r['players']; me=r['players'][p['token']]
                    if r['start'] and now>=r['start'] and not me['done']:
                        me['score']=max(me['score'],score); me['done']=bool(p.get('done',False))
                    return self.send({'start':r['start'],'now':now,'players':list(r['players'].values())})
            self.send({'error':'not found'},404)
        except (ValueError,TypeError,AssertionError,KeyError,AttributeError): self.send({'error':'invalid request or room unavailable'},400)
if __name__=='__main__':
    print('KUI prototype server: port 8080'); ThreadingHTTPServer(('0.0.0.0',8080),Handler).serve_forever()
