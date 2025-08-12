import wulfric

cell = wulfric.cell.get_cell_example("BCT2")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("bct2_reciprocal.png")
# Interactive plot:
backend.show()
