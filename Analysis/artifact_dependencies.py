import pandas as pd
from collections import defaultdict, Counter
from deepdiff import DeepDiff
from itertools import product

all_artifacts = pd.read_csv('artifactmodel/data/01_activities_artifacts.csv', delimiter=';')
aggregated_artifacts = pd.read_csv('artifactmodel/data/02_artifacts_aggregated.csv', delimiter=';')
all_artifacts = all_artifacts[all_artifacts['Type (Activity/Artifact)'] == 'artifact']
def filter_irrelevant(row):
    if row['Paper Title'] in set(aggregated_artifacts['Reference']):
        return True
    return False 

all_artifacts = all_artifacts[all_artifacts.apply(filter_irrelevant, axis=1)]

## Left here for completeness, yields results which were manually checked. These missmatches are due to multiple references in the reference field of the aggregated file
# Ensure all artifacts are matched
#for row in all_artifacts.itertuples(index=False):
#   relevant_artifact = aggregated_artifacts[(aggregated_artifacts['Artifact'] == row.Name) & (aggregated_artifacts['Reference'] == row._1)]
#   if relevant_artifact.shape[0] == 0:
#       print(row)

#for row in aggregated_artifacts.itertuples():
#    relevant_artifact = all_artifacts[(all_artifacts['Name'] == row.Artifact) & (all_artifacts['Paper Title'] == row.Reference)]
#    if relevant_artifact.shape[0] == 0:
#        print(row)
#

new_aggregation = aggregated_artifacts.groupby(['Artifact', 'Reference'])[['Input/Intermediate/Output', 'Activity Category']]
dependencies = []
print('---------Raw Dependencies:')
for name, cats in new_aggregation:
    after = cats[cats['Input/Intermediate/Output'] == 'Input']['Activity Category'].values
    before = cats[cats['Input/Intermediate/Output'] == 'Output']['Activity Category'].values
    combinations = list(product(before, after))
    dependencies.extend(combinations)
    if len(combinations):
        print(name[0], list(combinations))

print('\n---------Summary:\n')

print(Counter(dependencies))
