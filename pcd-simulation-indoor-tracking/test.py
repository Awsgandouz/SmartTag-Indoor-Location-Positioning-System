import matplotlib.pyplot as plt
import numpy as np

# Position des points fixes (anchors)
A1 = np.array([1, 1])
A2 = np.array([5, 4])

# Fonction de distance entre deux points
def distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2)**2))

# Fonction de localisation
def localize(d1, d2):
    # Les coordonnées de la position estimée du point mobile (tag)
    x = (A1[0]**2 - A2[0]**2 + d2**2 - d1**2) / (2 * (A1[0] - A2[0]))
    y = np.sqrt(d1**2 - (x - A1[0])**2) + A1[1]
    return np.array([x, y])

# Initialisation de la figure
fig, ax = plt.subplots()

# Trace des points fixes (anchors)
ax.plot(A1[0], A1[1], 'ro', markersize=10)
ax.plot(A2[0], A2[1], 'ro', markersize=10)

# Boucle principale
while True:
    # Génération de distances aléatoires simulées
    d1 = np.random.uniform(low=2, high=6)
    d2 = np.random.uniform(low=2, high=6)
    
    # Estimation de la position du point mobile (tag)
    tag_pos = localize(d1, d2)
    
    # Affichage de la position du point mobile (tag)
    ax.plot(tag_pos[0], tag_pos[1], 'bo', markersize=10)
    ax.set_xlim([0, 6])
    ax.set_ylim([0, 6])
    plt.pause(0.5)
    ax.lines[-1].remove()
