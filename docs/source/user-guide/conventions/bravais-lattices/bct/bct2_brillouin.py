import wulfric as wulf

cell = wulf.cell.get_cell_example("BCT2")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("bct2_brillouin.png")
# Interactive plot:
backend.show()
