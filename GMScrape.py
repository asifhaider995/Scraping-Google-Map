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
            print("Retrying...")
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



# Scrape_function, runs for bounded time
def scrape_gm(api, source, destination, freq, duration,fname):
    
    # get co-ordinates, values
    src = list(source.values())
    out = list(destination.values())
    
    # get keys
    in_keys = list(source.keys())
    out_keys = list(destination.keys())
    
    # fetch request urls
    request_urls = get_urls(src, out, api)

    # open file
    with open(fname, 'w') as file:
        w = csv.writer(file)

        # number of destinations
        dest_len = len(out)
        row = ['timestamp']
        for i in range(dest_len):
            row.append('travel_time(in mins): \n' + in_keys[0] + ' to ' + out_keys[i])

        w.writerow(row)
        step = 1
        while (step <= int(duration * 60 / freq)):
            start = time.time()
     
            # lists for data, traffic_times

            data = list()
            traffic_times = list()

            # appends all data unloaded by json in list for all request urls
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

            #prints steps after gathering 'freq' number of data points
            if (step % freq == 0):
                print(str(step) + ' data points gathered')
            step += 1

            end = time.time()
            elapsed = end - start
            
            # let program sleep for freq*60 seconds minus time elapsed to run current step
            time.sleep((freq * 60) - elapsed)


# Main function
def main():
    api_key = input('Enter API key: ')
    filename = (input('Enter CSV file name: '))+'.csv'
    origin = {
        'Gulshan_1': '23.780622,90.425636',
    }
    destination = {
        'Gulshan_2': '23.794843,90.414243',
        'Badda': '23.780626,90.425631',
        'Mohakhali': '23.777927,90.397985',
        'Hatirjheel': '23.772249,90.414066',
        'Notun_Bazar': '23.797697,90.423514',
        'Kakoli': '23.792478,90.400619',
        'Merul': '23.770742,90.424925',
        'Tejgaon': '23.761468,90.394344',
        'JFPark': '23.813985, 90.421195',
        'ShadhSoroni': '23.790710, 90.388188',
        'Nikuja_2': '23.837566, 90.418286',
        'Cantonment': '23.816430,90.405198',
        'Mirpur': '23.819824, 90.365092'
    }
    f = int(input('Enter scrape frequency (in minutes): '))
    d = float(input('Enter total scrape period (in hours): '))
    scrape_gm(api_key, origin, destination, f, d,filename)


if __name__ == '__main__':
    main()
