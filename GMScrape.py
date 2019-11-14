"""Original code from https://github.com/ritvikmath/ScrapingData || Modified for use in Python3.x"""
import urllib3
import json
import csv
import time
import datetime

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


# function to return a list of URLS
def get_urls(origin, destination, api):
    # scraping googlemaps website
    site = 'https://maps.googleapis.com/maps/api/'

    # distancematrix service
    service = 'distancematrix/json?'

    # api key
    key = 'key=' + api

    # list of urls, combination of origins and destinations
    url = []

    # form url list
    for i in origin:
        for j in destination:
            if i != j:
                location = ('origins=' + i + '&destinations=' + j + '&departure_time=now&')
                url.append(site + service + location + key)

    return url


# test function, runs once
def scrape_gm_test(api, source, destination):
    # get co-ordinates
    src = source.values()
    out = destination.values()

    # get keys
    in_keys = source.keys()
    out_keys = destination.keys()

    # fetch request urls
    request_urls = get_urls(src, out, api)

    # open file
    # with open('traffic_data.csv', 'w') as file:
    #   w = csv.writer(file)

    # number of sources
    src_len = len(src)
    row = ['timestamp']
    for i in range(src_len):
        row.append('travel_time' + in_keys[i] + ' to ' + out_keys[i])
    #   w.writerow(row)
    #    step = 1
    #   while (step <= int(duration * 60 / freq)):

    # number of request urls

    # lists for data, traffic_times, batch

    data = []
    traffic_times = []

    for i in request_urls:
        data.append(json.loads(req_data_from_url(i)))
    for i in data:
        traffic_times.append(data['rows'][0]['elements'][0]['duration_in_traffic']['text'])
    batch = [datetime.datetime.now()]
    for i in traffic_times:
        batch.append(i)
    print(batch)
    #   w.writerow(batch)

    #        if (step % 10 == 0):
    #           print(str(step) + ' datapoints gathered')
    #        step += 1
    #        time.sleep(freq * 60)
    # data = json.loads(req_data_from_url(request_url))
    # traffic_time = data['rows'][0]['elements'][0]['duration_in_traffic']['text']
    # print(str(datetime.datetime.now())+" --- "+str(traffic_time))


# Main Scrape_function, runs for bounded time ||| Not yet tested
def scrape_gm(api, source, destination, freq, duration):
    # get co-ordinates
    src = source.values()
    out = destination.values()

    # get keys
    in_keys = source.keys()
    out_keys = destination.keys()

    # fetch request urls
    request_urls = get_urls(src, out, api)

    # open file
    with open('traffic_data.csv', 'w') as file:
        w = csv.writer(file)

        # number of sources
        src_len = len(src)
        row = ['timestamp']
        for i in range(src_len):
            row.append('travel_time' + in_keys[i] + ' to ' + out_keys[i])
        w.writerow(row)
        step = 1
        while (step <= int(duration * 60 / freq)):

            # number of request urls

            # lists for data, traffic_times, batch

            data = []
            traffic_times = []

            for i in request_urls:
                data.append(json.loads(req_data_from_url(i)))
            for i in data:
                traffic_times.append(data['rows'][0]['elements'][0]['duration_in_traffic']['text'])
            batch = [datetime.datetime.now()]
            for i in traffic_times:
                batch.append(i)
            w.writerow(batch)
            print(batch)
            if (step % 10 == 0):
                print(str(step) + ' datapoints gathered')
            step += 1
            time.sleep(freq * 60)
    # data = json.loads(req_data_from_url(request_url))
    # traffic_time = data['rows'][0]['elements'][0]['duration_in_traffic']['text']
    # print(str(datetime.datetime.now())+" --- "+str(traffic_time))


# Main function | Incomplete code
def main():
    api_key = input("Enter API key: ")
    origin = {
        'Link_Road': '',
        'Kakoli':''
    }
    destination = {}
    # f = int(input('Enter Frequency in minutes: '))
    # d = int(input('How long to scrape in hours: '))
    # scrape_gm(api_key, origin, destination, f, d)


if __name__ == '__main__':
    main()
