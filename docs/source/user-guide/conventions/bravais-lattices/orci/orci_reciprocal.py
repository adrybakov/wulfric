import wulfric as wulf

cell = wulf.cell.get_cell_example("ORCI")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("orci_reciprocal.png")
# Interactive plot:
backend.show()
