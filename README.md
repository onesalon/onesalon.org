# Running Feed Generation

You must have fb & aws credentials. Create a `generate_feed.sh` file based on `generate_feed.sh.example`, and run:

    generate_feed.sh

# Deployment

This is currently just run as a cronjob, run once a day.

    crontab -e

Edit crontab to have the line

    0 0 * * * cd onesalon.org && bash generate_feed.sh

