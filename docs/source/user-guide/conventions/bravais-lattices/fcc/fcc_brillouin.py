import wulfric as wulf

cell = wulf.cell.get_cell_example("FCC")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("fcc_brillouin.png")
# Interactive plot:
backend.show()
