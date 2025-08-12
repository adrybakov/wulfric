import wulfric

cell = wulfric.cell.get_cell_example("MCLC1")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("mclc1_reciprocal.png")
# Interactive plot:
backend.show()
