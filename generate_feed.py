import yaml
import requests
from copy import deepcopy
import os
from boto import connect_s3
import boto.s3 as s3
import os.path as path
from jinja2 import Template
from datetime import datetime
from dateutil import parser

PREFIX = 'https://graph.facebook.com/v2.3/'


class Config:
    def __init__(self, data):
        self.data = data

    @classmethod
    def load(cls, filepath=None):
        if filepath is None:
            filepath = 'config.yaml'

        with open(filepath) as f:
            config = yaml.load(f)
        return cls(config)

    def get(self, key):
        keys = key.split('.')
        d = self.data
        for key in keys:
            d = d.get(key)
        return d

config = Config.load()


class S3Uploader:
    def __init__(self):
        conn = connect_s3(*aws_creds())
        self.bucket = conn.get_bucket(config.get('deploy.url'), validate=False)

    def upload_string(self, string, key_name, mime_type=None):
        key = s3.key.Key(self.bucket)
        key.key = key_name
        if mime_type is not None:
            key.set_metadata("Content-Type", mime_type)
        key.set_contents_from_string(string)

    def upload_url(self, url, key_name, mime_type=None):
        res = requests.get(url)
        return self.upload_string(res.content, key_name, mime_type)

    def upload_image(self, image):
        pairs = []
        if image.get('url'):
            pairs.append((image.get('url'), ''))
        if image.get('url_small'):
            pairs.append((image.get('url_small'), '_small'))
        for url, suffix in pairs:
            key_name = path.join(
                config.get('deploy.root_path'),
                'images',
                image['id'] + suffix + '.jpg',
            )
            self.upload_url(url, key_name, 'image/jpeg')
        print 'Uploaded image', image

    def list_bucket(self):
        return {key.name: key.etag[1:-1]
                for key in self.bucket.get_all_keys()}


def fb_token():
    return os.environ['FB_ACCESS_TOKEN']


def aws_creds():
    return os.environ['AWS_ACCESS_KEY'], os.environ['AWS_ACCESS_TOKEN']


def get_obj_info(obj, fields=None):
    params = dict(access_token=fb_token())
    if fields:
        params['fields'] = ','.join(fields)
    url = PREFIX + ('%s/' % obj['id'])
    print 'Fetching', url
    res = requests.get(url, params=params)
    return res.json()


def get_posts_in_object_feed(obj, post_type=None, fields=None):
    fields = fields or []
    url = PREFIX + ('%s/feed' % obj['id'])
    print 'Fetching', url
    res = requests.get(url, params=dict(
        access_token=fb_token(),
        ))
    data = res.json()
    if post_type is not None:
        data = filter(lambda x: x.get('type') == post_type, data['data'])
    results = []
    for d in data:
        result = dict(id=d.get('object_id'))
        for field in fields:
            result[field] = d.get(field)
        results.append(result)
    return results


def get_event_info(event):
    data = get_obj_info(event, ['photos', 'name', 'id', 'start_time'])
    photos = []
    for photo in data.get('photos', {}).get('data', []):
        d = dict(id=photo.get('id'))
        images = photo.get('images')
        if images:
            d['url'] = images[0].get('source')  # biggest image
            if images[0].get('height') > 400:
                for image in images:
                    if 300 < image.get('height') < 400:
                        d['url_small'] = image.get('source')
        photos.append(d)
    data['photos'] = photos
    return data


def get_group_event_stream(group):
    results = get_posts_in_object_feed(group, 'event', ['name', 'link'])
    return filter(lambda x: group['name'] in x['name'], results)


def construct_events_page(events):
    utc_now = datetime.utcnow().replace(tzinfo=parser.tz.tzutc())
    events = deepcopy(events)
    events_t = []
    for e in events:
        if e.get('start_time'):
            e['start_time'] = parser.parse(e['start_time'])
            e['display_date'] = e['start_time'].strftime('%B %-d, %Y')
            if e['start_time'] <= utc_now:
                events_t.append(e)
    events_t.sort(key=lambda x: x['start_time'], reverse=True)
    events = events_t

    with open('templates/feed.j2') as f:
        template = Template(f.read())
    for event in events:
        for image in event.get('photos', []):
            if image.get('url_small'):
                suffix = '_small'
            else:
                suffix = ''
            image['url'] = path.join(
                '/feed/images',
                image['id'] + suffix + '.jpg',
                )
    return template.render(events=events)


def main():
    with open('chapters.yaml') as f:
        data = yaml.load(f)

    events = []
    for chapter in data['chapters']:
        chapter['events'] = get_group_event_stream(chapter)
        events.extend(chapter['events'])

    photos = []
    for event in events:
        info = get_event_info(event)
        event['start_time'] = info['start_time']
        event['photos'] = info['photos']
        photos.extend(info['photos'])

    print yaml.safe_dump(data)

    uploader = S3Uploader()

    uploaded_images = set(path.splitext(path.basename(k))[0]
                          for k in uploader.list_bucket().iterkeys())
    for image in photos:
        if image['id'] not in uploaded_images:
            uploader.upload_image(image)

    events_page = construct_events_page(events)

    try:
        os.makedirs('output/feed')
    except OSError:
        pass
    with open('output/feed/index.html', 'w') as f:
        f.write(events_page)

    key_name = path.join(
        config.get('deploy.root_path'),
        'index.html',
        )
    uploader.upload_string(events_page, key_name, 'text/html')
    print 'Uploaded', key_name


if __name__ == '__main__':
    main()
