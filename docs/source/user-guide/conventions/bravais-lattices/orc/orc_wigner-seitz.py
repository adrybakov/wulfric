import wulfric as wulf

cell = wulf.cell.get_cell_example("ORC")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("orc_wigner-seitz.png")
# Interactive plot:
backend.show()
