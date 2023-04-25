import svgwrite
from collections import namedtuple

dimension = namedtuple('dimension', 'width height')
activity_dimension = dimension(100, 100)
artifact_dimension = dimension(35, 50)
activity_spacer = dimension(50, 0)


class Model:
    def __init__(self, graph, name, act_to_art_map=None):
        self.name = name
        self.baseline = 400
        self.cur_position = {'x': 0,'y': self.baseline}
        self.graph = graph
        self.act_to_art_map = act_to_art_map

    def from_graph(self):
        while self.graph.is_active():
            nodes = self.graph.get_ready()
            print('Nodes:', nodes)
            if len(nodes) > 1:
                print('Yoho')
            else:
                pass
            for node in nodes:
                if len(nodes) == 1:
                    self.model_activity(node)
                    self.update_position(activity_dimension.width, 0)
                self.graph.done(node)
            self.update_position(activity_spacer.width, activity_spacer.height)

    def update_position(self, x, y):
        self.cur_position['x'] += x
        self.cur_position['y'] += y

    def model_activity(self, activity):
        print(self.cur_position)
        return dwg.rect(self.cur_position.values(), size=activity_dimension, rx=5, ry=5, stroke="black", fill="none")

# General
dwg = svgwrite.Drawing('test.svg', profile='full', debug=True)


##### Markers
horizontal_marker = dwg.marker(insert=(5,5), size=(10,10))
points = [(0,0), (0,10), (5,5)]
horizontal_marker.add(dwg.polygon(points))

vertical_down_marker = dwg.marker(insert=(5,5), size=(10,10))
points = [(0,0), (10, 0), (5,5)]
vertical_down_marker.add(dwg.polygon(points))

vertical_up_marker = dwg.marker(insert=(5,5), size=(10,10))
points = [(0,10), (10, 10), (5,5)]
vertical_up_marker.add(dwg.polygon(points))

dwg.defs.add(horizontal_marker)
dwg.defs.add(vertical_down_marker)
dwg.defs.add(vertical_up_marker)


##### Basic shape creation
def model_activity(coordinates):
    return dwg.rect(coordinates, size=(50,50), rx=5, ry=5, stroke="black", fill="none")

def model_activity_flow(start, end):
    start_x, start_y = start.attribs['x'], start.attribs['y'], 
    start_width, start_width = start.attribs['width'], start.attribs['height']
    stop_x, stop_y = end.attribs['x'], end.attribs['y'], 
    stop_width, stop_width = end.attribs['width'], end.attribs['height']

    flow_start = (start_x + start_width, start_y + start_width/2)
    flow_stop  = (stop_x, stop_y + stop_width/2)

    flow = dwg.line(flow_start, flow_stop, stroke="black")
    flow.set_markers((None, None, horizontal_marker))
    return flow

def generate_artifact(coordinates):
    offset_x, offset_y = coordinates
    points = [(offset_x + 0, offset_y + 0), (offset_x + 30, offset_y + 0), (offset_x + 35, offset_y + 5), (offset_x + 35, offset_y + 50), (offset_x + 0, offset_y + 50)]
    return dwg.polygon(points, stroke='black', fill='none')

def generate_dependency(art, act, mode):
    points = art.points
    art_start = points[0]
    art_stop  = points[-2]
    dependency_x = art_start[0] + (art_stop[0]-art_start[0])/2
    act_x = act.attribs['x'] + act.attribs['width']/2
    if art_start[1] > act.attribs['y']:
        # Artifact below activity
        dependency_y = art_start[1]
        act_y = act.attribs['y'] + act.attribs['height']
        dependency = dwg.line((dependency_x, dependency_y), (act_x, act_y), stroke="black")
        if mode == 'input':
            dependency.set_markers((None, None, vertical_up_marker))
        elif mode == 'output':
            dependency.set_markers((vertical_down_marker, None, None))
    else:
        # Artifact above activity
        dependency_y = art_stop[1]
        act_y = act.attribs['y']
        dependency = dwg.line((dependency_x, dependency_y), (act_x, act_y), stroke="black")
        if mode == 'input':
            dependency.set_markers((None, None, vertical_down_marker))
        elif mode == 'output':
            dependency.set_markers((vertical_up_marker, None, None))
        else:
            raise Exception('Not implemented')
    return dependency

def text_for_act(activity):
    pass

def text_for_art(artifact):
    pass


##### Advanced shape creation
# 1. Check graph for parallel activities
# 2. Check graph for multiple inputs/outputs to activity
# 3. Check graph for multiple inputs/outputs that are attached to more than one activity

##### Test instantiation
# Activities
act1 = model_activity((100,100))
act2 = model_activity((200,100))
act3 = model_activity((300,100))
act4 = model_activity((400,100))

# Flows
flow12 = model_activity_flow(act1, act2)
flow23 = model_activity_flow(act2, act3)
flow34 = model_activity_flow(act3, act4)

# Artifacts
art1 = generate_artifact((110,200))

# Dependencies
dep1 = generate_dependency(art1, act1, mode='input')

# Add to drawing
dwg.add(act1)
dwg.add(act2)
dwg.add(act3)
dwg.add(act4)
dwg.add(flow12)
dwg.add(flow23)
dwg.add(flow34)
dwg.add(art1)
dwg.add(dep1)

#dwg.add(dwg.rect((100,100), size=(50,50), rx=5, ry=5, stroke="black", fill='none'))
#dwg.add(dwg.text("Bla", insert=(100, 150)))
#dwg.add(dwg.rect((200,100), size=(50,50)))
#line = dwg.line((150,125), (200,125), stroke=svgwrite.rgb(10, 10, 16, '%'))
#line.set_markers((None, None, marker))
#dwg.add(line)
#dwg.add(dwg.rect((100,100), size=(1,1)))
dwg.save()

