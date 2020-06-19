import os



projectdir = find_project_dir()

#analysis_subdir = os.path.join(projectdir, 'Analysis')
analysis_subdir = project.subdir_analysis

#plot_dir = os.path.join(projectdir, 'Plots')
plot_dir = project.subdir_plots


linking_list = []

for subdir in list_subdirs(analysis):

    source_plot_dir = os.path.join(analysis_subdir, subdir, 'Plots')
    link_plot_dir = os.path.join(plot_dir, subdir)

    linking_list.append((source_plot_dir, link_plot_dir) )

# Print out the list of links
for source, target in linking_list:

    print(target, '-->', source)


# Print out the list of links
for source, target in linking_list:

    make_link(source_plot_dir, link_plot_dir)



