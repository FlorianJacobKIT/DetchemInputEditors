

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
    line += "{:10.3E}".format(reaction.A_k)
    line += "{:7G}".format(reaction._beta_k)
    line += "{:10G}".format(reaction.E_k)
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