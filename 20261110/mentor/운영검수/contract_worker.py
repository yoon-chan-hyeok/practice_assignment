"""교안 계약 검수. 테스트는 임시 JSON만 변경하며 실제 데이터를 보존한다."""
import sys, json, tempfile, importlib, traceback
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient


def run(project: Path, config: dict, mode: str = 'complete') -> dict:
    sys.path.insert(0, str(project))
    checks=[]
    def check(name, condition, detail=None):
        if not condition:
            raise AssertionError(f'{name}: {detail}')
        checks.append(name)
    module=importlib.import_module(config['module'].split(':')[0])
    app=getattr(module,config['module'].split(':')[1])
    actual_file=project/'data'/'knowledge.json'
    original=actual_file.read_bytes() if actual_file.exists() else None
    with tempfile.TemporaryDirectory(prefix='day17_contract_') as temp:
        data_file=Path(temp)/'knowledge.json'
        seed={'next_id':4,'entries':[
            {'id':1,'title':'가상환경','content':'프로젝트별 패키지를 분리한다.','category':'setup'},
            {'id':2,'title':'서버 실행','content':'uvicorn으로 개발 서버를 켠다.','category':'api'},
            {'id':3,'title':'입력 오류','content':'422이면 입력값을 확인한다.','category':'api'}]}
        def reset(): data_file.write_text(json.dumps(seed,ensure_ascii=False,indent=2),encoding='utf-8')
        def state(): return json.loads(data_file.read_text(encoding='utf-8'))
        storage=None
        if config.get('storage'):
            storage=importlib.import_module(config['storage']); storage.DATA=data_file; reset()
        with TestClient(app, raise_server_exceptions=False) as client:
            check('docs_200',client.get('/docs').status_code==200)
            doc=client.get('/openapi.json')
            check('openapi_200',doc.status_code==200)
            check('openapi_is_json',isinstance(doc.json().get('paths'),dict))
            if mode=='student':
                check('student_no_startup_data_write',not storage or state()==seed)
            else:
                r=client.get('/health')
                check('health_status',r.status_code==200,r.text)
                check('health_body',r.json()=={'status':'ok'},r.text)
                if config['level']=='A':
                    r=client.get('/hello',params={'name':'민준'})
                    check('hello_query',r.json()=={'message':'안녕하세요, 민준'},r.text)
                stage=config['step']
                paths=doc.json()['paths']
                if stage>=2:
                    before=data_file.read_bytes()
                    r=client.get('/api/knowledge')
                    check('list_200',r.status_code==200,r.text)
                    check('list_content',r.json()==seed['entries'],r.text)
                    check('list_content_type',r.headers['content-type'].startswith('application/json'))
                    check('list_no_next_id',all('next_id' not in x for x in r.json()))
                    r=client.get('/api/knowledge/2')
                    check('detail_200',r.status_code==200)
                    check('detail_matches_file',r.json()==seed['entries'][1],r.text)
                    check('detail_absent_404',client.get('/api/knowledge/9999').status_code==404)
                    check('detail_absent_body',client.get('/api/knowledge/9999').json()=={'detail':'Knowledge not found'})
                    check('path_type_422',client.get('/api/knowledge/foo').status_code==422)
                    if config.get('filter'):
                        r=client.get('/api/knowledge',params={'category':'api'})
                        check('filter_exact',[x['id'] for x in r.json()]==[2,3])
                        check('filter_absent_200',client.get('/api/knowledge',params={'category':'unknown'}).status_code==200)
                        check('filter_absent_empty',client.get('/api/knowledge',params={'category':'unknown'}).json()==[])
                        check('filter_empty_string',client.get('/api/knowledge',params={'category':''}).json()==[])
                    check('get_preserves_file',data_file.read_bytes()==before)
                if stage>=3:
                    reset()
                    good={'title':'실습 환경 안내','content':'가상환경의 Python을 선택합니다.','category':'learning'}
                    r=client.post('/api/knowledge',json=good)
                    check('create_201',r.status_code==201,r.text)
                    check('create_fields',r.json()==dict(good,id=4),r.text)
                    check('create_count',len(state()['entries'])==4)
                    check('create_next_id',state()['next_id']==5)
                    check('create_file_payload',state()['entries'][-1]==r.json())
                    check('create_readback',client.get('/api/knowledge/4').json()==r.json())
                    check('response_keys',set(r.json())=={'id','title','content','category'})
                    for key,lim in [('title',80),('content',2000),('category',30)]:
                        for suffix,payload in [('missing',{k:v for k,v in good.items() if k!=key}),('empty',dict(good,**{key:''})),('over',dict(good,**{key:'가'*(lim+1)}))]:
                            before=data_file.read_bytes()
                            rr=client.post('/api/knowledge',json=payload)
                            check(f'post_{key}_{suffix}_422',rr.status_code==422,rr.text)
                            check(f'post_{key}_{suffix}_preserve',data_file.read_bytes()==before)
                    before=data_file.read_bytes()
                    rr=client.post('/api/knowledge',content='{"title":',headers={'Content-Type':'application/json'})
                    check('bad_json_422',rr.status_code==422)
                    check('bad_json_preserve',data_file.read_bytes()==before)
                    rr=client.post('/api/knowledge',json={'title':'가'*80,'content':'가'*2000,'category':'가'*30})
                    check('max_lengths_accepted',rr.status_code==201,rr.text)
                    reset()
                    rr=client.post('/api/knowledge',json=dict(good,id=999,next_id=999,ignored='x'))
                    check('server_owns_id',rr.status_code==201 and rr.json()['id']==4)
                    check('ignored_extra_not_exposed',set(rr.json())=={'id','title','content','category'})
                    reset()
                    rr=client.post('/api/knowledge',json={'title':' ','content':' ','category':' '})
                    check('whitespace_policy_matches_ppt',rr.status_code==201)
                    reset()
                if stage>=4:
                    good={'title':'서버 실행','content':'서버를 새 명령으로 확인합니다.','category':'api'}
                    before_state=state()
                    r=client.put('/api/knowledge/2',json=good)
                    check('put_200',r.status_code==200,r.text)
                    check('put_fields_id',r.json()==dict(good,id=2))
                    check('put_readback',client.get('/api/knowledge/2').json()==r.json())
                    check('put_count',len(state()['entries'])==3)
                    check('put_next_id',state()['next_id']==4)
                    check('put_other_records',state()['entries'][0]==before_state['entries'][0] and state()['entries'][2]==before_state['entries'][2])
                    after=state()
                    r=client.put('/api/knowledge/2',json=good)
                    check('put_twice_stable',r.status_code==200 and state()==after)
                    before=data_file.read_bytes()
                    check('put_missing_404',client.put('/api/knowledge/9999',json=good).status_code==404)
                    check('put_missing_preserve',data_file.read_bytes()==before)
                    check('put_partial_422',client.put('/api/knowledge/2',json={'content':'본문만'}).status_code==422)
                    check('put_partial_preserve',data_file.read_bytes()==before)
                    check('put_bad_path_422',client.put('/api/knowledge/foo',json=good).status_code==422)
                    check('put_bad_path_preserve',data_file.read_bytes()==before)
                    reset()
                if stage>=5:
                    before=state()
                    r=client.delete('/api/knowledge/2')
                    check('delete_204',r.status_code==204,r.text)
                    check('delete_no_body',r.content==b'')
                    check('deleted_get_404',client.get('/api/knowledge/2').status_code==404)
                    check('delete_other_records',state()['entries']==[x for x in before['entries'] if x['id']!=2])
                    check('delete_next_id',state()['next_id']==before['next_id'])
                    frozen=data_file.read_bytes()
                    check('delete_again_404',client.delete('/api/knowledge/2').status_code==404)
                    check('delete_absent_preserve',data_file.read_bytes()==frozen)
                    check('delete_bad_path_422',client.delete('/api/knowledge/foo').status_code==422)
                    check('delete_bad_path_preserve',data_file.read_bytes()==frozen)
                    rr=client.put('/api/knowledge/3',json={'title':'세 번째 항목','content':'ID는 3, 위치는 1입니다.','category':'api'})
                    check('index_not_id',rr.status_code==200 and state()['entries'][1]['id']==3)
                    check('delete_last_id',client.delete('/api/knowledge/3').status_code==204)
                    rr=client.post('/api/knowledge',json={'title':'새 지식','content':'새 내용','category':'x'})
                    check('id_not_reused',rr.status_code==201 and rr.json()['id']==4)
                    check('routes_contract',{'get','post'}<=set(paths['/api/knowledge']) and {'get','put','delete'}<=set(paths['/api/knowledge/{knowledge_id}']))
                    reset()
                if stage>=3:
                    before=data_file.read_bytes()
                    with patch.object(Path,'replace',side_effect=OSError('검수용 저장 실패')):
                        r=client.post('/api/knowledge',json={'title':'실패','content':'저장 실패 검수','category':'qa'})
                    check('write_failure_not_success',r.status_code==500)
                    check('write_failure_preserve',data_file.read_bytes()==before)
                    check('temp_removed',not data_file.with_suffix('.tmp').exists())
                if stage>=2:
                    damaged=b'{invalid'
                    data_file.write_bytes(damaged)
                    r=client.get('/api/knowledge')
                    check('invalid_file_not_empty_success',r.status_code==500)
                    check('invalid_file_not_overwritten',data_file.read_bytes()==damaged)
                    reset()
        if original is not None: check('real_file_untouched',actual_file.read_bytes()==original)
    return {'status':'passed','project':str(project),'mode':mode,'level':config['level'],'step':config['step'],'checks':checks,'check_count':len(checks)}

if __name__=='__main__':
    try:
        result=run(Path(sys.argv[1]).resolve(),json.loads(sys.argv[2]),sys.argv[3] if len(sys.argv)>3 else 'complete')
    except Exception as exc:
        result={'status':'failed','error':str(exc),'traceback':traceback.format_exc()}
    print(json.dumps(result,ensure_ascii=False))
    raise SystemExit(0 if result['status']=='passed' else 1)
