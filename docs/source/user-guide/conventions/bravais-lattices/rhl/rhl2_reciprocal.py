import wulfric

cell = wulfric.cell.get_cell_example("RHL2")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("rhl2_reciprocal.png")
# Interactive plot:
backend.show()
