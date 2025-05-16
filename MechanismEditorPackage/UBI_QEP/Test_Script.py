# Define constants (tunable based on calibration)
import os
import time

ALPHA = 0.80
BETA = 0.50

# Example data (can be extended)
D_gas_bonds = {
    'C-H': 103.0,  # kcal/mol
    'C-O': 85.0,
    'O-H': 110.0
}

Q_adsorption = {
    'H': 65.0,    # kcal/mol
    'C': 160.0,
    'O': 100.0,
    'CH3': 50.0,
    'CH2': 90.0,
    'CH': 120.0
}

def parse_species(species):
    """Remove adsorbed symbol and return atom/group"""
    return species.replace('*', '').strip()

def guess_bond_break(reactant, products):
    """Try to guess which bond is broken based on molecular fragments"""
    for atom in ['H', 'O', 'C']:
        if atom in reactant and f"{atom}*" in products:
            return f"C-{atom}", atom
    raise ValueError("Could not guess broken bond.")

def calculate_activation_energy(reaction):
    """Compute UBI-QEP activation energy for a dissociation reaction"""
    # Split reaction
    lhs, rhs = reaction.split("->")
    reactant = lhs.strip()
    products = [p.strip() for p in rhs.strip().split('+')]

    # Guess broken bond and desorbing atom
    bond, atom = guess_bond_break(reactant, rhs)

    # Determine fragment A and B
    frag_A = parse_species(products[0])  # usually H*
    frag_B = parse_species(products[1])  # CH3*, etc.

    # Look up values
    D = D_gas_bonds.get(bond)
    Q_A = Q_adsorption.get(frag_A)
    Q_B = Q_adsorption.get(frag_B)

    if None in (D, Q_A, Q_B):
        raise ValueError(f"Missing data for bond {bond} or fragments {frag_A}, {frag_B}.")

    # UBI-QEP estimation
    Ea = ALPHA * D - BETA * (Q_A + Q_B)
    return Ea, bond, frag_A, frag_B

# ==== EXAMPLE ====
if __name__ == "__main__":
    reaction = "CH4 -> CH3* + H*"
    Ea, bond, A, B = calculate_activation_energy(reaction)
    print(f"\nReaction: {reaction}")
    print(f"Broken bond: {bond}")
    print(f"Surface-bound fragments: {A}*, {B}*")
    print(f"Estimated activation energy (Ea): {Ea:.2f} kcal/mol")
