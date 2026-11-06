import pathlib,json,sys,hashlib
p=pathlib.Path(__file__).parent;m=json.loads((p/'input-manifest.json').read_text()); files=[m['summary_path']]+[x['path'] for x in m['sources']]; path=pathlib.Path(files[int(sys.argv[1])]) if sys.argv[1].isdigit() else p/sys.argv[1];s=path.read_text(); n=int(sys.argv[2]); a=n*5000;b=min(a+5000,len(s));assert a<len(s)
r={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'characters':len(s),'slice':n,'start':a,'end':b,'delivered_characters':b-a,'status':'complete_output_attempt'}
with (p/'delivery-attempts.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
print(s[a:b],end='')
