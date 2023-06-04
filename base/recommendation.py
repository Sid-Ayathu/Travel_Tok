from .models import DESTINATIONS

# def find_similar_destination(liked_destination):
#     # Retrieve the details of the liked destination
#     liked = None
#     try:
#         liked = DESTINATIONS.objects.filter(DEST=liked_destination).values_list('BEACHES', 'HISTORICAL', 'WILDLIFE', 'HILLSTATIONS', 'MODERN_INFRASTRUCTURE', 'REC').first()
#     except DESTINATIONS.DoesNotExist:
#         print(f"No data found for '{liked_destination}'")

#     if liked is not None:
#         # Find the destination with the minimum distance from the liked destination
#         mini = None
#         place = DESTINATIONS()
#         for dest in DESTINATIONS.objects.exclude(DEST=liked_destination):
#             x = (dest.BEACHES, dest.HISTORICAL, dest.WILDLIFE, dest.HILLSTATIONS, dest.MODERN_INFRASTRUCTURE, dest.REC)
#             A = sum([abs(x[i]-liked[i]) for i in range(6)])
#             if mini == None or A < mini:
#                 mini = A
#                 place = dest
#         place.REC=1
#         return place


def go_next(r):
    r.REC=2
    return recommend_without_pref()

def recommend_without_pref():
    r=DESTINATIONS.objects.all()
    L=[]
    for place in r:
        if place.REC!=1 and place.REC!=2:
            L.append(place)
    L.sort(key=lambda x:x.RATING)
    return L[0]



def recommend_more_liked_stuff(liked_destination):
    places = DESTINATIONS.objects.filter(DEST=liked_destination)
    places.REC=1
    d = {}
    for r in places:
        lis=[r.BEACHES,r.HISTORICAL,r.WILDLIFE,r.HILLSTATIONS,r.MODERN_INFRASTRUCTURE,r.FOREST,r.SNOW,r.RATING]
        for i in range(7):
            if lis[i] == 1:
                d[i+2] = 1

    places = DESTINATIONS.objects.exclude(DEST=liked_destination)
    max_count = 0
    place_with_max_count = None

    for r in places:
        lis=[r.BEACHES,r.HISTORICAL,r.WILDLIFE,r.HILLSTATIONS,r.MODERN_INFRASTRUCTURE,r.FOREST,r.SNOW,r.RATING]
        count = 0
        for i in range(7):
            if lis[i] == 1 and ((i+2) in d):
                count += 1
        if DESTINATIONS.REC == 1 or DESTINATIONS.REC == 2:
            pass
        elif (place_with_max_count is None) or (count >= max_count):
            if count == max_count:
                if place_with_max_count is None:
                    place_with_max_count = r
                elif place_with_max_count.RATING > r.RATING:
                    place_with_max_count = r
            else:
                max_count = count
                place_with_max_count = r
    return place_with_max_count

