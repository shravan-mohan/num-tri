import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def base_representation(num, base):
    """
    This function generates the base representation of a number in a given base.
    :param num: An integer.
    :param base: The desired base.
    :return: The representation of the number in the given base.
    """
    r = []
    t = num
    while(t!=0):
        r = r + [int(np.mod(t,base))]
        t = t - np.mod(t,base)
        t = t/base
    s = str(r[::-1][0])
    for k in r[::-1][1:]:
        s = s + ',' + str(k)

    return s


def xor_base(x1, x2, base):
    """
    This function returns the XOR in a given base (modula the base).
    :param x1: First integer.
    :param x2: Second integer.
    :param base: The desired base.
    :return: The resulting equivalence class.
    """
    return np.mod(x1+x2, base)

def getMat(z, base):
    """
    This function generates the number triangle in a given base triangle.
    :param z: An integer. Must be greater than (base+1), esle the output is equal to -1.
    :param base: The desired base representation.
    :return: The number triangle.
    """
    r = base_representation(z, base)
    dec2base = r.split(',')
    L = len(dec2base)
    if(L<=1):
        return -1, -1
    tmp = -1 * np.ones([L, 2 * L - 1])
    for l in range(2 * L - 1):
        if (np.mod(l, 2) == 0):
            tmp[0, l] = dec2base[int(l / 2)]
    for l in range(1, L):
        for j in range(1, 2 * L - 2):
            if (tmp[l - 1, j - 1] == -1 or tmp[l - 1, j + 1] == -1):
                continue
            else:
                tmp[l, j] = xor_base(tmp[l - 1, j - 1], tmp[l - 1, j + 1], base)

    dec2base2 = ''
    for l in range(L):
        if(l==0):
            dec2base2 = dec2base2 + str(int(tmp[l, 2 * L - 2 - l]))
        else:
            dec2base2 = dec2base2 + str(',') + str(int(tmp[l, 2 * L - 2 - l]))
    dec2base2 = dec2base2.split(',')

    dec2base3 = ''
    for l in range(L):
        if (l == 0):
            dec2base3 = dec2base3 + str(int(tmp[L - 1 - l, int((2 * L - 1) / 2) - l]))
        else:
            dec2base3 = dec2base3 + str(',') +str(int(tmp[L - 1 - l, int((2 * L - 1) / 2) - l]))
    dec2base3 = dec2base3.split(',')

    return tmp, [dec2base, dec2base2, dec2base3]

def plot(A, limlow, limhigh, xshift, yshift, base, colors, ax):
    """
    This function plots the number triangle for a given integer.
    :param A: The matrix resulting from getMat function.
    :param limlow: The lower xlim and ylim for plot.
    :param limhigh: The higher xlim and ylim for plot.
    :param xshift: The x-translation desired.
    :param yshift: The y-translation desired.
    :param base: The base used for getMat
    :param colors: Different colors for different congruent classes. Must be at least the size
    equal to base.
    :param ax: The plot handle.
    :return: Plot of the colored circles representing the number triangle.
    """
    r = (limhigh-limlow)/(A.shape[0])/2

    for k in range(A.shape[0]):
        if (np.mod(k, 2) == 0):
            count = 0
            for l in range(A.shape[1]):
                for u in range(base):
                    if(A[k,l] == u):
                        circle = plt.Circle((xshift + limlow + r + 2*r*count+(k*r), yshift + limhigh - r - 2*r * k), r, fill=True, color=colors[u].replace('0x','#'), linewidth=2)
                        ax.add_artist(circle)
                        count = count + 1
        if (np.mod(k, 2) == 1):
            count = 0
            for l in range(A.shape[1]):
                for u in range(base):
                    if (A[k, l] == u):
                        circle = plt.Circle((xshift + limlow + 2*r + 2*r * count+((k-1)*r), yshift + limhigh - r - 2*r * k), r, fill=True, color=colors[u].replace('0x','#'), linewidth=2)
                        ax.add_artist(circle)
                        count = count + 1

if(__name__=='__main__'):
    """
    1. Define the base
    2. Define the colors for the plot
    3. Define the number of slots in the plot. (sq_size)
    4. Define maxNum to look for special numbers (where top, rhs and lhs match)
    """

    base = 2 # define the base
    colors = [list(mcolors.CSS4_COLORS.keys())[t] for t in np.random.permutation(len(list(mcolors.CSS4_COLORS.keys())))]
    ans = []
    sq_size = 10
    N = sq_size**2
    maxNum = 1000000

    fig, ax = plt.subplots()
    ax.set_aspect(1)
    limlow = 0
    limhigh = 1
    plt.xlim(sq_size*limlow, sq_size*limhigh)
    plt.ylim(sq_size*limlow, sq_size*limhigh)

    count = 0
    z = base + 1
    while(count<N and z<maxNum):
        A, t = getMat(z, base)
        if(t[0]==t[1] and t[1]==t[2]):
            print(z)
            j = np.mod(count,sq_size)
            i = int((count - j)/sq_size)
            plot(A,limlow,limhigh,j,i,base,colors, ax)
            count = count + 1
        z = z + 1

