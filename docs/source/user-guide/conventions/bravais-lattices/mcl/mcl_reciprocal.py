import wulfric as wulf

cell = wulf.cell.get_cell_example("MCL")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("mcl_reciprocal.png")
# Interactive plot:
backend.show()
