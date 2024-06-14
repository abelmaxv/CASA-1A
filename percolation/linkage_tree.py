from scipy.cluster.hierarchy import dendrogram
from _tree import _label_of_cut

class LinkageTree(object):

    def __init__(self, linkage_matrix):
        self._linkage_matrix = linkage_matrix

    
    def plot(self):
        # TO DO : 
        #   improve visual 
        #   truncature option

        dendrogram_data = dendrogram(self._linkage_matrix)
    
    def label_of_cut(self, threshold):
        return _label_of_cut(self._linkage_matrix, threshold)