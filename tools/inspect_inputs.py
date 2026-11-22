"""Read-only integrity check for synthetic input files."""
from pathlib import Path
import hashlib
import json
def inspect(root):
    root=Path(root)
    catalog=json.loads((root/"data/catalog.json").read_text(encoding="utf-8"))
    result={}
    for name,meta in catalog["tables"].items():
        payload=(root/"data"/(name+".jsonl")).read_bytes()
        if hashlib.sha256(payload).hexdigest()!=meta["sha256"]:
            raise ValueError("sha256 mismatch: "+name)
        rows=[json.loads(x) for x in payload.decode("utf-8").splitlines() if x]
        if len(rows)!=meta["count"]:
            raise ValueError("row count mismatch: "+name)
        keys=set(meta["fields"])
        pk=meta["primary_key"]
        seen=set()
        for row in rows:
            if set(row)!=keys:
                raise ValueError("field mismatch: "+name)
            value=tuple(json.dumps(row[k],ensure_ascii=False,sort_keys=True) for k in pk)
            if value in seen:
                raise ValueError("duplicate primary key: "+name)
            seen.add(value)
        result[name]=len(rows)
    return result
if __name__=="__main__":
    print(json.dumps(inspect(Path(__file__).resolve().parents[1]),ensure_ascii=False,sort_keys=True))
