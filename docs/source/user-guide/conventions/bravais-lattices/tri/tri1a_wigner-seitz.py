import wulfric as wulf

cell = wulf.cell.get_cell_example("TRI1a")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("tri1a_wigner-seitz.png")
# Interactive plot:
backend.show()
