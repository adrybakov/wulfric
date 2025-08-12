import wulfric

cell = wulfric.cell.get_cell_example("MCLC4")
backend = wulfric.visualization.PlotlyBackend()
backend.plot(cell, kind="primitive", label="primitive", color="black")
backend.plot(cell, kind="conventional", label="conventional", color="blue")
backend.plot(cell, kind="wigner-seitz", label="wigner-seitz", color="green")
# Save an image:
backend.save("mclc4_real.png")
# Interactive plot:
backend.show()
