import wulfric as wulf

cell = wulf.cell.get_cell_example("MCLC1")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="primitive", label="primitive")
backend.plot(cell, kind="conventional", label="conventional", color="black")
# Save an image:
backend.save("mclc1_real.png")
# Interactive plot:
backend.show()
