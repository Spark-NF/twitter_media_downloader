# Twitter media downloader

## About
Downloads all videos and images from a Twitter account.

### Usage
```
twitter_media_downloader.py [-h] [-o DIR] [-f FORMAT] [-s IMAGE_SIZE] [-r] [-u] [-q] userid
```

On first run, the program will ask you for your OAuth token and secret. It will then be stored in a `.oauth.json` file so that you don't need to enter them every single time.

### Arguments
* `userid`: the account name or ID
* `-h`, `--help`: show the help and exit
* `-o DIR`, `--output DIR`: set the output directory where medias will be downloaded
* `-f FORMAT`, `--format FORMAT`: the filename format, see below for the available tokens to use
* `-s IMAGE_SIZE`, `--image-size IMAGE_SIZE`: the preferred image size to download, will fallback to the default size if not available
* `--since DATE`: the start date of the search, accepted formats: `YYYY-mm-dd HH:MM` and `YYYY-mm-dd` (defaults to 00:00)
* `--since-id ID`: the start ID of the search (exclusive)
* `--until DATE`: the end date of the search, accepted formats: `YYYY-mm-dd HH:MM` and `YYYY-mm-dd` (defaults to 00:00)
* `--until-id ID`: the end ID of the search (inclusive)
* `-r`, `--retweets`: also download medias from retweets
* `-u`, `--userid`: append the userid to the output directory
* `-q`, `--quiet`: disable output

### Example
```
python twitter_media_downloader.py -o out -f '[%date%] %filename%.%ext%' -s large -u Twitter
```

Will download all of the `Twitter` account media files into the `out/Twitter/` directory, each file named like `[2017-01-11 05-56-33] C13U6d-VQAAVKeY.jpg`.

## Available tokens for format
* `tweet_id`: the tweet identifier
* `original_tweet_id`: the tweet original identifier (different from `id` in the case of retweets)
* `date`: the tweet post date
* `original_date`: the tweet original post date (different from `date` in the case of retweets)
* `filename`: the file filename on the server
* `ext`: the file extension

## Authors
* [Nicolas Faure](https://github.com/Spark-NF)

## License
The program is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).