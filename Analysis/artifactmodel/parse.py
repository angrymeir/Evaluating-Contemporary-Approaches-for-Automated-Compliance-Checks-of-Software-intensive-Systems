import csv
from collections import defaultdict


def __load_data(path):
    papers = defaultdict(list)
    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            papers[row['Paper Title']].append(row)
    return papers


def __load_aggregation_data(path):
    category = defaultdict(list)
    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            print(row)
            try:
                category[row['Category']].append(row)
            except KeyError:
                category[row['Activity Category']].append(row)
    return category


def load_aggregated_demands():
    return __load_aggregation_data('data/00_requirements_aggregated.csv')


def load_aggregated_activities():
    return __load_aggregation_data('data/01_activities_aggregated.csv')


def load_aggregated_artifacts():
    return __load_aggregation_data('data/02_artifacts_aggregated.csv')


def load_activities_artifacts():
    return __load_data('data/01_activities_artifacts.csv')


def load_automation_approaches():
    return __load_data('data/02_automation_approaches.csv')
