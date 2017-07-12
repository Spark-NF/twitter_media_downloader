# Twitter media downloader

## About
Downloads all videos and images from a Twitter account.

### Usage
```
twitter_media_downloader.py [-h] [-o DIR] [-f FORMAT] [-s IMAGE_SIZE] [-r] [-u] [-q] userid
```

On first run, the program will ask you for your OAuth token and secret. It will then be stored in a `.oauth.json` file so that you don't need to enter them every single time.

### Example
```
python twitter_media_downloader.py -o out -f '[%date%] %filename%.%ext%' -s large -u Twitter
```

Will download all of the `Twitter` account media files into the `out/Twitter/` directory, each file named like `[2017-01-11 05-56-33] C13U6d-VQAAVKeY.jpg`.

## Available tokens for format
* `date`: the tweet post date
* `original_date`: the tweet original post date (different from `date` in the case of retweets)
* `filename`: the file filename on the server
* `ext`: the file extension

## Authors
* [Nicolas Faure](https://github.com/Spark-NF)

## License
The program is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).