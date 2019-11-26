# import random
# import string
#
# def randomString(stringLength=64):
#     letters = string.ascii_lowercase
#     return ''.join(random.choice(letters) for i in range(stringLength))
#
#
# print ("Random String is ", randomString() )

#
# import datetime
#
# x = datetime.datetime(2018, 6, 1)
#
# # print(x)
#
#
# import time
# import datetime
# # d = datetime.date(2015,21,5)
# #
# # print(time.mktime(d.timetuple())
# #       )
# from datetime import datetime, timedelta
# curr = datetime.now()
# fut = datetime.now() + timedelta(days = 30)
# import datetime
# d = datetime.datetime(fut.year, fut.month, fut.day)
# epoch = time.mktime(d.timetuple())
# current = int(epoch)
# print(current)
# print(curr)

string = "id,name,bio,business,category,fan_count,featured_video,artists_we_like,connected_instagram_account,cover,country_page_likes,engagement,impressum,influences,new_like_count,overall_star_rating,price_range,rating_count,talking_about_count,unread_message_count,unread_notif_count,unseen_message_count,verification_status,website,were_here_count,ratings.limit(100){rating},likes"
# new = string.split(',')
# for x in new:
#     print(x)
