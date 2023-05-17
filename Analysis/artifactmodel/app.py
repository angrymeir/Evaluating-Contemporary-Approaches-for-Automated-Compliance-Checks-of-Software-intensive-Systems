from flask import Flask, render_template, abort
from parse import load_activities_artifacts, load_automation_approaches, load_aggregated_demands, load_aggregated_activities, load_aggregated_artifacts
from process import filter_artifacts, filter_activities, map_art_cats_to_act_cats
from glob import glob

visualizations = 'visualizsations'
approach_visualization = visualizations + '/approach_visualization'

app = Flask(__name__)

aggr_demands = load_aggregated_demands()
aggr_activities = load_aggregated_activities()
aggr_artifacts = load_aggregated_artifacts()
artifacts_category_mapping = map_art_cats_to_act_cats(aggr_artifacts)

activities_artifacts = load_activities_artifacts()
all_automation_approaches = load_automation_approaches()
automation_approaches = {}
relevant_approaches = glob('{}/*.svg'.format(approach_visualization))
for name, approach in all_automation_approaches.items():
    new_name = '{}/{}.drawio.svg'.format(approach_visualization, name.replace(' ', '_').replace('-', '_').replace('.', '_').replace(':', '_').replace('?', '_').lower())
    if new_name in relevant_approaches:
        automation_approaches[name] = approach


def approach_is_valid(approach, approaches):
    for val_approach in approaches:
        if approach.lower() == val_approach.replace(' ', '_').replace('-', '_').replace('.', '_').replace(':', '_').replace('?', '_').lower():
            return val_approach
    return False


@app.route('/mapping')
def mapping():
    with open('{}/aggregation_overview.drawio.svg'.format(visualizations), 'r') as f:
        svg = f.read()
    context = {'svg': svg}
    return render_template('mapping.html', **context)


@app.route('/')
def approaches():
    context = {'approaches': automation_approaches.values()}
    return render_template('approaches.html', **context)


@app.route('/demands')
def demands():
    context = {'demands': aggr_demands}
    return render_template('demands.html', **context)


@app.route('/activities')
def activities():
    context = {'activities': aggr_activities}
    return render_template('activities.html', **context)


@app.route('/artifacts')
def artifacts():
    context = {'artifacts': aggr_artifacts, 'category_mapping': artifacts_category_mapping}
    return render_template('artifacts.html', **context)


@app.route('/approach/<approach>')
def details(approach):
    valid_approach = approach_is_valid(approach, automation_approaches)
    if valid_approach:
        activities = filter_activities(activities_artifacts[valid_approach])
        artifacts = filter_artifacts(activities_artifacts[valid_approach])
        with open('{}/{}.drawio.svg'.format(approach_visualization, approach.lower())) as f:
            svg = f.read()
        context = {'svg': svg, 'activities': activities, 'artifacts': artifacts, 'approach': automation_approaches[valid_approach][0]}
        return render_template('specific.html', **context)
    else:
        abort(404)
