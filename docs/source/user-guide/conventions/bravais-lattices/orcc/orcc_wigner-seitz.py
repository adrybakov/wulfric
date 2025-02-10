import wulfric as wulf

cell = wulf.cell.get_cell_example("ORCC")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("orcc_wigner-seitz.png")
# Interactive plot:
backend.show()
