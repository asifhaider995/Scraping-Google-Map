"""Original code from https://github.com/ritvikmath/ScrapingData || Modified for use in Python3.x"""
import urllib3
import json
import csv
import time
import datetime


def req_data_from_url(url):
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    req = http.request('GET', url)
    success = False
    while success is False:
        try:
            # open the url
            if (req.status == 200):
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)
            print("Error for Url " + url + ": " + str(datetime.datetime.now()))
            print("Retrying")
    return req.data


def scrape_gm(api, src, dest, freq, duration):
    # we want to scrape the googlemaps website
    site = 'https://maps.googleapis.com/maps/api/'

    # we want to use the distancematrix service
    service = 'distancematrix/json?'

    # input origin and destination from the user
    locations = 'origins=' + src + '&destinations=' + dest + '&departure_time=now&'

    # input api key from user
    key = 'key=' + api

    # construct request url
    request_url = site + service + locations + key
    with open('traffic_data.csv', 'w') as file:
        w = csv.writer(file)
        w.writerow(['timestamp', 'travel_time'])
        step = 1
        while (step <= int(duration * 60 / freq)):
            data = json.loads(req_data_from_url(request_url))
            traffic_time = data['rows'][0]['elements'][0]['duration_in_traffic']['text']
            batch = (datetime.datetime.now(), traffic_time)
            w.writerow(batch)
            print(batch)
            if (step % 10 == 0):
                print(str(step) + ' datapoints gathered')
            step += 1
            time.sleep(freq * 60)
    # data = json.loads(req_data_from_url(request_url))
    # traffic_time = data['rows'][0]['elements'][0]['duration_in_traffic']['text']
    # print(str(datetime.datetime.now())+" --- "+str(traffic_time))


def main():
    api_key = input("Enter API key: ")
    origin = input("Enter Origin co-ordinates: ")
    destination = intput("Enter Origin co-ordinates: ")
    f = int(input('Enter Frequency in minutes: '))
    d = int(input('How long to scrape in hours: '))
    scrape_gm(api_key, origin, destination, f, d)


if __name__ == '__main__':
    main()
