from pathlib import Path
import hashlib,json
B=Path(__file__).parent.resolve();I=B/'expanded-luna-iteration-01';K=B/'expanded-candidate-v7';G=I/'grading'
issues={
('a','Q13'):'Does the binding-status sentence, read in the actual disputed-binding question and complete entry, make a material overbroad claim or accurately answer that case?',
('b','Q26'):'Does the complete entry actually decide the stated numerical capital comparison, or leave it as an unevaluated conditional? Apply the explicit actual-case/result rule.',
('b','Q28'):'Does the complete entry correctly distinguish the owner’s own proposal costs from another player’s proposal costs, and does its actor wording make a wrong interception assertion or leave a condition unresolved?',
('b','Q40'):'Who does the complete entry identify as making the choice after asset transfer? Resolve owner/user wording in its full operative context, without canceling an actual contradiction with a quote.',
('a','Q52'):'Does the complete entry answer the asked movement/path scope, including by semantically complete ordinary-lookup source text, or omit it?',
('b','Q52'):'Does the complete entry answer the asked movement/path scope, including by semantically complete ordinary-lookup source text, or omit it?',
('a','Q60'):'Does the complete entry supply the requested unit/token classification, with the fixed actual-clause scope, or leave a genuine classification omission? Do not require unasked priority/failed-placement resolution.',
('b','Q62'):'Are the supplied unrest transitions merely true generic context or an assertion of an unavailable result in this fixed outage-removal case? Does the actual requested concrete result appear?',
('a','Q73'):'Does the literal question require a numerical Root-threat magnitude or only whether movement can increase threat? Explicitly separate any genuine question/map scope defect from factual sufficiency. Do not silently rewrite a frozen map.',
('b','Q74'):'Does the complete entry actually supply the requested movement/Root procedure, or merely name a rule to be applied without giving its operative consequences?',
('b','Q78'):'Does the complete entry supply the requested normal hand-check timing relative to End of Turn abilities, or leave that order unresolved?',
('a','Q84'):'Does ordinary End of Turn wording and the complete operative quotation supply the asked use-frequency restriction, or is a genuinely requested frequency absent?',
('b','Q84'):'Does ordinary End of Turn wording and the complete operative quotation supply the asked use-frequency restriction, or is a genuinely requested frequency absent?'}
maps=[{x['id']:x for x in json.loads((p).read_text())[key]} if key else {x['id']:x for x in json.loads(p.read_text())} for p,key in [(I/'questions.json','questions'),(K/'answer-key.json','answers'),(K/'asked-clause-map.json',None)]]
raw={l:{x['id']:x for x in json.loads((I/f'reader-{l}.json').read_text())['answers']} for l in ['a','b']}
canon=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
ids=list(dict.fromkeys(i for l,i in issues));pack={'purpose':'ONE fresh whole-entry adjudication of13 genuine flagged borderline entries; no prior labels supplied','questions':[maps[0][i] for i in ids],'fixed_key':[maps[1][i] for i in ids],'fixed_asked_clause_map':[maps[2][i] for i in ids],'entries':[{'reader':l,'id':i,'review_question':v,'complete_raw_entry':raw[l][i],'raw_entry_sha256':hashlib.sha256(canon(raw[l][i])).hexdigest()} for (l,i),v in issues.items()],'scope_status':'preliminary/current-bank; essential SG01 authority pending, no invented ruling'}
p=G/'fresh-borderline-input.json';assert not p.exists();p.write_text(json.dumps(pack,indent=2,ensure_ascii=False)+'\n');(G/'fresh-borderline-input-manifest.json').write_text(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'entries':13,'prior_labels_in_input':False,'one_fresh_adjudicator_only':True},indent=2)+'\n');print(str(p));print('characters',len(p.read_text()))
