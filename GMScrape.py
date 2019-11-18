"""Original code from https://github.com/ritvikmath/ScrapingData || Modified for use in Python3.x"""

import os
import urllib3
import json
import csv
import time
import datetime

from itertools import combinations


# requests data from a single url
def req_data_from_url(url):
    urllib3.disable_warnings()
    http = urllib3.PoolManager(num_pools=22)
    success = False

    while success is False:
        try:
            # open the url
            x = len(url)
            req = http.request('GET', url)
            if (req.status == 200):
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)
            print("Error for Url " + url + ": " + str(datetime.datetime.now()))
            print("Retrying")
    return req.data


# function to gernerate list of URLS
def get_urls(origin, destination, api):
    # scraping googlemaps website
    site = 'https://maps.googleapis.com/maps/api/'

    # distancematrix service
    service = 'distancematrix/json?'

    # api key
    key = 'key=' + api

    # list of urls, combination of origins and destinations
    url = list()

    # form url list
    x = len(origin)
    for i in range(x):
        location = ('origins=' + origin[i] + '&destinations=' + destination[i] + '&departure_time=now&')
        url.append(site + service + location + key)

    return url


# Function to check if file exists
def file_is_empty(file):
    if os.path.exists(file):
        return os.path.getsize(file) > 0
    else:
        return False

# Function to generate CSV header
def get_csv_header(urls, in_keys, out_keys):
    print('Getting Header...')
    temp_data = list()
    distances = list()
    for i in urls:
        temp_data.append(json.loads(req_data_from_url(i)))

    # for each data take out distance of route
    for i in temp_data:
        distances.append((i['rows'][0]['elements'][0]['distance']['text']))

    # number of sources
    _len = len(out_keys)
    row = ['timestamp']

    # Append route distance with route name
    for i in range(_len):
        row.append('tr_time(min): \n' + in_keys[i] + ' to ' + out_keys[i] + '(' + distances[i] + ')')

    # Write row to file
    return row


# Main Scrape_function, runs for bounded time ||| Not yet tested
def scrape_gm(api, nodes, freq, duration, filename):
    locations = nodes.keys()
    src_keys = list()
    dest_keys = list()
    src = list()
    out = list()
    comb = list(combinations(locations, 2))
    for i in comb:
        src.append(nodes[i[0]])
        out.append(nodes[i[1]])
        src_keys.append(i[0])
        dest_keys.append(i[1])

    # fetch request urls
    request_urls = get_urls(src, out, api)

    # Checks if file exists and is empty
    if file_is_empty(filename):
        action = 'a'
    else:
        action = 'w'
    # open file
    with open(filename, action) as file:
        w = csv.writer(file)
        if action == 'w':
            header = get_csv_header(request_urls, src_keys, dest_keys)
            print('Writing Header...')
            # Write header
            w.writerow(header)
        step = 1
        limit = int(duration * 60 / freq)
        while step <= limit:
            # timer
            start = time.time()

            # lists for data, traffic_times
            data = list()
            traffic_times = list()

            # appends all data unloaded by json in list
            print('Getting Data...')
            for i in request_urls:
                data.append(json.loads(req_data_from_url(i)))

            # for each data appends all the traffic times in minutes after striping trailing characters
            for i in data:
                traffic_times.append((i['rows'][0]['elements'][0]['duration_in_traffic']['text']).strip(' mins'))

            # init batch list with current datetime
            batch = [datetime.datetime.now()]

            # append traffic times in batch list
            for i in traffic_times:
                batch.append(i)

            # write batch list in rows in .csv
            w.writerow(batch)
            print(batch)

            # prints steps after gathering 'freq' number of data points
            if step % freq == 0:
                print(str(step) + ' data points gathered')
            step += 1

            end = time.time()
            elapsed = end - start
            progress = int((step / limit) * 100)
            print('Progress: ' + str(progress) + '%')

            # let program sleep for freq*60 seconds
            if elapsed < freq * 60:
                time.sleep(freq * 60)

# Main function 
def main():
    # All nodes
    all_nodes = {
        'G1': '23.780622,90.425636',  # Gulshan 1
        'G2': '23.794843,90.414243',  # Gulshan 2
        'B': '23.782115,90.425768',  # Badda
        'M': '23.777927,90.397985',  # Mohakhali
        'H': '23.772249,90.414066',  # Hatirjheel
        'NB': '23.797697,90.423514',  # Notun Bazar
        'K': '23.792478,90.400619',  # Kakoli
        'MB': '23.770742,90.424925',  # Merul Badda
        'TJ': '23.761468,90.394344',  # Tejgaon
        'JFP': '23.813985, 90.421195',  # Jamuna Future Park, Bashundhara
        'SS': '23.790710, 90.388188',  # Shadheenota Shoroni
        'N2': '23.837566, 90.418286',  # Ninkunja 2
        'C': '23.816430,90.405198',  # Dhaka Cantonment
        'M11': '23.819824, 90.365092'  # Mirpur
    }
    api_key = 'input('Enter API Key: ')
    filename = 'Log' + str(datetime.date.today()) + '.csv'
    f = 10 # Scrapping frequency in minutes
    d = float(input('Enter Scrape period in hours: ')) # Scrapping period
    scrape_gm(api_key, all_nodes, f, d, filename)


if __name__ == '__main__':
    main()
