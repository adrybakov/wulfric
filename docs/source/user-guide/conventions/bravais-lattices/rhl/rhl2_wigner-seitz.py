import wulfric as wulf

cell = wulf.cell.get_cell_example("RHL2")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("rhl2_wigner-seitz.png")
# Interactive plot:
backend.show()
