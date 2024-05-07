"""
Lazor Project

Authors: Noah Daniel Smith, Valentina Matos Romero
Last Modified May 3, 2024

Note: This script is an adaptation of a previous cell counting script by GitHub
user ZachPenn's repository 'CellCounting' (see: https://github.com/ZachPenn/CellCounting/).
The scripts from this repo were ported from Jupyter Notebook to Python, updated from deprecation
and adjusted for speed and clarity. Finally, the script was tweaked to interface with a PyQt GUI,
which comprised the main focus of our project.

On that note, the main goal of our project was to create an cell counting applet with a GUI to
streamline the automatic collection of cell counting data for wet lab scientists who are not
experienced with programming and adjusting the parameters of scripts in text editors.
"""

import os
import sys
import fnmatch
import cv2
import numpy as np
import mahotas as mh
import pandas as pd
import holoviews as hv
import scipy as sp
from skimage import filters
from skimage.segmentation import watershed as skwatershed
from skimage.feature import peak_local_max
from skimage import measure
from contextlib import contextmanager
import warnings

hv.extension('bokeh')
warnings.filterwarnings("ignore")

#########
'''originally written by Zachary Pennington'''


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


#########
'''originally written by Zachary Pennington'''


def rm_smallparts(image, celldiam, pmin):
    labeled, nr_objects = mh.label(image)
    sizes = mh.labeled.labeled_size(labeled)
    too_small = np.where(sizes < (celldiam * celldiam * pmin))
    labeled = mh.labeled.remove_regions(labeled, too_small)
    Image_Current_T = labeled != 0
    return Image_Current_T


#########

'''originally written by Zachary Pennington'''


def medianFilter(image, ksize):
    ksize = (ksize - 1) if (ksize % 2 == 0) else ksize
    image = sp.ndimage.median_filter(image, size=ksize)
    return image


#########
'''originally written by Zachary Pennington; edited by Noah Smith'''


def subtractbg(image, ksize):
    image = image.astype('float')
    bg = cv2.GaussianBlur(image,
                          (0, 0),
                          ksize)
    new_image = image - bg
    new_image[new_image < 0] = 0
    return new_image


#########
'''originally written by Zachary Pennington; edited by Noah Smith'''


