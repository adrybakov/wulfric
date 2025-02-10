import wulfric as wulf

cell = wulf.cell.get_cell_example("HEX")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="primitive")
# Save an image:
backend.save("hex_real.png")
# Interactive plot:
backend.show()
