"""
Contents
--------

- data_globe_gif
- connections_globe_gif
- lag_mat_gif_time
- lag_network_gif
- corr_thresh_gif
- cca_ang_gif
"""


## Packages
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
## Local Packages
import spaceweather.visualisation.static as svg
import spaceweather.visualisation.heatmaps as svh


def data_globe_gif(ds, filepath='data_gif', filename='globe_data',
                   list_of_stations=None, list_of_components=['N', 'E'],
                   ortho_trans=None, daynight=True, colour=False, **kwargs):
    '''
    Animates the data vectors on a globe over time with an optional shadow for
    nighttime and optional data colouration.

    Parameters
    ----------
    ds : xarray.Dataset
        3-dimensional Dataset whose coordinates are first_st, second_st, time.
    filepath : str, optional
        File path for storing the image files and gif. Default is
        'data_gif' folder to be made in the current working directory.
    filename : str, optional
        File name for the gif, without file extension. Default is 'globe_data'.
    list_of_stations : list, optional
        List of stations in ds to be used on the plot.
    list_of_components : list, optional
        List of components in ds to be used on the plot. Must be of length 2.
    ortho_trans : tuple, optional
        Orientation of the plotted globe; determines at what angle we view the globe.
        Defaults to average location of all stations.
    daynight : bool, optional
        Whether or not to include a shadow for nighttime. Default is True.
    colour : bool, optional
        Whether or not to colour the data vectors. Also accepts 'color' for
        Americans who can't spell properly.

    Returns
    -------
    .png
        png image files used to make the gif animation, saved in filepath/images_for_giffing.
    .gif
        gif animation of the png image files, saved in filepath/gif.
    '''

    # check filepaths
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    im_filepath = filepath + '/images_for_giffing'
    if not os.path.exists(im_filepath):
        os.makedirs(im_filepath)

    # check filename
    if '.' in filename:
        if len(filename) > 4:
            filename = filename[:-4] # remove file extension
        else:
            raise ValueError('Error: please input filename without file extension')

    # get contstants
    if list_of_stations is None:
        list_of_stations = ds.station.values
    list_of_times = ds.time.values
    num_times = len(list_of_times)

    # check ortho_trans
    if ortho_trans is None:
        ortho_trans = svg.auto_ortho(list_of_stations)

    # initialize the list of names of image files
    names = []

    # plot the data vectors for each time in the Dataset
    for i in range(num_times):
        fig = svg.plot_data_globe(ds = ds,
                                  list_of_stations = list_of_stations,
                                  list_of_components = list_of_components,
                                  t = i,
                                  ortho_trans = ortho_trans,
                                  daynight = daynight,
                                  colour = colour,
                                  **kwargs)
        im_name = im_filepath + '/%s.png' %i
        fig.savefig(im_name) # save image file
        names.append(im_name) # add name of image file to list

    # append plots to each other
    images = []
    for n in names:
        images.append(Image.open(n))

    # make gif file and save it in filepath
    images[0].save(filepath + '/%s.gif' %filename,
                   save_all = True,
                   append_images = images[1:],
                   duration = 100, loop = 0)


def connections_globe_gif(adj_mat_ds,
                          filepath='connections_gif', filename='globe_conn',
                          ortho_trans=None, daynight=True, **kwargs):
    '''
    Animates the network on a globe over time with an optional shadow for nighttime.

    Parameters
    ----------
    adj_mat_ds : xarray.Dataset
        3-dimensional Dataset whose coordinates are first_st, second_st, win_start.
    filepath : str, optional
        File path for storing the image files and gif. Default is
        'connections_gif' folder to be made in the current working directory.
    filename : str, optional
        File name for the gif, without file extension. Default is 'globe_conn'.
    ortho_trans : tuple, optional
        Orientation of the plotted globe; determines at what angle we view the globe.
        Defaults to average location of all stations.
    daynight : bool, optional
        Whether or not to include a shadow for nighttime. Default is True.

    Returns
    -------
    .png
        png image files used to make the gif animation, saved in filepath/images_for_giffing.
    .gif
        gif animation of the png image files, saved in filepath/gif.
    '''

    # check filepaths
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    im_filepath = filepath + '/images_for_giffing'
    if not os.path.exists(im_filepath):
        os.makedirs(im_filepath)

    # check filename
    if '.' in filename:
        if len(filename) > 4:
            filename = filename[:-4] # remove file extension
        else:
            print('Error: please input filename without file extension')
            return 'Error: please input filename without file extension'

    # get contstants
    list_of_stations = adj_mat_ds.first_st.values
    list_of_win_start = adj_mat_ds.win_start.values
    num_win = len(list_of_win_start)

    # check ortho_trans
    if ortho_trans is None:
        ortho_trans = svg.auto_ortho(list_of_stations)

    # initialize the list of names of image files
    names = []

    # plot the connections for each win_start value in the adjacency matrix
    for i in range(num_win):
        fig = svg.plot_connections_globe(adj_matrix = adj_mat_ds[dict(win_start = i)].adj_coeffs.values,
                                         list_of_stations = list_of_stations,
                                         time = list_of_win_start[i],
                                         ortho_trans = ortho_trans,
                                         daynight = daynight,
                                         **kwargs)
        im_name = im_filepath + '/%s.png' %i
        fig.savefig(im_name) # save image file
        names.append(im_name) # add name of image file to list

    # append plots to each other
    images = []
    for n in names:
        images.append(Image.open(n))

    # make gif file and save it in filepath
    images[0].save(filepath + '/%s.gif' %filename,
                   save_all = True,
                   append_images = images[1:],
                   duration = 100, loop = 0)


