import wulfric as wulf

cell = wulf.cell.get_cell_example("MCL")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("mcl_wigner-seitz.png")
# Interactive plot:
backend.show()
