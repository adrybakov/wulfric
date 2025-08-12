import wulfric

cell = wulfric.cell.get_cell_example("ORCI")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("orci_reciprocal.png")
# Interactive plot:
backend.show()