def lag_mat_gif_time(lag_ds, filepath='lag_mat_gif',
                     filename='lag_mat', **kwargs):
    '''
    Animates a correlogram over time for a station pair.

    Parameters
    ----------
    lag_ds : xarray.Dataset
        Dataset whose coordinates are time_win, lag, first_st, second_st, win_start.
    filepath : str, optional
        File path for storing the image files and gif. Default is
        'lag_mat_gif' folder to be made in the current working directory.
    filename : str, optional
        File name for the gif, without file extension. Default is 'lag_mat'.

    Returns
    -------
    .png
        png image files used to make the gif animation, saved in filepath/images_for_giffing.
    .gif
        gif animation of the png image files, saved in filepath/gif.
    '''

    # check filepaths
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    im_filepath = filepath + '/images_for_giffing'
    if not os.path.exists(im_filepath):
        os.makedirs(im_filepath)

    # check filename
    if '.' in filename:
        if len(filename) > 4:
            filename = filename[:-4] # remove file extension
        else:
            raise ValueError('Error: please input filename without file extension')

    # get constants
    time_wins = lag_ds.time_win.values
    num_win = len(time_wins)

    # initialize the list of names of image files
    names = []

    # plot the connections for each win_start value in the adjacency matrix
    for i in range(num_win):
        lm = lag_ds[dict(time_win = i, lag = 0, win_start = i)]
        fig = svh.plot_lag_mat_time(lag_mat = lm, **kwargs)
        im_name = im_filepath + '/%s.png' %i
        fig.savefig(im_name) # save image file
        names.append(im_name) # add name of image file to list

    # append plots to each other
    images = []
    for n in names:
        images.append(Image.open(n))

    # make gif file and save it in filepath
    images[0].save(filepath + '/%s.gif' %filename,
                   save_all = True,
                   append_images = images[1:],
                   duration = 100, loop = 0)


def lag_network_gif(adj_matrix_ds, filepath='lag_network_gif',
                    filename='lag_network', **kwargs):
    '''
    Animate the directed network provided by the adjacency matrix and lag over time.

    Parameters
    ----------
    adj_matrix_ds : xarray.Dataset
        Adjacency matrix for the network; output from :func:`spaceweather.analysis.threshold.adj_mat`.
    filepath : str, optional
        File path for storing the image files and gif. Default is
        'lag_network_gif' folder to be made in the current working directory.
    filename : str, optional
        File name for the gif, without file extension. Default is 'lag_network'.

    Returns
    -------
    .png
        png image files used to make the gif animation, saved in filepath/images_for_giffing.
    .gif
        gif animation of the png image files, saved in filepath/gif.
    '''

    # check filepaths
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    im_filepath = filepath + '/images_for_giffing'
    if not os.path.exists(im_filepath):
        os.makedirs(im_filepath)

    # check filename
    if '.' in filename:
        if len(filename) > 4:
            filename = filename[:-4] # remove file extension
        else:
            raise ValueError('Error: please input filename without file extension')

    # get constants
    w_sts = adj_matrix_ds.win_start.values
    num_win = len(w_sts)

    # initialize the list of names of image files
    names = []

    # plot the connections for each win_start value in the adjacency matrix
    for i in range(num_win):
        am = adj_matrix_ds[dict(win_start = i)]
        fig = svg.plot_lag_network(adj_matrix = am, **kwargs)
        im_name = im_filepath + '/%s.png' %i
        fig.savefig(im_name) # save image file
        names.append(im_name) # add name of image file to list

    # append plots to each other
    images = []
    for n in names:
        images.append(Image.open(n))

    # make gif file and save it in filepath
    images[0].save(filepath + '/%s.gif' %filename,
                   save_all = True,
                   append_images = images[1:],
                   duration = 100, loop = 0)


