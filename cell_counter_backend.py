"""
Final Project - Development of a Python-based GUI for Interactive Cell Analysis and Quantification

Authors: Noah Daniel Smith, Valentina Matos Romero
Last Modified May 6, 2024

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
import fnmatch
import cv2
import numpy as np
import mahotas as mh
import pandas as pd
import scipy as sp
from skimage import filters
from skimage.segmentation import watershed as skwatershed
from skimage.feature import peak_local_max
from skimage import measure
import warnings

warnings.filterwarnings("ignore")

def median_filter(image, kernel_size):
    """
    Originally written by Zachary Pennington. Accepts an image and applies a median
    filter to remove noise using the scipy.ndimage median filter function.

    **Parameters**
        image: *np.ndarray*
            An array containing cell tissue image information.
        kernel_size: *int*
            Kernel used to apply the Gaussian blur; specified outside the function
            as half the optimal average cell diameter.
        
    **Returns**
        new_image: *np.ndarray*
            An array containing intensity information after noise filtering.
    """
    kernel_size = (kernel_size-1) if (kernel_size%2 == 0) else kernel_size
    image = sp.ndimage.median_filter(image, size=kernel_size)
    return image


def subtract_bg(image, kernel_size):
    """
    Originally written by Zachary Pennington. Accepts an image that was processed by
    a median filter to remove noise and subtracts away background using the openCV
    gaussian blur function with a relatively large e size

    **Parameters**
        image: *np.ndarray*
            An array containing image information.
        kernel_size: *int*
            Kernal used to apply the Gaussian blur; specified outside the function
            as three times the optimal average cell diameter.
        
    **Returns**
        new_image: *np.ndarray*
            An array containing intensity information after blur post-processing.
    """

    image = image.astype('float')
    bg = cv2.GaussianBlur(image,
                         (0,0),
                         kernel_size)
    new_image = image - bg
    new_image[new_image<0] = 0
    return new_image


def rm_smallparts (image, optimal_diam, particle_min):
    """
    Originally written by Zachary Pennington. Accepts an image that was processed by
    median filter and Gaussian blur to remove noise and 
    filter to remove noise using the scipy.ndimage median filter function.

    **Parameters**
        image: *np.ndarray*
            An array containing cell tissue image information.
        optimal_diameter: *int*
            The optimal average cell diameter for autocounting as determined previously
            by the cellcounting_param_optimizer function.
        particle_min:
            User-specified minimum particle size fraction of the ideal average cell area;
            below which cells are cut off.
        
    **Returns**
        new_image: *np.ndarray*
            An array containing intensity information after noise filtering, blur,
            and thresholding.
    """ 

    labeled, nr_objects = mh.label(image)
    sizes = mh.labeled.labeled_size(labeled)
    too_small = np.where(sizes < (optimal_diam*optimal_diam*particle_min))
    labeled = mh.labeled.remove_regions(labeled, too_small)
    image_current_thresholded = labeled != 0
    return image_current_thresholded

def cellcounter(file,channel,params,dirinfo,use_watershed=False,save_intensities=False):
    """
    Originally written by Zachary Pennington, edited by Noah Smith. Presented with an image
    file which is passed through the same pre-processing pipeline as the mask before being
    counted by the watershed algorithm or ndimage.label. Optionally, cell intensities can be
    saved to a .csv output file and total cell counts are always returned per image.

    **Parameters**
        file: *int*
            The number file in an ordered list to be pulled from filenames_current for
            processing. Used as a key.
        channel: *str*
            A string specifying the channel over which cells should be counted. The applet
            is only configured for single-channel counting, but eventually multichannel
            processing could be implemented using this parameter.
        params: *lib, str/int*
            A library containing various parameters that are important for cell counting,
            including optimal diameter and threshold for picking and whether or not counting
            should include watershed segmentation.
        dirinfo: *lib, str*
            A library containing the working directory and all pertinent subdirectories
            for the cell-count optimization and image processing.
        use_watershed: *bool*
            User-specified condition for whether or not the cell-counting process makes
            use of the watershed algorithm.
        save_intensities: *bool*
            Switch to determine whether individual cell intensities are saved in .csv files;
            for instance, they are saved during data processing but not during optimizations.
        
    **Returns**
        count_output: *lib, str/int/np.ndarray*
            A library containing data pertinent to the cell counting results; includes
            an image of the cells and several copies of the image after pre-processing;
            also includes the number of cells and the size of the image.
    """

    #Set function parameters in accordance with channel to be counted
    if channel == "Ch1":
        cell_diam = params['ch1_diam']
        thresh = params['ch1_thresh']
        directory_current = dirinfo['ch1']
        filenames_current = dirinfo['ch1_fnames']
        output = dirinfo['output_ch1']
    elif channel == "Optim":
        cell_diam = params['diam']
        thresh = params['thresh']
        directory_current = dirinfo['composite']
        filenames_current = dirinfo['composite_fnames']

    #Load file
    image_current_file = os.path.join(os.path.normpath(directory_current), filenames_current[file])
    image_current_gray = cv2.imread(image_current_file,cv2.IMREAD_ANYDEPTH)
    if channel != "Optim":
        print("Processing: " + filenames_current[file])

    #Process file
    image_current_median = median_filter(image_current_gray, kernel_size = cell_diam//2)
    image_current_BG = subtract_bg(image_current_median, kernel_size = cell_diam*3)
    image_current_gaussian = cv2.GaussianBlur(image_current_BG.astype('float'),(0,0),cell_diam/6)
    image_current_thresholded = rm_smallparts(image_current_gaussian > thresh, cell_diam, params['particle_min'])
    roi_size = image_current_gray.size

    if use_watershed == True:
        image_current_cells, nr_nuclei = watershed(image_current_thresholded, cell_diam, params['particle_min'])
    else:
        image_current_cells, nr_nuclei = sp.ndimage.label(image_current_thresholded)
        
    if save_intensities:
        cell_info = pd.DataFrame(columns=['{}_file'.format(channel),'cell_id','cell_size','cell_intensity'])
        for cell_id in np.unique(image_current_cells[image_current_cells>0]):
            cell_info_new = pd.DataFrame(
                {
                    '{}_file'.format(channel) : [filenames_current[file]],
                    'cell_id' : [cell_id],
                    'cell_size' : [len(image_current_cells[image_current_cells==cell_id])],
                    'cell_intensity' : [image_current_gaussian[image_current_cells==cell_id].mean()]
                },
            )
            cell_info = pd.concat([cell_info, cell_info_new], ignore_index = True)
        cell_info.to_csv(
            os.path.splitext(
                os.path.join(
                    os.path.normpath(output),
                    filenames_current[file]
                )
            )[0] + '_CellInfo.csv', 
            index=False
        )

    count_output = {
        'cells' : image_current_cells,
        'nr_nuclei' : nr_nuclei,
        'roi_size' : roi_size,
        'image' : image_current_gray,
        'gauss' : image_current_gaussian,
        'thresh' : image_current_thresholded
    }
    return count_output



def getdirinfo(dirinfo):
    """
    Originally written by Zachary Pennington, edited by Noah Smith. Parses subdirectories
    according to the naming scheme detailed in the readme.txt, allowing composite, mask,
    and data-containing images to be located by the script. Also generates an output
    subdirectory where the files generated by the script are saved.

    **Parameters**
        dirinfo: *lib, str*
            A library containing the working directory under which all of the image-containing
            subdirectories are stored.
        
    **Returns**
        dirinfo: *lib, str*
            A library containing the working directory and all pertinent subdirectories
            for the cell-count optimization and image processing.
    """
    dirinfo['composite'] = os.path.join(os.path.normpath(dirinfo['main']), "Composite")
    dirinfo['manual'] = os.path.join(os.path.normpath(dirinfo['main']), "ManualCounts")
    dirinfo['output'] = os.path.join(os.path.normpath(dirinfo['main']), "SavedOutput")
    if not os.path.isdir(dirinfo['output']): os.mkdir(dirinfo['output'])
    dirinfo['composite_fnames'] = sorted(os.listdir(dirinfo['composite']))
    dirinfo['composite_fnames'] = fnmatch.filter(dirinfo['composite_fnames'], '*.tif')
    dirinfo['manual_fnames'] = sorted(os.listdir(dirinfo['manual']))
    dirinfo['manual_fnames'] = fnmatch.filter(dirinfo['manual_fnames'], '*.tif')

    #Define subdirectories
    dirinfo['ch1'] = os.path.join(os.path.normpath(dirinfo['main']), "Ch1")
    dirinfo['output'] = os.path.join(os.path.normpath(dirinfo['main']), "SavedOutput")

    #Get filenames and create output subdirectories based upon usage
    if not os.path.exists(dirinfo['output']): os.mkdir(dirinfo['output'])
    if os.path.isdir(dirinfo['ch1']):
        dirinfo['ch1_fnames'] = sorted(os.listdir(dirinfo['ch1']))
        dirinfo['ch1_fnames'] = fnmatch.filter(dirinfo['ch1_fnames'], '*.tif')
        dirinfo['output_ch1'] = os.path.join(os.path.normpath(dirinfo['output']), "Ch1")
        if not os.path.isdir(dirinfo['output_ch1']): os.mkdir(dirinfo['output_ch1'])

    return dirinfo

def image_preprocessing(dirinfo,params):
    """
    Originally written by Zachary Pennington, edited by Noah Smith. Calculates auto-counted
    cells at varying threshold value to determine the appropriate threshold for a particular
    set of cell tissue images.

    **Parameters**
        dirinfo: *lib, str*
            A library containing the working directory and all pertinent subdirectories
            for the cell-count optimization and image processing.
        params: *lib, str/int*
            A library containing various parameters that are important for cell counting,
            including optimal diameter and threshold for picking and whether or not counting
            should include watershed segmentation.


    **Returns**
        images: *dict, array*
            Dictionary containing numpy arrays of all of the image data of the composite
            image after each step of pre-processing, including median filter noise removal, 
            background subtraction, and gaussian blur.
        params: *lib, str/int*
            A library containing various parameters that are important for cell counting,
            including optimal diameter and threshold for picking and whether or not counting
            should include watershed segmentation. The function adds Otsu's threshold for the
            given composite image.
    """

    images = {
        'manual' : cv2.imread(
            os.path.join(os.path.normpath(dirinfo['manual']), dirinfo['manual_fnames'][0]),
            cv2.IMREAD_ANYDEPTH
        ),
        'composite' : cv2.imread(
            os.path.join(os.path.normpath(dirinfo['composite']), dirinfo['composite_fnames'][0]),
            cv2.IMREAD_ANYDEPTH
        )
    }
    images['median'] = median_filter(images['composite'], kernel_size = params['diam']//2)
    images['bg'] = subtract_bg(images['median'], kernel_size = params['diam']*3)
    images['gauss'] = cv2.GaussianBlur(images['bg'],(0,0),params['diam']/6)
    params['counts'] = (images['manual']>0).sum()
    params['otsu'] = filters.threshold_otsu(image=images['gauss'].astype('int64'))
    params['thresh'] = params['otsu']
    
    images['otsu'] = images['gauss'] > params['thresh']

    return images, params


def threshold_optimizer(images, dirinfo, params, interv=1):
    """
    Originally written by Zachary Pennington, edited by Noah Smith. Calculates auto-counted
    cells at varying threshold value to determine the appropriate threshold for a particular
    set of cell tissue images.

    **Parameters**
        images: *dict, array*
            Dictionary containing numpy arrays of all of the image data of the composite
            image after each step of pre-processing, including median filter noise removal, 
            background subtraction, and gaussian blur.
        dirinfo: *lib, str*
            A library containing the working directory and all pertinent subdirectories
            for the cell-count optimization and image processing.
        params: *lib, str/int*
            A library containing various parameters that are important for cell counting,
            including optimal diameter and threshold for picking and whether or not counting
            should include watershed segmentation.
        interv: *int*
            An interval value that defines the step between threshold values tested by the
            optimizer.

    **Returns**
        optimization_data: *df*
            Pandas dataframe containing all of the pertinent information from the threshold
            optimization process. 
    """
    channel = 'Optim'
    file = 0 #Should always be zero because only one composite image

    #Initialize Arrays to Store Data In
    list_auto_counts = []
    list_cell_areas = []
    list_acc_auto_over_manual_counts = []

    #Define maximum threshold value and create series of thresholds to cycle through
    thresh_min = 0 #params['otsu']
    thresh_max = int(images['gauss'].max()//1) #Get maximum value in array.  Threshold can't go beyond this
    list_thresh_values = list(np.arange(thresh_min,thresh_max,interv))
    for thresh in list_thresh_values:

        params['thresh']=thresh
        #with suppress_stdout():
        count_out = cellcounter(file,channel,params,dirinfo,use_watershed=params['UseWatershed'])
        list_auto_counts.append(count_out['nr_nuclei'])

        #Determine Avg Cell Size in Pixel Units
        if count_out['nr_nuclei'] > 0:
            cell_area = count_out['cells'] > 0
            cell_area = cell_area.sum() / count_out['nr_nuclei']
        elif count_out['nr_nuclei'] == 0:
            cell_area = float('nan')
        list_cell_areas.append(cell_area)

        #Calculate Accuracies
        accuracy_over_manual_counts = count_out['nr_nuclei']/params['counts'] if count_out['nr_nuclei'] > 0 else np.nan
        list_acc_auto_over_manual_counts.append(accuracy_over_manual_counts)
    
    #Create Dataframe
    optimization_data = pd.DataFrame(
        {
            'AutoCount_Thresh': list_thresh_values,
            'OTSU_Thresh': np.ones(len(list_thresh_values))*params['otsu'],
            'Manual_CellDiam': np.ones(len(list_thresh_values))*params['diam'],
            'Manual_Counts': np.ones(len(list_thresh_values))*params['counts'],
            'AutoCount_UseWatershed': np.ones(len(list_thresh_values))*params['UseWatershed'],
            'AutoCount_Counts': list_auto_counts,
            'AutoCount_AvgCellArea': list_cell_areas,
            'Acc_Manual_over_AutoCounts': list_acc_auto_over_manual_counts,

        }
    )
    return optimization_data


def watershed(image_current_thresholded, optimal_diameter, particle_min):
    """
    Originally written by Zachary Pennington, edited by Noah Smith. A watershed
    segmentation algorithm that improves the accuracy of the counting algorithm by 
    handling and separating shapes that are touching. Makes use of scikitimage and 
    scipy to locate local maxima.

    **Parameters**
        image_current_thresholded: *np.ndarray*
            Cell tissue image after pre-processing that contains touching cells in need 
            of separation by the watershed algorithm
        optimal_diameter: *int*
            The optimal average cell diameter for autocounting as determined previously
            by the cellcounting_param_optimizer function.
        particle_min:
            User-specified minimum particle size fraction of the ideal average cell area;
            below which cells are cut off.

    **Returns**
        labels: *np.ndarray*
            N-dimensional array of the local maxima within the image as determined by the
            scikitimage watershed package.

        nseeds: *int*
            Number of nuclei located by the automatic cell counting algorithm, where nuclei
            are local maxima contained by each cell shape.
    """
    if image_current_thresholded.max() == True:

        image_current_thresh_dist = sp.ndimage.distance_transform_edt(image_current_thresholded)
        image_current_thresh_dist_erd = image_current_thresh_dist > optimal_diameter*particle_min
        image_current_thresh_dist_lbls = measure.label(image_current_thresh_dist_erd)
        
        coords = peak_local_max(
            image_current_thresh_dist, 
            min_distance = int(optimal_diameter),
            labels = image_current_thresh_dist_lbls,
            num_peaks_per_label = 1
        )
        image_current_seeds = np.zeros(image_current_thresholded.shape, dtype=bool)
        image_current_seeds[tuple(coords.T)] = True
        image_current_seeds, nseeds = sp.ndimage.label(image_current_seeds)
        labels = skwatershed(-image_current_thresh_dist, image_current_seeds, mask=image_current_thresholded)
    
    elif image_current_thresholded.max() == False:
        labels = image_current_thresholded.astype(int)
        nseeds = 0
    return labels, nseeds

def cellcounting_param_optimizer(dirinfo, params):
    """
    Utilizes a composite image and mask to determine the optimal diameter and threshold
    for cell counting within a set of images.

    **Parameters**

        dirinfo: *lib, str*
            A library containing the working directory and all pertinent subdirectories
            for the cell-count optimization and image processing.
        params: *lib, str/int*
            A library containing various parameters that are important for cell counting,
            including optimal diameter and threshold for picking and whether or not counting
            should include watershed segmentation.


    **Returns**

        optimal_diameter: *int*
            An average cell diameter deemed 'optimal' by iterating down in diameter until the
            automatic counts exceed manual counts.
        optimal_threshold: *int*
            An cell-picking threshold deemed 'optimal' by up in threshold by 10 until the
            automatic counts exceed manual counts. The penultimate threshold (before auto-counts
            exceed manual counts) is deemed optimal.

    """

    # Determines the manual and auto counts using preset Otsu threshold.
    images, params = image_preprocessing(dirinfo,params)
    count_output = cellcounter(
        0,
        "Optim",
        params,
        dirinfo,
        use_watershed=params['UseWatershed']
    )

    # Gradually decreases the average diameter until the manual counts exceed the manual counts.
    # Serves as a rough optimization which is smoothened by auto-thresholding.
    status = "...Optimizing average diameter..."
    print(status)

    while count_output['nr_nuclei'] < params['counts']:
        params['diam'] = params['diam']-1
        count_output = cellcounter(
        0,
        "Optim",
        params,
        dirinfo,
        use_watershed=params['UseWatershed']
        )
    
    optimal_diameter = params['diam']


    # Collects data on cell-counting at different threshold values.
    data = threshold_optimizer(images, dirinfo, params, interv=10)
    data.to_csv(os.path.join(os.path.normpath(dirinfo['output']), "OptimizationSummary.csv"))

    # Determines the optimum threshold value.
    status = "...Optimizing average threshold..."
    print(status)
    i = len(data)-1
    while data['Acc_Manual_over_AutoCounts'][i] < 1:
        i-=1
    optimal_threshold = data['AutoCount_Thresh'][i+1]

    return optimal_diameter, optimal_threshold


def cellcounting_batch(dirinfo, channel, params, save_intensities=False):
    """
    Iterates through all applicable files in the Ch1 subdirectory and passes them to the
    cellcounter function.

    **Parameters**

        dirinfo: *lib, str*
            A library containing the working directory and all pertinent subdirectories
            for the cell-count optimization and image processing.
        channel: *str*
            A string specifying the channel over which cells should be counted. The applet
            is only configured for single-channel counting, but eventually multichannel
            processing could be implemented using this parameter.
        params: *lib, str/int*
            A library containing various parameters that are important for cell counting,
            including optimal diameter and threshold for picking and whether or not counting
            should include watershed segmentation.


    **Returns**

        Ch1_Counts: *df*
            A pandas dataframe containing a summary of the counting performed on each
            channel one file within the Ch1 subdirectory.
    """

    global Ch1_Counts
    fnames = dirinfo['ch1_fnames']
    output = dirinfo['output_ch1']
    diam = params['ch1_diam']
    thresh = params['ch1_thresh']

    counts = []
    roi_size = []

    for file in range(len(fnames)):
        count_out = cellcounter(
            file,
            "Ch1",
            params,
            dirinfo,
            use_watershed=params['UseWatershed'],
            save_intensities=save_intensities
            )

        counts.append(count_out['nr_nuclei'])
        roi_size.append(count_out['roi_size'])
        cv2.imwrite(
            filename = os.path.splitext(
                os.path.join(
                    os.path.normpath(output),
                    fnames[file]
                )
            )[0] + '_Counts.tif',
            img = count_out['cells'].astype(np.uint16)
        )

    #Create DataFrame
    if channel == "Ch1":
        Ch1_Counts = pd.DataFrame(
        {'Ch1_FileNames': fnames,
         'Ch1_Thresh' : np.ones(len(fnames))*thresh,
         'Ch1_AvgCellDiam' : np.ones(len(fnames))*diam,
         'Ch1_ParticleMin' : np.ones(len(fnames))*params['particle_min'],
         'Ch1_Counts': counts,
         'Ch1_ROIsize': roi_size
        })


    # Ch1_Counts.to_csv(os.path.join(os.path.normpath(dirinfo['output']), "Ch1_Counts.csv"))

    return Ch1_Counts


# if __name__ == "__main__":
#     working_directory, particle_min, use_watershed = "/Users/noahsmith/Documents/Hopkins Documents/Courses/S24 Courses/Software Carpentry/Final Project/ref code cell counting ZachPenn github", 0.05, True #get input parameters from gui
#
#     # Populates dirinfo with paths to composite, mask, cell images, and an output container.
#     dirinfo = {'main' : working_directory}
#     dirinfo = getdirinfo(dirinfo)
#     params = {'diam' : 6,
#               'particle_min' : particle_min,
#               'UseWatershed' : True }
#
#     #send input parameters to optimizer
#     optimal_diameter, optimal_threshold = cellcounting_param_optimizer(dirinfo, params)
#     params['ch1_diam'] = optimal_diameter
#     params['ch1_thresh'] = optimal_threshold
#
#     #send input parameters to counter
#     output = cellcounting_batch(dirinfo, "Ch1", params, save_intensities=True)
#     print(output)
