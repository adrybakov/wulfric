import wulfric as wulf

cell = wulf.cell.get_cell_example("ORC")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="primitive")
# Save an image:
backend.save("orc_real.png")
# Interactive plot:
backend.show()
