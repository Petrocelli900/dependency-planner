"""Plan deterministic execution waves for a JSON dependency graph."""
import argparse
import json
import sys

class CycleError(ValueError):
    def __init__(self,blocked):
        self.blocked=tuple(sorted(blocked))
        super().__init__('Cycle detected; blocked tasks: '+', '.join(self.blocked))

def plan(graph):
    if not isinstance(graph,dict): raise ValueError('Graph must be an object')
    if any(not isinstance(name,str) or not name.strip() for name in graph):
        raise ValueError('Names must be nonblank strings')
    normalized={}
    for name,deps in graph.items():
        if not isinstance(deps,list) or any(not isinstance(dep,str) for dep in deps):
            raise ValueError('Dependencies must be lists of names')
        if any(dep not in graph for dep in deps): raise ValueError('Unknown dependency for '+name)
        normalized[name]=set(deps)
    indegree={name:len(deps) for name,deps in normalized.items()}
    followers={name:set() for name in graph}
    for name,deps in normalized.items():
        for dep in deps: followers[dep].add(name)
    ready=sorted(name for name,degree in indegree.items() if degree==0)
    waves=[]; processed=0
    while ready:
        wave=ready; ready=[]; waves.append(wave); processed+=len(wave)
        for name in wave:
            for follower in followers[name]:
                indegree[follower]-=1
                if indegree[follower]==0: ready.append(follower)
        ready.sort()
    if processed!=len(graph): raise CycleError(name for name,degree in indegree.items() if degree>0)
    return {'waves':waves,'order':[name for wave in waves for name in wave]}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('graph')
    args=parser.parse_args(argv)
    try:
        with open(args.graph,encoding='utf-8') as stream: graph=json.load(stream)
        result=plan(graph)
    except (OSError,ValueError,TypeError) as error:
        print(str(error),file=sys.stderr); return 2
    print(json.dumps(result,indent=2,ensure_ascii=False)); return 0

if __name__=='__main__': sys.exit(main())
