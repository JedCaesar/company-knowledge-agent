from __future__ import annotations
import json, math, re, sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

STOP={"a","an","and","are","as","at","be","by","do","for","from","how","i","in","is","it","of","on","or","the","to","what","when","where","who","with"}
def tokens(text): return [x for x in re.findall(r"[a-z0-9]+",text.lower()) if x not in STOP]

@dataclass(frozen=True)
class Document:
    id:str; title:str; content:str; source:str

class KnowledgeBase:
    def __init__(self,docs):
        self.docs=docs; self.vec=[Counter(tokens(d.content)) for d in docs]
        df=Counter(t for v in self.vec for t in v); n=len(docs)
        self.idf={t:math.log((n+1)/(c+1))+1 for t,c in df.items()}
    @classmethod
    def load(cls,path="company_handbook.json"):
        return cls([Document(**x) for x in json.loads(Path(path).read_text())])
    def weight(self,v): return {t:c*self.idf.get(t,1) for t,c in v.items()}
    def search(self,q):
        qv=self.weight(Counter(tokens(q))); ranked=[]
        for d,v in zip(self.docs,self.vec):
            dv=self.weight(v); dot=sum(x*dv.get(t,0) for t,x in qv.items())
            norm=math.sqrt(sum(x*x for x in qv.values())*sum(x*x for x in dv.values()))
            ranked.append((d,dot/norm if norm else 0))
        ranked.sort(key=lambda x:x[1],reverse=True)
        if not ranked or not ranked[0][1]: return []
        return [x for x in ranked[:3] if x[1]>=max(.05,ranked[0][1]*.75)]

class CompanyAgent:
    intents={"leave_request":("leave","vacation","holiday"),"expense_claim":("expense","receipt","claim"),"security_help":("password","phishing","security")}
    def __init__(self,kb): self.kb=kb
    def answer(self,message):
        intent=next((n for n,terms in self.intents.items() if any(t in message.lower() for t in terms)),"knowledge_search")
        found=self.kb.search(message)
        if not found: return {"answer":"I could not find a supported answer in the company knowledge base.","intent":intent,"confidence":0,"citations":[]}
        return {"answer":" ".join(re.split(r"(?<=[.!?])\s+",d.content)[0] for d,_ in found),"intent":intent,"confidence":round(sum(s for _,s in found)/len(found),3),"citations":[d.source for d,_ in found]}

if __name__=="__main__":
    q=" ".join(sys.argv[1:]) or "How do I submit an expense claim?"
    print(json.dumps(CompanyAgent(KnowledgeBase.load()).answer(q),indent=2))
