from scipy.cluster.hierarchy import dendrogram

class LinkageTree(object):

    def __init__(self, linkage_matrix):
        self._linkage_matrix = linkage_matrix

    
    def plot(self):
        dendrogram_data = dendrogram(self._linkage_matrix)