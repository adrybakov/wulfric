import wulfric as wulf

cell = wulf.cell.get_cell_example("MCLC5")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("mclc5_reciprocal.png")
# Interactive plot:
backend.show()
