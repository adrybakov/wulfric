import wulfric

cell = wulfric.cell.get_cell_example("ORCF2")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("orcf2_reciprocal.png")
# Interactive plot:
backend.show()
