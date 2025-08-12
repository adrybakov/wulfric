import wulfric

cell = wulfric.cell.get_cell_example("TRI1a")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("tri1a_reciprocal.png")
# Interactive plot:
backend.show()
