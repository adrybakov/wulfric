import wulfric

cell = wulfric.cell.get_cell_example("MCL")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("mcl_reciprocal.png")
# Interactive plot:
backend.show()
