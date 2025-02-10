import wulfric as wulf

cell = wulf.cell.get_cell_example("FCC")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("fcc_wigner-seitz.png")
# Interactive plot:
backend.show()
