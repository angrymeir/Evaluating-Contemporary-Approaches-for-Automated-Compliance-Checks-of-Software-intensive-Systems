import svgwrite

dwg = svgwrite.Drawing('bla.svg')
# create a new marker object
marker = dwg.marker(insert=(5,5), size=(10,10))

# red point as marker
marker.add(dwg.circle((5, 5), r=5, fill='red'))

# add marker to defs section of the drawing
dwg.defs.add(marker)

# create a new line object
line = dwg.add(dwg.polyline(
    [(10, 10), (50, 20), (70, 50), (100, 30)],
    stroke='black', fill='none'))

line.set_markers((None, False, marker))

dwg.save()
