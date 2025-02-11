import wulfric as wulf

cell = wulf.cell.get_cell_example("TRI1b")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("tri1b_reciprocal.png")
# Interactive plot:
backend.show()
