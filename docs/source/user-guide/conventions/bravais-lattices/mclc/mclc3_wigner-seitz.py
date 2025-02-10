import wulfric as wulf

cell = wulf.cell.get_cell_example("MCLC3")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="wigner-seitz")
# Save an image:
backend.save("mclc3_wigner-seitz.png")
# Interactive plot:
backend.show()
