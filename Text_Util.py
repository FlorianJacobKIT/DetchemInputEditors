

def add_reaction_to_line(reaction, lines):
    line = ""
    if reaction.is_stick:
        if reaction.is_disabled:
            lines.append("*STICK\n")
        else:
            lines.append("STICK\n")
    if reaction.is_disabled:
        line += "*"
    for educt in reaction.educts:
        for i in range(reaction.educts[educt]):
            line += str(educt).ljust(8)
            line += "+"
    line = line[:-1]
    line += ">"
    for product in reaction.products:
        for i in range(reaction.products[product]):
            line += str(product).ljust(8)
            line += "+"
    line = line[:-1]
    line = line.ljust(45)

    A_k = reaction.get_A_k(raw=True)
    if not reaction.is_stick:
        # Mol/cm2 -> Mol/m2 and Mol/cm3 -> Mol/m3
        A_k = A_k * 100**reaction.exponent
    beta_k = reaction.get_beta_k(raw=True)
    # kJ/mol -> J/mol
    E_k = reaction.E_k / 1e3

    line += "{:10.3E}".format(A_k).rjust(10)
    line += "{:.4f}".format(beta_k).rjust(7)
    line += "{:10G}".format(E_k).rjust(10)
    line += "\n"
    lines.append(line)
    orders = reaction.orders
    for key, value in orders.items():
        line = "$"
        line += key
        line = line.ljust(55)
        line += "{:7G}".format(value)
        if key in reaction.epsilon:
            line += "{:10G}".format(reaction.epsilon[key])
            reaction.epsilon.pop(key)
        else:
            line += "{:10G}".format(0)
            line += "\n"
        lines.append(line)
    for key, value in reaction.epsilon.items():
        line = "$"
        line += key
        line = line.ljust(55)
        line += "{:7G}".format(0)
        line += "{:10G}".format(value)
        line += "\n"
        lines.append(line)