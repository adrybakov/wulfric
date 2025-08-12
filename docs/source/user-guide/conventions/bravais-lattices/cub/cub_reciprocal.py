import wulfric

cell = wulfric.cell.get_cell_example("CUB")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("cub_reciprocal.png")
# Interactive plot:
backend.show()
