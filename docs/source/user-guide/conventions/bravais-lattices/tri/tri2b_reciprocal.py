import wulfric

cell = wulfric.cell.get_cell_example("TRI2b")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("tri2b_reciprocal.png")
# Interactive plot:
backend.show()
