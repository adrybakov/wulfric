import wulfric as wulf

cell = wulf.cell.get_cell_example("MCLC4")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("mclc4_wigner-seitz.png")
# Interactive plot:
backend.show()
