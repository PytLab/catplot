#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from catplot.ep_components.ep_lines import ElementaryLine
from catplot.ep_components.ep_chain import EPChain
from catplot.ep_components.ep_canvas import EPCanvas

# Read data from input.txt
globs, locs = {}, {}
exec(open("input.txt", "r").read(), globs, locs)

line_width = locs.get("line_width", 3)

# Create chains.
chains = []
for idx, (energy_tuples,
          peak_widths,
          color,
          initial_x,
          initial_y) in enumerate(zip(locs["multi_energy_tuples"],
                                      locs["peak_widths"],
                                      locs["colors"],
                                      locs["initial_xs"],
                                      locs["initial_ys"])):
    lines = []
    for peak_width, energies in zip(peak_widths, energy_tuples):
        # Create an elementary line.
        line = ElementaryLine(energies,
                              peak_width=peak_width,
                              line_width=line_width,
                              color=color,
                              shadow_depth=locs["shadow_depth"],
                              shadow_color=locs["shadow_color"])
        lines.append(line)

    chain = EPChain(lines)
    chain.translate(initial_x, "x")
    chain.translate(initial_y, "y")
    chains.append(chain)

    # Export data.
    filename = "data_{}.csv".format(idx)
    chain.export(filename)

    print("INFO: write data for chain_{} to {}".format(idx, filename))

# Create energy profile canvas.
figsize = locs.get("figsize", (30, 20))
dpi = locs.get("dpi", 50)
canvas = EPCanvas(figsize=figsize, dpi=dpi)

# Add chains to canvas.
canvas.add_chains(chains)
canvas.draw()

print("INFO: drawing in canvas")

if locs["display_mode"] == "save":
    canvas.figure.savefig("multiple_energy_profile.png")
    print("INFO: energy profile is plotted in multiple_energy_profile.png")
else:
    canvas.figure.show()

