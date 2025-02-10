import wulfric as wulf

cell = wulf.cell.get_cell_example("RHL1")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="primitive")
# Save an image:
backend.save("rhl1_real.png")
# Interactive plot:
backend.show()
