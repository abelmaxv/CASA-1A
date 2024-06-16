from scipy.cluster.hierarchy import dendrogram
from _tree import _label_of_cut
import numpy as np
from cluster import Cluster

def _get_dendrogram_ordering(parent, linkage, root):
    # COPIED FROM THE HDBSCAN LIBRARY
    if parent < root:
        return []

    return _get_dendrogram_ordering(int(linkage[parent-root][0]), linkage, root) + \
            _get_dendrogram_ordering(int(linkage[parent-root][1]), linkage, root) + [parent]


def _calculate_linewidths(ordering, linkage, root):
    # COPIED FROM THE HDBSCAN LIBRARY

    linewidths = []

    for x in ordering:
        if linkage[x - root][0] >= root:
            left_width = linkage[int(linkage[x - root][0]) - root][3]
        else:
            left_width = 1

        if linkage[x - root][1] >= root:
            right_width = linkage[int(linkage[x - root][1]) - root][3]
        else:
            right_width = 1

        linewidths.append((left_width, right_width))

    return linewidths






class LinkageTree(object):

    def __init__(self, linkage_matrix):
        self._linkage_matrix = linkage_matrix

    
    def plot(self, axis=None, truncate_mode=None, p=0, vary_line_width=True,
             cmap='viridis', colorbar=True):
        # COPIED FROM THE HDBSCAN LIBRARY

        dendrogram_data = dendrogram(self._linkage_matrix, p=p, truncate_mode=truncate_mode, no_plot=True)
        X = dendrogram_data['icoord']
        Y = dendrogram_data['dcoord']

    

        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError('You must install the matplotlib library to plot the single linkage tree.')

        if axis is None:
            axis = plt.gca()

        if vary_line_width:
            dendrogram_ordering = _get_dendrogram_ordering(2 * len(self._linkage_matrix), self._linkage_matrix, len(self._linkage_matrix) + 1)
            linewidths = _calculate_linewidths(dendrogram_ordering, self._linkage_matrix, len(self._linkage_matrix) + 1)
        else:
            linewidths = [(1.0, 1.0)] * len(Y)

        if cmap != 'none':
            color_array = np.log2(np.array(linewidths).flatten())
            sm = plt.cm.ScalarMappable(cmap=cmap,
                                       norm=plt.Normalize(0, color_array.max()))
            sm.set_array(color_array)
    
        for x, y, lw in zip(X, Y, linewidths):
            left_x = x[:2]
            right_x = x[2:]
            left_y = y[:2]
            right_y = y[2:]
            horizontal_x = x[1:3]
            horizontal_y = y[1:3]

            if cmap != 'none':
                axis.plot(left_x, left_y, color=sm.to_rgba(np.log2(lw[0])),
                          linewidth=np.log2(1 + lw[0]),
                          solid_joinstyle='miter', solid_capstyle='butt')
                axis.plot(right_x, right_y, color=sm.to_rgba(np.log2(lw[1])),
                          linewidth=np.log2(1 + lw[1]),
                          solid_joinstyle='miter', solid_capstyle='butt')
            else:
                axis.plot(left_x, left_y, color='k',
                          linewidth=np.log2(1 + lw[0]),
                          solid_joinstyle='miter', solid_capstyle='butt')
                axis.plot(right_x, right_y, color='k',
                          linewidth=np.log2(1 + lw[1]),
                          solid_joinstyle='miter', solid_capstyle='butt')

            axis.plot(horizontal_x, horizontal_y, color='k', linewidth=1.0,
                      solid_joinstyle='miter', solid_capstyle='butt')

        if colorbar:
            cb = plt.colorbar(sm, ax=axis)
            cb.ax.set_ylabel('log(Number of points)')

        axis.set_xticks([])
        for side in ('right', 'top', 'bottom'):
            axis.spines[side].set_visible(False)
        axis.set_ylabel('distance')

        return axis

    
    def label_of_cut(self, threshold):
        clusters_array = _label_of_cut(self._linkage_matrix, threshold)
        return Cluster(clusters_array)