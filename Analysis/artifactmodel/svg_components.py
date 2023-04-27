def activity(dwg, position, size):
    return dwg.rect(position, size=size, rx=5, ry=5, stroke='black', fill='none')


def description(dwg, position, size, name):
    paragraph = dwg.add(dwg.g(font_size='0.005em'))
    text = dwg.text("", insert=list(position))
    if len(name) > 25:
        text_lines = name.split(' ')
        counter = 0
        for line in text_lines:
            text.add(dwg.tspan(line, insert=(200, 500 + counter * 20), size=size, font_size='150em', fill='red'))
            counter += 1
        paragraph.add(text)
        return paragraph
    return dwg.text(name, insert=list(position))


def artifact(dwg, position):
    pass


def markers(dwg):
    horizontal_marker = _generate_markers(dwg, [(0, 0), (0, 10), (5, 5)])
    dwg.defs.add(horizontal_marker)

    vertical_down_marker = _generate_markers(dwg, [(0, 0), (10, 0), (5, 5)])
    dwg.defs.add(vertical_down_marker)

    vertical_up_marker = _generate_markers(dwg, [(0, 10), (10, 10), (5, 5)])
    dwg.defs.add(vertical_up_marker)

    return horizontal_marker, vertical_down_marker, vertical_up_marker


def _generate_markers(dwg, points):
    marker = dwg.marker(insert=(5,5), size=(10,10))
    marker.add(dwg.polygon(points))
    return marker
