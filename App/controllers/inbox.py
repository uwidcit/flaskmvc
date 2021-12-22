from App.models import (Inbox, db)

# Get user feed
def get_inbox_feed_by_id(postId):
    print(f"Getting Feeds: {postId}")
    IFeed = Inbox.query.filter_by(postId=postId).first()
    return IFeed