def Count(file, Channel, params, dirinfo, UseROI=False, UseWatershed=False, SaveIntensities=False):
    # Set function parameters in accordance with channel to be counted
    if Channel == "Ch1":
        CellDiam = params['ch1_diam']
        Thresh = params['ch1_thresh']
        Directory_Current = dirinfo['ch1']
        FileNames_Current = dirinfo['ch1_fnames']
        output = dirinfo['output_ch1']
    elif Channel == "Optim":
        CellDiam = params['diam']
        Thresh = params['thresh']
        Directory_Current = dirinfo['composite']
        FileNames_Current = dirinfo['composite_fnames']

    # Load file
    Image_Current_File = os.path.join(os.path.normpath(Directory_Current), FileNames_Current[file])
    Image_Current_Gray = cv2.imread(Image_Current_File, cv2.IMREAD_ANYDEPTH)
    # print("Processing: " + FileNames_Current[file])

    # Process file
    Image_Current_Median = medianFilter(Image_Current_Gray, ksize=CellDiam // 2)
    Image_Current_BG = subtractbg(Image_Current_Gray, ksize=CellDiam * 3)
    Image_Current_Gaussian = cv2.GaussianBlur(Image_Current_BG.astype('float'), (0, 0), CellDiam / 6)
    Image_Current_T = rm_smallparts(Image_Current_Gaussian > Thresh, CellDiam, params['particle_min'])
    roi_size = Image_Current_Gray.size

    if UseWatershed == True:
        Image_Current_Cells, nr_nuclei = watershed(Image_Current_T, CellDiam, params['particle_min'])
    else:
        Image_Current_Cells, nr_nuclei = sp.ndimage.label(Image_Current_T)

    if SaveIntensities:
        cell_info = pd.DataFrame(columns=['{}_file'.format(Channel), 'cell_id', 'cell_size', 'cell_intensity'])
        for cell_id in np.unique(Image_Current_Cells[Image_Current_Cells > 0]):
            cell_info_new = pd.DataFrame(
                {
                    '{}_file'.format(Channel): [FileNames_Current[file]],
                    'cell_id': [cell_id],
                    'cell_size': [len(Image_Current_Cells[Image_Current_Cells == cell_id])],
                    'cell_intensity': [Image_Current_Gaussian[Image_Current_Cells == cell_id].mean()]
                },
            )
            cell_info = pd.concat([cell_info, cell_info_new], ignore_index=True)
        cell_info.to_csv(
            os.path.splitext(
                os.path.join(
                    os.path.normpath(output),
                    FileNames_Current[file]
                )
            )[0] + '_CellInfo.csv',
            index=False
        )

    count_output = {
        'cells': Image_Current_Cells,
        'nr_nuclei': nr_nuclei,
        'roi_size': roi_size,
        'image': Image_Current_Gray,
        'gauss': Image_Current_Gaussian,
        'thresh': Image_Current_T
    }
    return count_output


#########
'''originally written by Zachary Pennington; edited by Noah Smith'''


def getdirinfo(dirinfo):
    dirinfo['composite'] = os.path.join(os.path.normpath(dirinfo['main']), "Composite")
    dirinfo['manual'] = os.path.join(os.path.normpath(dirinfo['main']), "ManualCounts")
    dirinfo['output'] = os.path.join(os.path.normpath(dirinfo['main']), "SavedOutput")
    if not os.path.isdir(dirinfo['output']): os.mkdir(dirinfo['output'])
    dirinfo['composite_fnames'] = sorted(os.listdir(dirinfo['composite']))
    dirinfo['composite_fnames'] = fnmatch.filter(dirinfo['composite_fnames'], '*.tif')
    dirinfo['manual_fnames'] = sorted(os.listdir(dirinfo['manual']))
    dirinfo['manual_fnames'] = fnmatch.filter(dirinfo['manual_fnames'], '*.tif')

    # Define subdirectories
    dirinfo['ch1'] = os.path.join(os.path.normpath(dirinfo['main']), "Ch1")
    dirinfo['output'] = os.path.join(os.path.normpath(dirinfo['main']), "SavedOutput")

    # Get filenames and create output subdirectories based upon usage
    if not os.path.exists(dirinfo['output']): os.mkdir(dirinfo['output'])
    if os.path.isdir(dirinfo['ch1']):
        dirinfo['ch1_fnames'] = sorted(os.listdir(dirinfo['ch1']))
        dirinfo['ch1_fnames'] = fnmatch.filter(dirinfo['ch1_fnames'], '*.tif')
        dirinfo['output_ch1'] = os.path.join(os.path.normpath(dirinfo['output']), "Ch1")
        if not os.path.isdir(dirinfo['output_ch1']): os.mkdir(dirinfo['output_ch1'])

    return dirinfo


########
'''originally written by Zachary Pennington; edited by Noah Smith'''


def optim_getimages(dirinfo, params):
    images = {
        'manual': cv2.imread(
            os.path.join(os.path.normpath(dirinfo['manual']), dirinfo['manual_fnames'][0]),
            cv2.IMREAD_ANYDEPTH
        ),
        'composite': cv2.imread(
            os.path.join(os.path.normpath(dirinfo['composite']), dirinfo['composite_fnames'][0]),
            cv2.IMREAD_ANYDEPTH
        )
    }
    images['median'] = medianFilter(images['composite'], ksize=params['diam'] // 2)
    images['bg'] = subtractbg(images['median'], ksize=params['diam'] * 3)
    images['gauss'] = cv2.GaussianBlur(images['bg'], (0, 0), params['diam'] / 6)
    params['counts'] = (images['manual'] > 0).sum()
    params['otsu'] = filters.threshold_otsu(image=images['gauss'].astype('int64'))
    params['thresh'] = params['otsu']

    images['otsu'] = images['gauss'] > params['thresh']
    count_output = Count(
        0,
        "Optim",
        params,
        dirinfo,
        UseROI=False,
        UseWatershed=params['UseWatershed']
    )

    return images, params, count_output


#########
'''Originally written by Zachary Pennington'''


def optim_iterate(images, dirinfo, params, interv=1):
    Channel = 'Optim'
    file = 0  # Should always be zero because only one composite image

    # Initialize Arrays to Store Data In
    List_AutoCounts = []
    List_CellAreas = []
    List_Acc_Auto_over_ManualCounts = []

    # Define maximum threshold value and create series of thresholds to cycle through
    TMin = 0  # params['otsu']
    TMax = int(images['gauss'].max() // 1)  # Get maximum value in array.  Threshold can't go beyond this
    List_ThreshValues = list(np.arange(TMin, TMax, interv))

    for thresh in List_ThreshValues:

        params['thresh'] = thresh
        with suppress_stdout():
            count_out = Count(file, Channel, params, dirinfo, UseROI=False, UseWatershed=params['UseWatershed'])
        List_AutoCounts.append(count_out['nr_nuclei'])

        # Determine Avg Cell Size in Pixel Units
        if count_out['nr_nuclei'] > 0:
            Cell_Area = count_out['cells'] > 0
            Cell_Area = Cell_Area.sum() / count_out['nr_nuclei']
        elif count_out['nr_nuclei'] == 0:
            Cell_Area = float('nan')
        List_CellAreas.append(Cell_Area)

        # Calculate Accuracies
        aomc = count_out['nr_nuclei'] / params['counts'] if count_out['nr_nuclei'] > 0 else np.nan
        List_Acc_Auto_over_ManualCounts.append(aomc)

    # Create Dataframe
    DataFrame = pd.DataFrame(
        {
            'AutoCount_Thresh': List_ThreshValues,
            'OTSU_Thresh': np.ones(len(List_ThreshValues)) * params['otsu'],
            'Manual_CellDiam': np.ones(len(List_ThreshValues)) * params['diam'],
            'Manual_Counts': np.ones(len(List_ThreshValues)) * params['counts'],
            'AutoCount_UseWatershed': np.ones(len(List_ThreshValues)) * params['UseWatershed'],
            'AutoCount_Counts': List_AutoCounts,
            'AutoCount_AvgCellArea': List_CellAreas,
            'Acc_Manual_over_AutoCounts': List_Acc_Auto_over_ManualCounts,

        }
    )
    return DataFrame, images['manual']


#########
'''originally written by Zachary Pennington'''

def Count_folder(dirinfo, params, Channel, UseROI=False, UseWatershed=False, SaveIntensities=False):
    # Set some info in accordance with channel to be counted
    if Channel == "Ch1":
        fnames = dirinfo['ch1_fnames']
        output = dirinfo['output_ch1']
        diam = params['ch1_diam']
        thresh = params['ch1_thresh']
    elif Channel == "Ch2":
        fnames = dirinfo['ch2_fnames']
        output = dirinfo['output_ch2']
        diam = params['ch2_diam']
        thresh = params['ch2_thresh']

    # Initialize arrays to store data in
    COUNTS = []
    ROI_SIZE = []

    # Loop through images and count cells
    for file in range(len(fnames)):
        count_out = Count(
            file,
            Channel,
            params,
            dirinfo,
            UseROI=UseROI,
            UseWatershed=UseWatershed,
            SaveIntensities=SaveIntensities
        )
        COUNTS.append(count_out['nr_nuclei'])
        ROI_SIZE.append(count_out['roi_size'])
        cv2.imwrite(
            filename=os.path.splitext(
                os.path.join(
                    os.path.normpath(output),
                    fnames[file]
                )
            )[0] + '_Counts.tif',
            img=count_out['cells'].astype(np.uint16)
        )

    # Create DataFrame
    if Channel == "Ch1":
        DataFrame = pd.DataFrame(
            {'Ch1_FileNames': fnames,
             'Ch1_Thresh': np.ones(len(fnames)) * thresh,
             'Ch1_UseROI': np.ones(len(fnames)) * UseROI,
             'Ch1_AvgCellDiam': np.ones(len(fnames)) * diam,
             'Ch1_ParticleMin': np.ones(len(fnames)) * params['particle_min'],
             'Ch1_Counts': COUNTS,
             'Ch1_ROIsize': ROI_SIZE
             })
        return DataFrame
    if Channel == "Ch2":
        DataFrame = pd.DataFrame(
            {'Ch2_FileNames': fnames,
             'Ch2_Thresh': np.ones(len(fnames)) * thresh,
             'Ch2_UseROI': np.ones(len(fnames)) * UseROI,
             'Ch2_AvgCellDiam': np.ones(len(fnames)) * diam,
             'Ch2_ParticleMin': np.ones(len(fnames)) * params['particle_min'],
             'Ch2_Counts': COUNTS,
             'Ch2_ROIsize': ROI_SIZE
             })
        return DataFrame


#########
'''Originally written by Zachary Pennington'''


def watershed(Image_Current_T, CellDiam, particle_min):
    if Image_Current_T.max() == True:

        Image_Current_Tdist = sp.ndimage.distance_transform_edt(Image_Current_T)
        Image_Current_Tdist_erd = Image_Current_Tdist > CellDiam * particle_min
        Image_Current_Tdist_lbls = measure.label(Image_Current_Tdist_erd)

        coords = peak_local_max(
            Image_Current_Tdist,
            min_distance=int(CellDiam),
            labels=Image_Current_Tdist_lbls,
            num_peaks_per_label=1
        )
        Image_Current_Seeds = np.zeros(Image_Current_T.shape, dtype=bool)
        Image_Current_Seeds[tuple(coords.T)] = True
        Image_Current_Seeds, nseeds = sp.ndimage.label(Image_Current_Seeds)

        labels = skwatershed(-Image_Current_Tdist, Image_Current_Seeds, mask=Image_Current_T)

    elif Image_Current_T.max() == False:
        labels = Image_Current_T.astype(int)
        nseeds = 0

    return labels, nseeds


#########

def cellcounting_param_optimizer(dirinfo, params):
    # Determines the manual and auto counts using preset Otsu threshold.
    images, params, count_output = optim_getimages(dirinfo, params)
    # Gradually decreases the average diameter until the manual counts exceed the manual counts.
    # Serves as a rough optimization which is smoothened by auto-thresholding.
    while count_output['nr_nuclei'] < params['counts']:
        params['diam'] = params['diam'] - 1
        images, params, count_output = optim_getimages(dirinfo, params)
        # print('Cells: {x}'.format(x=count_output['nr_nuclei']))
        # print('Manual: {x}'.format(x=params['counts']))
    optimal_diameter = params['diam']

    # Determining the optimum threshold value
    data, manual = optim_iterate(images, dirinfo, params, interv=10)
    data.to_csv(os.path.join(os.path.normpath(dirinfo['output']), "OptimizationSummary.csv"))
    i = len(data) - 1
    while data['Acc_Manual_over_AutoCounts'][i] < 1:
        i -= 1
    optimal_threshold = data['AutoCount_Thresh'][i + 1]

    return optimal_diameter, optimal_threshold


########


def cellcounting_batch(working_directory, params, use_watershed):
    Ch1_Counts = Count_folder(
        working_directory,
        params,
        Channel="Ch1",
        UseROI=False,
        UseWatershed=use_watershed,
        SaveIntensities=True
    )
    Ch1_Counts.to_csv(os.path.join(os.path.normpath(dirinfo['output']), "Ch1_Counts.csv"))
    return (Ch1_Counts)

#
# if __name__ == "__main__":
#     working_directory = "/Users/noahsmith/Documents/Hopkins Documents/Courses/S24 Courses/Software Carpentry/Final Project/ref code cell counting ZachPenn github"
#     particle_min = 0.05
#     use_watershed = True
#
#
#     dirinfo = {'main': working_directory}
#     # Populates dirinfo with paths to composite, mask, cell images, and an output container.
#     dirinfo = getdirinfo(dirinfo)
#     params = {'diam': 6,
#               'particle_min': particle_min,
#               'UseWatershed': True}
#
#     # send input parameters to optimizer
#     optimal_diameter, optimal_threshold = cellcounting_param_optimizer(dirinfo, params)
#
#     params['ch1_diam'] = optimal_diameter
#     params['ch1_thresh'] = optimal_threshold
#
#     # send input parameters to counter
#     output = cellcounting_batch(dirinfo, params, use_watershed)
#     print(output)
