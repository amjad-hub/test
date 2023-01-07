from pathlib import Path
import numpy as np
from convertation_func import *

map_folder_name = 'map_1'  # название только в таком формате

traj_number = 10 # количество траекторий на карте
tx_pos_number = 10 # количество координат tx для каждой траектории
# path = Path(Path.home(), 'raytracing progs', 'data', map_folder_name)
# path = f'data/{map_folder_name}'


traj_arrival_list = []
traj_departure_list = []
for traj in range(traj_number):
    # path_to_traj_folder = Path(path, f'traj{traj+1}')
    path_to_traj_folder = f'data/{map_folder_name}/traj{traj+1}'
    print(path_to_traj_folder)
    arrival, departure = save_all_tx_pos(path_to_traj_folder, tx_pos_number)
    traj_arrival_list.append(arrival)
    traj_departure_list.append(departure)


# path_to_save = Path(Path.home(), 'raytracing progs', 'data', map_folder_name)
path_to_save = f'data/{map_folder_name}'
path_arrival = Path(path_to_save, 'data_arrival.npy')
path_departure = Path(path_to_save, 'data_departure.npy')
np.save(path_arrival, np.asarray(traj_arrival_list, dtype=object))
np.save(path_departure, np.asarray(traj_departure_list, dtype=object))
# чтобы открыть эти файлы нужна команда:
# array = np.load(path_array, allow_pickle=True)