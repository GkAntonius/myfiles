from .. import Node, Project

def make_anadir(ids):
    node = Node(ids)
    node.make_analysis_dir(verbose=True)

def save_results():
    project = Project()
    project.copy_analysis_files_to_results()
    pass
