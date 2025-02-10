import wulfric as wulf

cell = wulf.cell.get_cell_example("BCT1")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("bct1_wigner-seitz.png")
# Interactive plot:
backend.show()
