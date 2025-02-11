import wulfric as wulf

cell = wulf.cell.get_cell_example("ORCC")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("orcc_reciprocal.png")
# Interactive plot:
backend.show()
