import wulfric as wulf

cell = wulf.cell.get_cell_example("ORCF2")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("orcf2_wigner-seitz.png")
# Interactive plot:
backend.show()
