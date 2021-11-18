import requests
import shutil
from tqdm import tqdm, trange
import argparse
import math
import os

class Scrapper:
    def __init__(self,collection, output_dir, num_of_iterations, order_by, order_direction, offset, limit=50):
        self.base_url = "https://api.opensea.io/api/v1/assets"
        self.limit = limit
        self.offset = offset
        self.payload = {'order_by':order_by,'order_direction': order_direction, 'offset': self.offset, 'limit': self.limit, 'collection':collection}
        self.counter = 1 # for naming the img files
        self.nfts = []
        self.image_links = []
        self.output_dir = output_dir
        self.number_of_images = num_of_iterations

    def scrap(self):
        try:
            req = requests.get(self.base_url, params=self.payload)
            self.nfts = req.json()["assets"]
        except Exception:
            print(req.json())

    def get_image_urls(self):
        for item in self.nfts:
            self.image_links.append(item["image_url"])

    def download_images(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        for i, link in enumerate(tqdm(self.image_links)):
            response = requests.get(link, stream=True)
            with open('{0}/{1}.png'.format(self.output_dir, self.counter), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            self.counter += 1

def main(args):
    scrapper = Scrapper(args.collection, args.output, args.iterations, args.order, args.sort, args.offset)
    for i in trange(0, scrapper.number_of_images, scrapper.limit):
        scrapper.payload['offset'] = i*scrapper.limit
        if (scrapper.number_of_images-(scrapper.offset*scrapper.limit) <= 50 ):
            scrapper.payload['limit'] = scrapper.number_of_images-scrapper.offset*scrapper.limit
        scrapper.scrap()
        scrapper.get_image_urls()
    scrapper.download_images()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Adding optional argument
    parser.add_argument("-c", "--collection", help="Collection Name", required=True)
    parser.add_argument("-o", "--output", help="Output directory", default="./output")
    parser.add_argument("-i", "--iterations", help="Number of images to download", type=int, default=10)
    parser.add_argument("-ob", "--order", help="Order by", default="pk")
    parser.add_argument("-s", "--sort", help="Output directory", default="desc")
    parser.add_argument("-ofs", "--offset", help="offset", type=int, default=0)
    
    # Read arguments from command line
    args = parser.parse_args()
    main(args)

