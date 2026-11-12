"""실습 구간 추출·주석/문자열 경계 검사. PostgreSQL 문법 파서는 아닙니다."""
from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Step:
    key: str
    expect: str
    capture: str
    reconnect: bool
    sql: str

HEADER=re.compile(r'^-- @step (\w+) expect=(\w+) capture=([\w-]+) reconnect=(true|false)\s*$',re.M)

def parse_steps(text: str) -> list[Step]:
    matches=list(HEADER.finditer(text));result=[]
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i+1<len(matches) else len(text)
        result.append(Step(m[1],m[2],m[3],m[4]=='true',text[m.end():end].strip()))
    if not result:raise ValueError('실행 구간 @step이 없습니다.')
    return result

def mask_sql(text: str, strings: bool=True) -> str:
    """주석/문자열을 공백으로 덮습니다. 닫힘 경계만 검사하며 SQL 의미는 판정하지 않습니다."""
    out=list(text);i=0;n=len(text)
    while i<n:
        start=i
        if text.startswith('--',i):
            j=text.find('\n',i);i=n if j<0 else j
        elif text.startswith('/*',i):
            i+=2;depth=1
            while i<n and depth:
                if text.startswith('/*',i):depth+=1;i+=2
                elif text.startswith('*/',i):depth-=1;i+=2
                else:i+=1
            if depth:raise ValueError('닫히지 않은 블록 주석')
        elif text[i] in "'\"":
            quote=text[i];i+=1
            while i<n:
                if text[i]==quote:
                    if i+1<n and text[i+1]==quote:i+=2;continue
                    i+=1;break
                i+=1
            else:raise ValueError('닫히지 않은 문자열/식별자')
            if not strings:continue
        elif text[i]=='$' and (m:=re.match(r'\$[A-Za-z_][A-Za-z_0-9]*\$|\$\$',text[i:])):
            tag=m[0];j=text.find(tag,i+len(tag))
            if j<0:raise ValueError('닫히지 않은 dollar quote')
            i=j+len(tag)
            if not strings:continue
        else:i+=1;continue
        for k in range(start,i):
            if out[k]!='\n':out[k]=' '
    return ''.join(out)

def capture_once(sql: str, prefix: str) -> str:
    """RETURNING을 gset으로 딱 한 번 전송. 세미콜론 뒤 재실행을 피합니다."""
    masked=mask_sql(sql);semis=[i for i,c in enumerate(masked) if c==';']
    if len(semis)!=1 or masked[semis[-1]+1:].strip():
        raise ValueError('capture 구간은 SQL 한 문장이어야 합니다.')
    i=semis[0]
    return sql[:i]+sql[i+1:]+'\n\\gset '+prefix+'\n'

def replace_runtime_ids(sql: str) -> str:
    for name in ['NEW_ID','A_ID','B_ID','C_ID']:
        sql=sql.replace('__'+name+'__',':'+name.lower())
    if re.search(r'__TODO_\w+__',mask_sql(sql,strings=False)):
        raise ValueError('미완성 SQL TODO가 남아 있습니다.')
    return sql
