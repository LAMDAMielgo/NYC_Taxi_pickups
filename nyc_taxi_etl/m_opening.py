# -------------- files
import os
import zipfile
import requests
from io import BytesIO
import time

# -------------- for data
import numpy as np
import pandas as pd

# -------------------------------------------------------------------------------------------------------- FUNCTIONS FOR FILE LOADING

def request_info_from_ZIP(zipfile_dir):
    """
    input
    output
    """
    print(f"---------------------- Getting ZIP file")
    tic = time.perf_counter()

    response = requests.get(zipfile_dir, stream=True)
    f = BytesIO()
    f.write(response.content)

    toc = time.perf_counter()
    mins = (toc - tic) // 60;
    secs = np.around((toc - tic) % 60, 3)

    print(f"---------------------- Done in {mins}'{secs}''")
    return f

def getting_df_fromZip(zipfile_info, minLen_toDisgard, first_row = 5, num_rows = 35):
    """
    input
    output
    """
    filenames, frame_to_concat = [], []
    # Open and concat df
    print(f"---------------------- Opening ZIP file and construction of DF \n");
    tic = time.perf_counter()

    with zipfile.ZipFile(zipfile_info) as zip_:
        for filename in zip_.namelist():
            if len(filename) > minLen_toDisgard:
                # there is a folder data/ with nothing inside
                # this is to only pick valid textfiles
                # based on their lenght
                with zip_.open(filename) as file_:
                    if len(filenames) == 0:
                        # for first file in data.zip
                        first_frame = pd.read_csv(file_, sep=',', low_memory=False)
                        # for the sake of the exercise
                        # only 1 every 35 rows are read
                        frame_to_use = first_frame.loc[first_row::num_rows, :]
                        #
                        column_names = first_frame.columns.tolist()
                        filenames.append(filename);
                        frame_to_concat.append(frame_to_use)
                        memory_usage = frame_to_use.memory_usage(index=True, deep=False).sum() / (1000 * 1024)
                        print(
                            f"{filename} \tDone \t Memory Usage: {np.around(memory_usage, 2)} Mb \t Shape {frame_to_use.shape}")

                    else:
                        new_frame = pd.read_csv(file_, sep=',', names=column_names, low_memory=False)
                        # for the sake of the exercise
                        # only 1 every 35 rows are read
                        frame_to_use = new_frame.loc[first_row::num_rows, :]
                        #
                        filenames.append(filename);
                        frame_to_concat.append(frame_to_use)
                        memory_usage += frame_to_use.memory_usage(index=True, deep=False).sum() / (1000 * 1024)

                        print(
                            f"{filename} \tDone \t Memory Usage: {np.around(memory_usage, 2)} Mb \t Shape {frame_to_use.shape}")

    toc = time.perf_counter();
    mins = (toc - tic) // 60;
    secs = np.around((toc - tic) % 60, 3)
    print(
        f"\n ---------------------- Done Running all in {mins}'{secs}'' \t Total frames {len(frame_to_concat)} return as {type(frame_to_concat)}")
    # returns list of list of DFs
    return frame_to_concat