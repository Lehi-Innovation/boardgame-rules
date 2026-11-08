"""Bind failed current18 originals, all primary labels, quotes, and ONE neutral."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
V=ROOT/'docs/quality/summary-qa/root'/B.name/'current-snapshot-revalidation-2026-11-07';D=V/'iteration-01'
J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
C=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
q={x['id']:x for x in J(D/'questions.json')['questions']};key={x['id']:x for x in J(D/'answer-key.json')['answers']}
body=(D/'summary-snapshot.md').read_text();raw={w:{x['id']:x for x in J(D/('reader-'+w+'.json'))['answers']} for w in 'ab'}
freeze=J(D/'raw-output-manifest.json');early=J(D/'grading-chronology-deviation.json')
for w in 'ab':
    f=freeze['readers'][w];assert H(Path(f['path']))==f['sha256']==H(Path(f['exact_original_copy']))==f['copy_sha256'] and f['answer_count']==81
    assert list(raw[w])==list(q)
for path,digest in early['existing_primary_grade_files'].items():assert H(Path(path))==digest
for path,digest in freeze['existing_prefix_primary_labels_preserved'].items():assert H(Path(path))==digest
counts={w:Counter() for w in 'ab'};seen=set();reports=[];quote_count=0
for p in sorted((D/'primary-grades').glob('*.json')):
    x=J(p);w,i=x['reader'],x['id'];assert (w,i) not in seen and x['question']==q[i] and x['expected']==key[i]
    assert x['observed_original_entry']==raw[w][i] and x['observed_entry_sha256']==C(raw[w][i])
    assert x['every_substantive_field_reviewed'] and x['whole_entry_policy']
    assert x['grade'] in ['correct','partial','incorrect','borderline']
    for passage in raw[w][i]['source_passages']:
        quote=passage['quotation'];assert quote and quote in body;quote_count+=1
    counts[w][x['grade']]+=1;seen.add((w,i));reports.append({'path':str(p),'sha256':H(p),'reader':w,'id':i,'primary_grade':x['grade']})
assert seen=={(w,i) for w in 'ab' for i in q}
packet_path=D/'neutral-adjudication-input.json';packet=J(packet_path);np=D/'neutral-adjudication.json';neutral=J(np)
assert neutral['summary_sha256']==H(D/'summary-snapshot.md') and neutral['adjudication_input_sha256']==H(packet_path)
cases={x['case_id']:x for x in packet['cases']};assert set(cases)=={'a-Q52','b-Q73'}
effective={w:Counter(c) for w,c in counts.items()}
for case_id,case in cases.items():
    w,i=case_id.split('-');assert case['question']==q[i] and case['fixed_key']==key[i] and case['complete_original_entry']==raw[w][i]
for x in neutral['cases']:
    w,i=x['case_id'].split('-');assert x['case_id'] in cases and x['grade']=='correct'
    original=J(D/'primary-grades'/f'{w}-{i}.json');assert original['grade']=='borderline'
    effective[w]['borderline']-=1;effective[w]['correct']+=1
assert len(neutral['cases'])==2
scores=lambda d:{w:{label:c[label] for label in ['correct','partial','incorrect','borderline']} for w,c in d.items()}
assert effective['a']['correct']==79 and effective['a']['partial']==2 and effective['b']['correct']==81 and not any(effective[w][label] for w in 'ab' for label in ['incorrect','borderline'])
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'N':81,'complete_original_entries':162,'all_fixed_Q_and_prose_key_records_exact':True,'all162_original_entry_hashes_and_full_fields_bound':True,'exact_nonempty_same_entry_source_quotations':quote_count,'primary_scores':scores(counts),'one_neutral_effective_scores':scores(effective),'reports':reports,'raw_hashes':{w:H(D/('reader-'+w+'.json')) for w in 'ab'},'one_neutral_report_sha256':H(np),'one_neutral_packet_sha256':H(packet_path),'semantic_acceptance':{'A_Q03':'True omission: broad battle procedure from ambush to removal lacks both before-roll and after-roll effects, in all its fields and chosen quotations. Merely naming six steps does not supply those omitted stages.','A_Q04':'True omission: broad crafting cost/reuse asks include the core Vagabond exception. Its hammer payment, pawn reactivation and all-icon suit restriction are absent from the whole entry. No invented name/paraphrase gate.','A_Q52':'Fresh neutral reasonably interprets imprecise cost shorthand in context of exact Exhaust hammer instruction; it never expressly permits an already exhausted item. All literal asked Rest/Refresh/Repair outcomes supplied.','B_Q73':'Fresh neutral interprets trailing base-clearing phrase as the matching-card prerequisite rather than an explicit map placement. The complete entry names Officers box and gives exact base-card condition; no definite material false instruction established.'},'pair_verdict':'FAIL','technical_qualifications':['Prefixgrading chronology preserved with all early hashes unchanged; no readerfeedback or target edits. All complete originals frozen before remaining grading.','B initial first-five mid-turn draft was self-expanded before first completed turn or factual grading; both partial drafts preserved. Not another completed81 attempt.','Parent may evaluate/repair per localQAguide; pure source audit is a different fresh actor.'],'limits':['Neutral actual input/model verification separate. No new vote or grade resampling.','Source accuracy audit unchanged currentda0 is separate from failed reader performance; NEW entire81 pair required.','No publication or goal-complete approval.']}
out=B/'coordinator-checks/root-current18-primary-and-one-neutral-integrity.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'entries':162,'exact_source_quotes':quote_count,'primary':scores(counts),'effective':scores(effective),'proof':str(out)}))
