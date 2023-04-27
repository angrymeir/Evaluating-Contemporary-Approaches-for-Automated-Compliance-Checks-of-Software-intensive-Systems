from parse import load_requirements, load_activities_artifacts, load_automation_approaches
from process import generate_activity_graph  # , filter_artifacts
from create_model import Model

requirements = load_requirements()
activities_artifacts = load_activities_artifacts()
automation_approaches = load_automation_approaches()


def main():
    global counter, acts, all_acts
    for act_art in activities_artifacts.values():
        print('Title:', act_art[0]['Paper Title'])
        graph = generate_activity_graph(act_art)
        model = Model(graph, 'outputs/{}.svg'.format(act_art[0]['Paper Title']))
        model.from_graph()
        model.to_svg()
        # iterate_activity_graph(graph, lambda x: print(x))
        print('------')


if __name__ == '__main__':
    main()
