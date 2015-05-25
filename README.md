## Feed Generator

### Getting credentials

You need AWS credentials. Get those. 
You need a Facebook token. Be part of the `salon-photostream` app (ask Kurt Spindler), and 
visit `https://developers.facebook.com/tools/explorer`. Choose the `salon-photostream` application,
and fill in the following URL:

    oauth/access_token?redirect_uri=http://www.onesalon.org&client_id=<client_id>&client_secret=<client_secret>&grant_type=fb_exchange_token&fb_exchange_token=<exchange_token>

`client_id` and `client_secret` are both from the `config.yaml` file. The `exchange_token` is the access_token in the field above the URL field.

### Running the Feed Generator

Create `generate_feed.sh` based on `generate_feed.sh.example` using the credentials from the previous step. Then run:

    bash generate_feed.sh

# Deployment

This is currently just a cronjob. Install the dependencies (`pip install -r requirements.txt`). Edit crontab (`crontab -e`) and add the line:

    0 0 * * * cd onesalon.org && bash generate_feed.sh

