import pickle
import numpy as np


def convert_to_dict(step_data):
    """
    Convert a list of grain ID pairs into a dictionary mapping.

    Args:
        step_data (list of lists): List of [initial, link] pairs.

    Returns:
        dict: Dictionary where each key is an initial grain ID and the value 
              is a list of linked grain IDs after the step.
    """
    mapping = {}
    for initial, link in step_data:
        if isinstance(link, list):
            mapping[initial] = link
        else:
            mapping[initial] = [link]
    return mapping


with open(r"Grain Track Data/step01_track_result_dict.pickle", "rb") as f:
    step1 = pickle.load(f)
with open(r"Grain Track Data/step23_track_result_dict.pickle", "rb") as f:
    step2 = pickle.load(f)
with open(r"Grain Track Data/step34_track_result_dict.pickle", "rb") as f:
    step3 = pickle.load(f)
with open(r"Grain Track Data/step45_track_result_dict.pickle", "rb") as f:
    step4 = pickle.load(f)
with open(r"Grain Track Data/step56_track_result_dict.pickle", "rb") as f:
    step5 = pickle.load(f)
with open(r"Grain Track Data/step67_track_result_dict.pickle", "rb") as f:
    step6 = pickle.load(f)

steps = [step1, step2, step3, step4, step5, step6]

merged_step_maps = []
confident_tracks = []
retrack_results = []
trip_start_grains = []

for step_data in steps:
    confident_track = convert_to_dict(step_data['confident_track'])
    retrack_result = convert_to_dict(step_data['retrack_result'])
    # split = convert_to_dict(step_data['split_grains'])
    trip_start_grain = convert_to_dict(step_data['trip_start_grains'])
    # position = convert_to_dict(step_data['track_based_on_position'])
    
    confident_tracks.append(confident_track)
    retrack_results.append(retrack_result)
    trip_start_grains.append(trip_start_grain)

    merged_map = {}
    for d in [confident_track, retrack_result, trip_start_grain]: 
        for id, linked_id in d.items(): # Merge confident_track, retrack_result and trip_start_grains into single dictionary
            if id in merged_map:
                merged_map[id].extend(linked_id) # If a link to id already exists, add the new linked_id.
            else:
                merged_map[id] = linked_id[:] # Set key (id) to copy of linked_id list 

    merged_step_maps.append(merged_map)

linked_grain_map = {}

for initial_id in merged_step_maps[0].keys():
    grain_id_links = [] # Stores all subsequent linked grain ids for initial_id
    curr_grain_ids = [initial_id]

    for map in merged_step_maps: # Iterate through subsequent linked grain ids
        # print(initial_id)
        next_grain_ids = []
        for curr_grain in curr_grain_ids:
            next_grain_id = map.get(curr_grain) # Obtain grain ID in next step
            if next_grain_id is None: # continue if next_grain_id does not exist in the subsequent step map
                # print(f'{curr_grain} vanished')
                continue
            next_grain_ids.extend(next_grain_id) # Add next linked grain id(s) to next_grain_ids

        grain_id_links.append(next_grain_ids) # Add links for this step to grain_id_links
        curr_grain_ids = next_grain_ids

    linked_grain_map[initial_id] = grain_id_links 

print(linked_grain_map)

with open("linked_grain_map.pkl", "wb") as f:
    pickle.dump(linked_grain_map, f)