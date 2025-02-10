import wulfric as wulf

cell = wulf.cell.get_cell_example("MCL")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="primitive")
# Save an image:
backend.save("mcl_real.png")
# Interactive plot:
backend.show()
