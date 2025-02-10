import wulfric as wulf

cell = wulf.cell.get_cell_example("CUB")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("cub_wigner-seitz.png")
# Interactive plot:
backend.show()
