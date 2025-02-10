import wulfric as wulf

cell = wulf.cell.get_cell_example("ORCI")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("orci_wigner-seitz.png")
# Interactive plot:
backend.show()
