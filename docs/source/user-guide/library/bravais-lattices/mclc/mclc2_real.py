import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("MCLC2")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive", label="primitive")
backend.plot(l, kind="conventional", label="conventional", color="black")
# Save an image:
backend.save("mclc2_real.png")
# Interactive plot:
backend.show()
