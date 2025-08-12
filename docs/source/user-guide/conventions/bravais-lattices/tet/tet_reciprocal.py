import wulfric

cell = wulfric.cell.get_cell_example("TET")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("tet_reciprocal.png")
# Interactive plot:
backend.show()
