import wulfric as wulf

cell = wulf.cell.get_cell_example("TRI2b")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("tri2b_brillouin.png")
# Interactive plot:
backend.show()
