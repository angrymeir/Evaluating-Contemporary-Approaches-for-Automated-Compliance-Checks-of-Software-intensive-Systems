from flask import Flask, render_template, abort
from parse import load_requirements, load_activities_artifacts, load_automation_approaches
from process import filter_artifacts, filter_activities

app = Flask(__name__)
requirements = load_requirements()
activities_artifacts = load_activities_artifacts()
automation_approaches = load_automation_approaches()


def approach_is_valid(approach, approaches):
    for val_approach in approaches:
        if approach.lower() == val_approach.replace(' ', '_').replace('-', '_').replace('.', '_').replace(':', '_').replace('?', '_').lower():
            return val_approach
    return False


@app.route('/approaches')
def approaches():
    pass


@app.route('/approach/<approach>')
def details(approach):
    valid_approach = approach_is_valid(approach, automation_approaches)
    if valid_approach:
        activities = filter_activities(activities_artifacts[valid_approach])
        artifacts = filter_artifacts(activities_artifacts[valid_approach])
        with open('approach_visualization/{}.drawio.svg'.format(approach.lower())) as f:
            svg = f.read()
        context = {'svg': svg, 'activities': activities, 'artifacts': artifacts}
        return render_template('specific.html', **context)
    else:
        abort(404)
