import wulfric as wulf

cell = wulf.cell.get_cell_example("CUB")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="primitive")
# Save an image:
backend.save("cub_real.png")
# Interactive plot:
backend.show()
