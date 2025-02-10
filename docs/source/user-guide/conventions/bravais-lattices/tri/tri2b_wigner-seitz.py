import wulfric as wulf

cell = wulf.cell.get_cell_example("TRI2b")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("tri2b_wigner-seitz.png")
# Interactive plot:
backend.show()
