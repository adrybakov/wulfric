import wulfric as wulf

cell = wulf.cell.get_cell_example("RHL1")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("rhl1_brillouin.png")
# Interactive plot:
backend.show()
