import wulfric as wulf

cell = wulf.cell.get_cell_example("TRI1a")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("tri1a_reciprocal.png")
# Interactive plot:
backend.show()
