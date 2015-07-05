import pinboard
import datetime
import os

def is_youtube_url(url):
    return "youtube.com" in url or "youtu.be" in url

def download_and_backup(post):
    import youtube_dl

    url = post.url
    print "Starting download of %(url)" % locals()
    
    def my_hook(d):
        if d['status'] == 'finished':
            filename = d['filename']
            backup(post, filename)

    opts = {
        'progress_hooks': [my_hook],
        }
    
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([url])

def backup(post, filename):
    f = open(filename, 'rb')
    
    # upload to s3
    import tinys3
    s3_access_key = os.environ['S3_ACCESS_KEY']
    s3_secret_key = os.environ['S3_SECRET_KEY']
    conn = tinys3.Connection(s3_access_key, s3_secret_key, tls=True)
    conn.upload(filename, f, 'pinboard-youtube')
    
    # update Pinboard with s3 URL

def main:
    api_token = os.environ['PINBOARD_API_TOKEN']
    
    pb = pinboard.Pinboard(api_token)

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    recent_bookmarks = pb.posts.all(results=100, fromdt=yesterday)["posts"]

    youtube_bookmarks = [x for x in recent_bookmarks if is_youtube_url(x.url)]

    for bookmark in youtube_bookmarks:
        download_and_backup(bookmark)
    

    
if __name__ == "__main__": main()