def corr_thresh_gif(corr_thresh_ds, filepath='corr_thresh_gif',
                    filename='corr_thresh', **kwargs):
    '''
    Animates a correlation-threshold heatmap over time.

    Parameters
    ----------
    corr_thresh_ds : xarray.Dataset
        Dataset whose coordinates are win_start, first_st, second_st;
        and whose data variables are corr_thresh.
    filepath : str, optional
        File path for storing the image files and gif. Default is
        'corr_thresh_gif' folder to be made in the current working directory.
    filename : str, optional
        File name for the gif, without file extension. Default is 'corr_thresh'.

    Returns
    -------
    .png
        png image files used to make the gif animation, saved in filepath/images_for_giffing.
    .gif
        gif animation of the png image files, saved in filepath/gif.
    '''

    # check filepaths
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    im_filepath = filepath + '/images_for_giffing'
    if not os.path.exists(im_filepath):
        os.makedirs(im_filepath)

    # check filename
    if '.' in filename:
        if len(filename) > 4:
            filename = filename[:-4] # remove file extension
        else:
            raise ValueError('Error: please input filename without file extension')

    # get constants
    w_sts = corr_thresh_ds.win_start.values
    num_win = len(w_sts)

    # initialize the list of names of image files
    names = []

    # plot the connections for each win_start value in the adjacency matrix
    for i in range(num_win):
        clm = corr_thresh_ds[dict(win_start = i)]
        fig = svh.plot_corr_thresh(corr_lag_mat = clm, **kwargs)
        im_name = im_filepath + '/%s.png' %i
        fig.savefig(im_name) # save image file
        names.append(im_name) # add name of image file to list

    # append plots to each other
    images = []
    for n in names:
        images.append(Image.open(n))

    # make gif file and save it in filepath
    images[0].save(filepath + '/%s.gif' %filename,
                   save_all = True,
                   append_images = images[1:],
                   duration = 100, loop = 0)


def cca_ang_gif(cca_ang_ds, a_b, filepath='cca_ang_gif',
                filename='cca_ang', **kwargs):
    '''
    Animates a CCA angle heatmap over time.

    Parameters
    ----------
    cca_ang_ds : xarray.Dataset
        Dataset whose coordinates are time, first_st, second_st, a_b;
        and whose data variables are corr_thresh.
    a_b : {'a', 'b'}
        Plot angles for weight 'a' or weight 'b'.
    filepath : str, optional
        File path for storing the image files and gif. Default is
        'corr_thresh_gif' folder to be made in the current working directory.
    filename : str, optional
        File name for the gif, without file extension. Default is 'corr_thresh'.

    Returns
    -------
    .png
        png image files used to make the gif animation, saved in filepath/images_for_giffing.
    .gif
        gif animation of the png image files, saved in filepath/gif.
    '''

    # check filepaths
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    im_filepath = filepath + '/images_for_giffing'
    if not os.path.exists(im_filepath):
        os.makedirs(im_filepath)

    # check filename
    if '.' in filename:
        if len(filename) > 4:
            filename = filename[:-4] # remove file extension
        else:
            raise ValueError('Error: please input filename without file extension')

    # get constants
    times = cca_ang_ds.time.values
    num_times = len(times)

    # initialize the list of names of image files
    names = []

    # plot the connections for each win_start value in the adjacency matrix
    for i in range(num_times):
        cam = cca_ang_ds[dict(time = i)]
        fig = svh.plot_cca_ang(cca_ang = cam, a_b = a_b, **kwargs)
        im_name = im_filepath + '/%s.png' %i
        fig.savefig(im_name) # save image file
        names.append(im_name) # add name of image file to list

    # append plots to each other
    images = []
    for n in names:
        images.append(Image.open(n))

    # make gif file and save it in filepath
    images[0].save(filepath + '/%s.gif' %filename,
                   save_all = True,
                   append_images = images[1:],
                   duration = 100, loop = 0)
