import wulfric

cell = wulfric.cell.get_cell_example("MCLC4")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("mclc4_reciprocal.png")
# Interactive plot:
backend.show()
