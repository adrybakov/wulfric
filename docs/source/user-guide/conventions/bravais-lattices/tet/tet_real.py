import wulfric as wulf

cell = wulf.cell.get_cell_example("TET")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="primitive")
# Save an image:
backend.save("tet_real.png")
# Interactive plot:
backend.show()
