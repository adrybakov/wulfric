import wulfric

cell = wulfric.cell.get_cell_example("BCC")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="brillouin-kpath")
# Save an image:
backend.save("bcc_reciprocal.png")
# Interactive plot:
backend.show()
