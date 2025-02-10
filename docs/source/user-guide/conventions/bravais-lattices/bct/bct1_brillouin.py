import wulfric as wulf

cell = wulf.cell.get_cell_example("BCT1")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("bct1_brillouin.png")
# Interactive plot:
backend.show()
