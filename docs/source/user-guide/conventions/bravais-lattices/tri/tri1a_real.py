import wulfric as wulf

cell = wulf.cell.get_cell_example("TRI1a")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="primitive")
# Save an image:
backend.save("tri1a_real.png")
# Interactive plot:
backend.show()
