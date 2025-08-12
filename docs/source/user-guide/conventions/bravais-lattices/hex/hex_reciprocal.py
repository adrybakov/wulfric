import wulfric

cell = wulfric.cell.get_cell_example("HEX")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("hex_reciprocal.png")
# Interactive plot:
backend.show()
