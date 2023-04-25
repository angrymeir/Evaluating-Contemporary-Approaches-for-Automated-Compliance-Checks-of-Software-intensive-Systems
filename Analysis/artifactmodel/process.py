from graphlib import TopologicalSorter
from collections import defaultdict

def generate_activity_graph(activities):
    ts = TopologicalSorter()
    for activity in activities:
        if activity['Type (Activity/Artifact)'] == 'activity':
            predecessors = set()
            if activity['Predecessor (if activity)'] in ['--', '—']:
               #print(activity)
               ts.add(activity['Name'])
               #pass
            else:
               raw_predecessors = activity['Predecessor (if activity)'].split(',')
               for predecessor in raw_predecessors:
                   ts.add(activity['Name'], predecessor.strip())
    ts.prepare()
    return ts

def filter_artifacts(activities_artifacts):
    return list(filter(lambda x: x['Type (Activity/Artifact)'] == 'artifact', activities_artifacts))