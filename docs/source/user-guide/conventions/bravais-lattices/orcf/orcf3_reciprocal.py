import wulfric

cell = wulfric.cell.get_cell_example("ORCF3")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("orcf3_reciprocal.png")
# Interactive plot:
backend.show()
