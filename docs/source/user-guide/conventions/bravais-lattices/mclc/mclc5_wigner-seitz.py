import wulfric as wulf

cell = wulf.cell.get_cell_example("MCLC5")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("mclc5_wigner-seitz.png")
# Interactive plot:
backend.show()
