import csv
from collections import defaultdict


def __load_data(path):
    papers = defaultdict(list)
    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            papers[row['Paper Title']].append(row)
    return papers


def load_requirements():
    return __load_data('data/00_requirements.csv')


def load_activities_artifacts():
    return __load_data('data/01_activities_artifacts.csv')


def load_automation_approaches():
    return __load_data('data/02_automation_approaches.csv')
