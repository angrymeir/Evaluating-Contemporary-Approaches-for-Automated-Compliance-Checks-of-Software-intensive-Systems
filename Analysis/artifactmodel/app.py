from flask import Flask, render_template, abort
from parse import load_requirements, load_activities_artifacts, load_automation_approaches
from process import filter_artifacts, filter_activities
from glob import glob

app = Flask(__name__)
requirements = load_requirements()
activities_artifacts = load_activities_artifacts()
all_automation_approaches = load_automation_approaches()
automation_approaches = {}
relevant_approaches = glob('approach_visualization/*.svg')
for name, approach in all_automation_approaches.items():
    new_name = 'approach_visualization/{}.drawio.svg'.format(name.replace(' ', '_').replace('-', '_').replace('.', '_').replace(':', '_').replace('?', '_').lower())
    if new_name in relevant_approaches:
        automation_approaches[name] = approach


def approach_is_valid(approach, approaches):
    for val_approach in approaches:
        if approach.lower() == val_approach.replace(' ', '_').replace('-', '_').replace('.', '_').replace(':', '_').replace('?', '_').lower():
            return val_approach
    return False


@app.route('/approaches')
def approaches():
    context = {'approaches': automation_approaches.values()}
    return render_template('approaches.html', **context)


@app.route('/approach/<approach>')
def details(approach):
    valid_approach = approach_is_valid(approach, automation_approaches)
    if valid_approach:
        activities = filter_activities(activities_artifacts[valid_approach])
        artifacts = filter_artifacts(activities_artifacts[valid_approach])
        with open('approach_visualization/{}.drawio.svg'.format(approach.lower())) as f:
            svg = f.read()
        context = {'svg': svg, 'activities': activities, 'artifacts': artifacts, 'approach': automation_approaches[valid_approach][0]}
        return render_template('specific.html', **context)
    else:
        abort(404)
