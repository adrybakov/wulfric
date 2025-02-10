import wulfric as wulf

cell = wulf.cell.get_cell_example("MCLC4")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("mclc4_brillouin.png")
# Interactive plot:
backend.show()
