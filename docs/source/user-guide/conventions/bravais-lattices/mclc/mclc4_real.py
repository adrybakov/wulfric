import wulfric as wulf

cell = wulf.cell.get_cell_example("MCLC4")
backend = wulf.visualization.PlotlyBackend()
backend.plot(cell, kind="primitive", label="primitive")
backend.plot(cell, kind="conventional", label="conventional", color="black")
# Save an image:
backend.save("mclc4_real.png")
# Interactive plot:
backend.show()
