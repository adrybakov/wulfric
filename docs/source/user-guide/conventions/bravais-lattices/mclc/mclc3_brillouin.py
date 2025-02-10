import wulfric as wulf

cell = wulf.cell.get_cell_example("MCLC3")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("mclc3_brillouin.png")
# Interactive plot:
backend.show()
