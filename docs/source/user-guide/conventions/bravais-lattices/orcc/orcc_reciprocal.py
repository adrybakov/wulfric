import wulfric

cell = wulfric.cell.get_cell_example("ORCC")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("orcc_reciprocal.png")
# Interactive plot:
backend.show()
