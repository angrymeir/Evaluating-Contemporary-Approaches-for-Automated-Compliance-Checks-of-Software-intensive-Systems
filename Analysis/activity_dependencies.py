import pandas as pd
from collections import defaultdict
from deepdiff import DeepDiff

all_activities = pd.read_csv('artifactmodel/data/01_activities_artifacts.csv', delimiter=';')
aggregated_activities = pd.read_csv('artifactmodel/data/01_activities_aggregated.csv', delimiter=';')
all_activities = all_activities[all_activities['Type (Activity/Artifact)'] == 'activity']
def filter_irrelevant(row):
    if row['Paper Title'] in set(aggregated_activities['Reference']):
        return True
    return False 

all_activities = all_activities[all_activities.apply(filter_irrelevant, axis=1)]

# Ensure all activities are matched
for row in all_activities.itertuples(index=False):
   relevant_activity = aggregated_activities[(aggregated_activities['Activity'] == row.Name) & (aggregated_activities['Reference'] == row._1)]
   if relevant_activity.shape[0] == 0:
       print(row)

for row in aggregated_activities.itertuples():
    relevant_activity = all_activities[(all_activities['Name'] == row.Activity) & (all_activities['Paper Title'] == row.Reference)]
    if relevant_activity.shape[0] == 0:
        print(row)

# Generate graph
forward_graph = defaultdict(list)
backward_graph = defaultdict(list)
for row in aggregated_activities.itertuples():
    relevant_activity = all_activities[(all_activities['Name'] == row.Activity) & (all_activities['Paper Title'] == row.Reference)]
    successors = relevant_activity['Successor (if activity)']
    predecessors = relevant_activity['Predecessor (if activity)']
    for successor in successors.values[0].split(','):
        cur_successor = aggregated_activities[(aggregated_activities['Activity'] == successor.strip()) & (aggregated_activities['Reference'] == row.Reference)]
        if cur_successor.shape[0]:
            forward_graph[(row.Category, cur_successor['Category'].values[0])].append(row.Activity)
    for predecessor in predecessors.values[0].split(','):
        cur_predec = aggregated_activities[(aggregated_activities['Activity'] == predecessor.strip()) & (aggregated_activities['Reference'] == row.Reference)]
        if cur_predec.shape[0]:
            backward_graph[(cur_predec['Category'].values[0], row.Category)].append(cur_predec['Activity'].values[0])

print('Diff between forward and backward graph:', DeepDiff(forward_graph, backward_graph, ignore_order=True), '\n\n')
print('Forward graph:', forward_graph, '\n\n')
print('Backward graph:', backward_graph)
