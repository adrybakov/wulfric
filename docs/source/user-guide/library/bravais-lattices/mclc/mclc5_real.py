import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("MCLC5")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive", label="primitive")
backend.plot(l, kind="conventional", label="conventional", color="black")
# Save an image:
backend.save("mclc5_real.png")
# Interactive plot:
backend.show()
