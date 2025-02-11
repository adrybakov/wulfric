import wulfric as wulf

cell = wulf.cell.get_cell_example("TRI2a")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="primitive", label="primitive", color="black")
backend.plot(cell, kind="wigner-seitz", label="wigner-seitz", color="green")
# Save an image:
backend.save("tri2a_real.png")
# Interactive plot:
backend.show()
