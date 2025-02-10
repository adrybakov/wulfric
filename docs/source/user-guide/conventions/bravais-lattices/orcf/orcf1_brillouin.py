import wulfric as wulf

cell = wulf.cell.get_cell_example("ORCF1")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("orcf1_brillouin.png")
# Interactive plot:
backend.show()
