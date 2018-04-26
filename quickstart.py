import os
import time
from tempfile import gettempdir

from selenium.common.exceptions import NoSuchElementException

from instapy import InstaPy
from instapy.util import format_number, update_activity
from instapy.accounts import WINERYWORLD_USERNAME, WINERYWORLD_PW

insta_username = WINERYWORLD_USERNAME
insta_password = WINERYWORLD_PW

# set headless_browser=True if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'


def follow_like(session):
    hashtags = ['wine', 'winery', 'wineries', 'winelover', 'winemaker', 'winetime', 'wines', 'winenight', 'winetasting', 'wineporn', 'winestagram', 'winelife', 'winegeek', 'winetour', 'winewinewine', 'wineclub', 'winemaking', 'vineyard', 'winebar', 'winedown']
    session.like_by_tags(hashtags, amount=1)


def unfollow(session):
    session.unfollow_users(amount=10, unfollow_after=72*60*60)


def get_own_following_count(session):
    session.browser.get('https://www.instagram.com/' + session.username.strip())
    # update server calls
    update_activity()

    try:
        allfollowing = format_number(
            session.browser.find_element_by_xpath("//li[3]/a/span").text)
        return allfollowing
    except NoSuchElementException:
        logger.warning('There are 0 people to follow')
        return 0


def run():
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True,
                      multi_logs=True)

    # settings
    session.set_relationship_bounds(enabled=True,
                 potency_ratio=None,
                  delimit_by_numbers=True,
                   max_followers=9999,
                    max_following=1000,
                     min_followers=0,
                      min_following=0)
    session.set_dont_like(['pizza', 'girl'])
    session.set_do_follow(enabled=True, percentage=50, times=1)
    #session.set_dont_unfollow_active_users(enabled=True, posts=5)


    try:
        session.login()
        while True:
            following_count = get_own_following_count(session)
            print "Currently following " + str(following_count) + " users"
            if following_count < 1200:
                print "Starting follow/like cycle"
                follow_like(session)
            else:
                print "Starting unfollow cycle"
                unfollow(session)
    except Exception as exc:
        # if changes to IG layout, upload the file to help us locate the change
        if isinstance(exc, NoSuchElementException):
            file_path = os.path.join(gettempdir(), '{}.html'.format(time.strftime('%Y%m%d-%H%M%S')))
            with open(file_path, 'wb') as fp:
                fp.write(session.browser.page_source.encode('utf8'))
            print('{0}\nIf raising an issue, please also upload the file located at:\n{1}\n{0}'.format(
                '*' * 70, file_path))
        # full stacktrace when raising Github issue
        raise
    finally:
        session.end()


if __name__ == "__main__":
    run()
