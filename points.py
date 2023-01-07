import math
import os
from pathlib import Path

import numpy as np


def get_path_length(lat1, lng1, lat2, lng2):
    # '''calculates the distance between two lat, long coordinate pairs'''
    r = 6371000  # radius of earth in m
    lat1rads = math.radians(lat1)
    lat2rads = math.radians(lat2)
    delta_lat = math.radians((lat2 - lat1))
    delta_lng = math.radians((lng2 - lng1))
    a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + math.cos(
        lat1rads) * math.cos(lat2rads) * math.sin(delta_lng / 2) * math.sin(
        delta_lng / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = r * c
    return d


def get_destination_lat_long(lat, lng, azimuth, distance):
    # '''returns the lat an long of destination point
    # given the start lat, long, aziuth, and distance'''
    r = 6378.1  # Radius of the Earth in km
    brng = math.radians(azimuth)  # Bearing is degrees converted to radians.
    d = distance / 1000  # Distance m converted to km
    lat1 = math.radians(lat)  # Current dd lat point converted to radians
    lon1 = math.radians(lng)  # Current dd long point converted to radians
    lat2 = math.asin(
        math.sin(lat1) * math.cos(d / r) + math.cos(lat1) * math.sin(
            d / r) * math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / r) * math.cos(lat1),
                             math.cos(d / r) - math.sin(lat1) * math.sin(lat2))
    # convert back to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return [lat2, lon2]


def calculate_bearing(lat1, lng1, lat2, lng2):
    # '''calculates the azimuth in degrees from start point to end point'''
    start_lat = math.radians(lat1)
    start_long = math.radians(lng1)
    end_lat = math.radians(lat2)
    end_long = math.radians(lng2)
    d_long = end_long - start_long
    d_phi = math.log(math.tan(end_lat / 2.0 + math.pi / 4.0) / math.tan(
        start_lat / 2.0 + math.pi / 4.0))
    if abs(d_long) > math.pi:
        if d_long > 0.0:
            d_long = -(2.0 * math.pi - d_long)
        else:
            d_long = (2.0 * math.pi + d_long)
    bearing = (math.degrees(math.atan2(d_long, d_phi)) + 360.0) % 360.0
    return bearing


def generate_points(interval, azimuth, lat1, lng1, lat2, lng2):
    # '''returns every coordinate pair inbetween two coordinate
    # pairs given the desired interval'''

    d = get_path_length(lat1, lng1, lat2, lng2)
    remainder, dist = math.modf((d / interval))
    counter = float(interval)
    coords = [[lat1, lng1]]
    for distance in range(0, int(dist)):
        coord = get_destination_lat_long(lat1, lng1, azimuth, counter)
        counter = counter + float(interval)
        coords.append(coord)
    coords.append([lat2, lng2])
    return coords


def generate_linear_trajectories(path, array: np.ndarray, interval: float,
                                 map_number: int, senario:int):

    for i, points in enumerate(array):
        lat1 = points[0]
        lng1 = points[1]
        lat2 = points[2]
        lng2 = points[3]
        azimuth = calculate_bearing(lat1, lng1, lat2, lng2)
        coords = generate_points(interval, azimuth, lat1, lng1, lat2, lng2)
        # np.savetxt(path / f'+1}.txt', coords)
        if not os.path.exists(f'{path}/senario_{senario}'):
            os.mkdir(f'{path}/senario_{senario}')
        np.savetxt(f'{path}/senario_{senario}/map{map_number}_{i+1}.txt', coords)
    print('Траектории сгенерированы и сохраены успешно в папку: ', path)

