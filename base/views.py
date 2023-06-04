from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .models import User,DESTINATIONS
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
import json
from .recommendation import recommend_more_liked_stuff,go_next,recommend_without_pref

# Goa=DESTINATIONS()
# Goa.DEST='Goa'
# Goa.BEACHES=1
# Goa.HISTORICAL=1
# Goa.WILDLIFE=1
# Goa.HILLSTATIONS=0
# Goa.MODERN_INFRASTRUCTURE=1
# Goa.FOREST=1
# Goa.SNOW=0
# Goa.RATING=15
# Goa.REC=0
# Goa.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FGoa&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Goa.save()

# Chennai=DESTINATIONS()
# Chennai.DEST='Chennai'
# Chennai.BEACHES=1
# Chennai.HISTORICAL=1
# Chennai.WILDLIFE=0
# Chennai.HILLSTATIONS=0
# Chennai.MODERN_INFRASTRUCTURE=1
# Chennai.FOREST=0
# Chennai.SNOW=0
# Chennai.RATING=23
# Chennai.REC=0
# Chennai.IMAGES='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.shutterstock.com%2Fsearch%2Fchennai&psig=AOvVaw2EV02t45cOmjUzO3F70fXQ&ust=1679852115111000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCNi59PfO9_0CFQAAAAAdAAAAABAE'
# Chennai.save()

# Mahabalipuram=DESTINATIONS()
# Mahabalipuram.DEST='Mahabalipuram'
# Mahabalipuram.BEACHES=1
# Mahabalipuram.HISTORICAL=1
# Mahabalipuram.WILDLIFE=0
# Mahabalipuram.HILLSTATIONS=0
# Mahabalipuram.MODERN_INFRASTRUCTURE=1
# Mahabalipuram.FOREST=0
# Mahabalipuram.SNOW=0
# Mahabalipuram.RATING=7
# Mahabalipuram.REC=0
# Mahabalipuram.IMAGES='https://www.tripsavvy.com/thmb/yZuvI0lUakLLJ4QxgbAwtglMEyg=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/GettyImages-579760012-b78004a355354623924eda63842ac3a9.jpg'
# Mahabalipuram.save()

# Adaman_and_Nicobar_Islands=DESTINATIONS()
# Adaman_and_Nicobar_Islands.DEST='Andaman and Nicobar Islands'
# Adaman_and_Nicobar_Islands.BEACHES=1
# Adaman_and_Nicobar_Islands.HISTORICAL=1
# Adaman_and_Nicobar_Islands.WILDLIFE=1
# Adaman_and_Nicobar_Islands.HILLSTATIONS=0
# Adaman_and_Nicobar_Islands.MODERN_INFRASTRUCTURE=1
# Adaman_and_Nicobar_Islands.FOREST=1
# Adaman_and_Nicobar_Islands.SNOW=0
# Adaman_and_Nicobar_Islands.RATING=8
# Adaman_and_Nicobar_Islands.REC=0
# Adaman_and_Nicobar_Islands.IMAGES='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.studyiq.com%2Farticles%2Fandaman-and-nicobar-islands%2F&psig=AOvVaw1qfYg2WSrr4S5kxoQGwbuu&ust=1679852426272000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCOiagIvQ9_0CFQAAAAAdAAAAABAE'
# Adaman_and_Nicobar_Islands.save()

# Ajanta_and_Elora_Caves=DESTINATIONS()
# Ajanta_and_Elora_Caves.DEST='Ajanta and Elora Caves'
# Ajanta_and_Elora_Caves.BEACHES=0
# Ajanta_and_Elora_Caves.HISTORICAL=1
# Ajanta_and_Elora_Caves.WILDLIFE=0
# Ajanta_and_Elora_Caves.HILLSTATIONS=0
# Ajanta_and_Elora_Caves.MODERN_INFRASTRUCTURE=0
# Ajanta_and_Elora_Caves.FOREST=0
# Ajanta_and_Elora_Caves.SNOW=0
# Ajanta_and_Elora_Caves.RATING=1
# Ajanta_and_Elora_Caves.REC=0
# Ajanta_and_Elora_Caves.IMAGES='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.onacheaptrip.com%2Fajanta-and-ellora-caves%2F&psig=AOvVaw0nN-FnAnaO7ZIDeOOgPD5I&ust=1679852468655000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCOCo0KLQ9_0CFQAAAAAdAAAAABAI'
# Ajanta_and_Elora_Caves.save()

# Rann_of_Kutch=DESTINATIONS()
# Rann_of_Kutch.DEST='Rann of Kutch'
# Rann_of_Kutch.BEACHES=0
# Rann_of_Kutch.HISTORICAL=0
# Rann_of_Kutch.WILDLIFE=1
# Rann_of_Kutch.HILLSTATIONS=0
# Rann_of_Kutch.MODERN_INFRASTRUCTURE=0
# Rann_of_Kutch.FOREST=0
# Rann_of_Kutch.SNOW=0
# Rann_of_Kutch.RATING=2
# Rann_of_Kutch.REC=0
# Rann_of_Kutch.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FGoa&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Rann_of_Kutch.save()

# Hampi=DESTINATIONS()
# Hampi.DEST='Hampi'
# Hampi.BEACHES=0
# Hampi.HISTORICAL=1
# Hampi.WILDLIFE=0
# Hampi.HILLSTATIONS=0
# Hampi.MODERN_INFRASTRUCTURE=0
# Hampi.FOREST=0
# Hampi.SNOW=0
# Hampi.RATING=6
# Hampi.REC=0
# Hampi.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FGoa&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Hampi.save()


# Leh=DESTINATIONS()
# Leh.DEST='Leh'
# Leh.BEACHES=0
# Leh.HISTORICAL=1
# Leh.WILDLIFE=1
# Leh.HILLSTATIONS=1
# Leh.MODERN_INFRASTRUCTURE=0
# Leh.FOREST=0
# Leh.SNOW=1
# Leh.RATING=5
# Leh.REC=0
# Leh.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FGoa&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Leh.save()

# Pondicherry=DESTINATIONS()
# Pondicherry.DEST='Pondicherry'
# Pondicherry.BEACHES=1
# Pondicherry.HISTORICAL=1
# Pondicherry.WILDLIFE=0
# Pondicherry.HILLSTATIONS=0
# Pondicherry.MODERN_INFRASTRUCTURE=1
# Pondicherry.FOREST=0
# Pondicherry.SNOW=0
# Pondicherry.RATING=14
# Pondicherry.REC=0
# Pondicherry.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FPondicherry&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Pondicherry.save()

# Nubra_Valley=DESTINATIONS()
# Nubra_Valley.DEST='Nubra Valley'
# Nubra_Valley.BEACHES=0
# Nubra_Valley.HISTORICAL=1
# Nubra_Valley.WILDLIFE=1
# Nubra_Valley.HILLSTATIONS=1
# Nubra_Valley.MODERN_INFRASTRUCTURE=1
# Nubra_Valley.FOREST=1
# Nubra_Valley.SNOW=1
# Nubra_Valley.RATING=13
# Nubra_Valley.REC=0
# Nubra_Valley.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FNubra Valley&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Nubra_Valley.save()


# Pahalgam=DESTINATIONS()
# Pahalgam.DEST='Pahalgam'
# Pahalgam.BEACHES=0
# Pahalgam.HISTORICAL=1
# Pahalgam.WILDLIFE=1
# Pahalgam.HILLSTATIONS=1
# Pahalgam.MODERN_INFRASTRUCTURE=0
# Pahalgam.FOREST=1
# Pahalgam.SNOW=1
# Pahalgam.RATING=4
# Pahalgam.REC=0
# Pahalgam.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FPahalgam&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Pahalgam.save()


# Dzukou_Valley=DESTINATIONS()
# Dzukou_Valley.DEST='Dzukou Valley'
# Dzukou_Valley.BEACHES=0
# Dzukou_Valley.HISTORICAL=0
# Dzukou_Valley.WILDLIFE=1
# Dzukou_Valley.HILLSTATIONS=1
# Dzukou_Valley.MODERN_INFRASTRUCTURE=0
# Dzukou_Valley.FOREST=1
# Dzukou_Valley.SNOW=1
# Dzukou_Valley.RATING=19
# Dzukou_Valley.REC=0
# Dzukou_Valley.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FDzukou Valley&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Dzukou_Valley.save()


# Silent_Valley=DESTINATIONS()
# Silent_Valley.DEST='Silent Valley'
# Silent_Valley.BEACHES=0
# Silent_Valley.HISTORICAL=0
# Silent_Valley.WILDLIFE=1
# Silent_Valley.HILLSTATIONS=0
# Silent_Valley.MODERN_INFRASTRUCTURE=1
# Silent_Valley.FOREST=1
# Silent_Valley.SNOW=0
# Silent_Valley.RATING=29
# Silent_Valley.REC=0
# Silent_Valley.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FSilent Valley&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Silent_Valley.save()

# Auli=DESTINATIONS()
# Auli.DEST='Auli'
# Auli.BEACHES=0
# Auli.HISTORICAL=0
# Auli.WILDLIFE=0
# Auli.HILLSTATIONS=1
# Auli.MODERN_INFRASTRUCTURE=1
# Auli.FOREST=1
# Auli.SNOW=1
# Auli.RATING=12
# Auli.REC=0
# Auli.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FAuli&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Auli.save()


# Valley_of_Flowers=DESTINATIONS()
# Valley_of_Flowers.DEST='Valley of Flowers'
# Valley_of_Flowers.BEACHES=0
# Valley_of_Flowers.HISTORICAL=0
# Valley_of_Flowers.WILDLIFE=1
# Valley_of_Flowers.HILLSTATIONS=1
# Valley_of_Flowers.MODERN_INFRASTRUCTURE=1
# Valley_of_Flowers.FOREST=1
# Valley_of_Flowers.SNOW=0
# Valley_of_Flowers.RATING=3
# Valley_of_Flowers.REC=0
# Valley_of_Flowers.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FValley of Flowers&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Valley_of_Flowers.save()

# Kovalam=DESTINATIONS()
# Kovalam.DEST='Kovalam'
# Kovalam.BEACHES=1
# Kovalam.HISTORICAL=0
# Kovalam.WILDLIFE=0
# Kovalam.HILLSTATIONS=0
# Kovalam.MODERN_INFRASTRUCTURE=1
# Kovalam.FOREST=0
# Kovalam.SNOW=0
# Kovalam.RATING=22
# Kovalam.REC=0
# Kovalam.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FKovalam&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Kovalam.save()


# Mawlynnong=DESTINATIONS()
# Mawlynnong.DEST='Mawlynnong'
# Mawlynnong.BEACHES=0
# Mawlynnong.HISTORICAL=0
# Mawlynnong.WILDLIFE=1
# Mawlynnong.HILLSTATIONS=1
# Mawlynnong.MODERN_INFRASTRUCTURE=0
# Mawlynnong.FOREST=1
# Mawlynnong.SNOW=0
# Mawlynnong.RATING=16
# Mawlynnong.REC=0
# Mawlynnong.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMawlynnong&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Mawlynnong.save()

# Cherrapunji=DESTINATIONS()
# Cherrapunji.DEST='Cherrapunji'
# Cherrapunji.BEACHES=0
# Cherrapunji.HISTORICAL=1
# Cherrapunji.WILDLIFE=1
# Cherrapunji.HILLSTATIONS=1
# Cherrapunji.MODERN_INFRASTRUCTURE=0
# Cherrapunji.FOREST=1
# Cherrapunji.SNOW=0
# Cherrapunji.RATING=11
# Cherrapunji.REC=0
# Cherrapunji.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FCherrapunji&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Cherrapunji.save()


# Munsiyari=DESTINATIONS()
# Munsiyari.DEST='Munsiyari'
# Munsiyari.BEACHES=0
# Munsiyari.HISTORICAL=1
# Munsiyari.WILDLIFE=1
# Munsiyari.HILLSTATIONS=1
# Munsiyari.MODERN_INFRASTRUCTURE=0
# Munsiyari.FOREST=1
# Munsiyari.SNOW=1
# Munsiyari.RATING=26
# Munsiyari.REC=0
# Munsiyari.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMunsiyari&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Munsiyari.save()

# Kufri=DESTINATIONS()
# Kufri.DEST='Kufri'
# Kufri.BEACHES=0
# Kufri.HISTORICAL=0
# Kufri.WILDLIFE=0
# Kufri.HILLSTATIONS=1
# Kufri.MODERN_INFRASTRUCTURE=0
# Kufri.FOREST=1
# Kufri.SNOW=1
# Kufri.RATING=28
# Kufri.REC=0
# Kufri.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FKufri&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Kufri.save()


# Gokarna=DESTINATIONS()
# Gokarna.DEST='Gokarna'
# Gokarna.BEACHES=1
# Gokarna.HISTORICAL=1
# Gokarna.WILDLIFE=0
# Gokarna.HILLSTATIONS=0
# Gokarna.MODERN_INFRASTRUCTURE=0
# Gokarna.FOREST=0
# Gokarna.SNOW=0
# Gokarna.RATING=21
# Gokarna.REC=0
# Gokarna.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FGokarna&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Gokarna.save()


# Jaipur=DESTINATIONS()
# Jaipur.DEST='Jaipur'
# Jaipur.BEACHES=1
# Jaipur.HISTORICAL=1
# Jaipur.WILDLIFE=0
# Jaipur.HILLSTATIONS=0
# Jaipur.MODERN_INFRASTRUCTURE=0
# Jaipur.FOREST=0
# Jaipur.SNOW=0
# Jaipur.RATING=21
# Jaipur.REC=0
# Jaipur.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FJaipur&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Jaipur.save()

# Mumbai=DESTINATIONS()
# Mumbai.DEST='Mumbai'
# Mumbai.BEACHES=1
# Mumbai.HISTORICAL=1
# Mumbai.WILDLIFE=0
# Mumbai.HILLSTATIONS=0
# Mumbai.MODERN_INFRASTRUCTURE=1
# Mumbai.FOREST=0
# Mumbai.SNOW=0
# Mumbai.RATING=18
# Mumbai.REC=0
# Mumbai.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMumbai&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Mumbai.save()

# Kolkata=DESTINATIONS()
# Kolkata.DEST='Kolkata'
# Kolkata.BEACHES=0
# Kolkata.HISTORICAL=1
# Kolkata.WILDLIFE=0
# Kolkata.HILLSTATIONS=0
# Kolkata.MODERN_INFRASTRUCTURE=1
# Kolkata.FOREST=0
# Kolkata.SNOW=0
# Kolkata.RATING=10
# Kolkata.REC=0
# Kolkata.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FKolkata&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Kolkata.save()

# Varkala=DESTINATIONS()
# Varkala.DEST='Varkala'
# Varkala.BEACHES=1
# Varkala.HISTORICAL=1
# Varkala.WILDLIFE=0
# Varkala.HILLSTATIONS=0
# Varkala.MODERN_INFRASTRUCTURE=1
# Varkala.FOREST=0
# Varkala.SNOW=0
# Varkala.RATING=24
# Varkala.REC=0
# Varkala.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FVarkala&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Varkala.save()


# Kanyakumari=DESTINATIONS()
# Kanyakumari.DEST='Kanyakumari'
# Kanyakumari.BEACHES=1
# Kanyakumari.HISTORICAL=1
# Kanyakumari.WILDLIFE=0
# Kanyakumari.HILLSTATIONS=0
# Kanyakumari.MODERN_INFRASTRUCTURE=1
# Kanyakumari.FOREST=0
# Kanyakumari.SNOW=0
# Kanyakumari.RATING=20
# Kanyakumari.REC=0
# Kanyakumari.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FKanyakumari&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Kanyakumari.save()


# Rameshwaram=DESTINATIONS()
# Rameshwaram.DEST='Rameshwaram'
# Rameshwaram.BEACHES=1
# Rameshwaram.HISTORICAL=1
# Rameshwaram.WILDLIFE=0
# Rameshwaram.HILLSTATIONS=0
# Rameshwaram.MODERN_INFRASTRUCTURE=1
# Rameshwaram.FOREST=0
# Rameshwaram.SNOW=0
# Rameshwaram.RATING=9
# Rameshwaram.REC=0
# Rameshwaram.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FRameshwaram&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Rameshwaram.save()


# Bengaluru=DESTINATIONS()
# Bengaluru.DEST='Bengaluru'
# Bengaluru.BEACHES=0
# Bengaluru.HISTORICAL=1
# Bengaluru.WILDLIFE=0
# Bengaluru.HILLSTATIONS=0
# Bengaluru.MODERN_INFRASTRUCTURE=1
# Bengaluru.FOREST=1
# Bengaluru.SNOW=0
# Bengaluru.RATING=21
# Bengaluru.REC=0
# Bengaluru.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FBengaluru&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Bengaluru.save()


# Ranthambore=DESTINATIONS()
# Ranthambore.DEST='Ranthambore'
# Ranthambore.BEACHES=1
# Ranthambore.HISTORICAL=1
# Ranthambore.WILDLIFE=0
# Ranthambore.HILLSTATIONS=0
# Ranthambore.MODERN_INFRASTRUCTURE=0
# Ranthambore.FOREST=0
# Ranthambore.SNOW=0
# Ranthambore.RATING=21
# Ranthambore.REC=0
# Ranthambore.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FRanthambore&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Ranthambore.save()

# Solang_Valley=DESTINATIONS()
# Solang_Valley.DEST='Solang_Valley'
# Solang_Valley.BEACHES=0
# Solang_Valley.HISTORICAL=0
# Solang_Valley.WILDLIFE=1
# Solang_Valley.HILLSTATIONS=1
# Solang_Valley.MODERN_INFRASTRUCTURE=0
# Solang_Valley.FOREST=1
# Solang_Valley.SNOW=1
# Solang_Valley.RATING=27
# Solang_Valley.REC=0
# Solang_Valley.IMAGES='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Ffc%2FBeachFun.jpg&tbnid=5YgCVkxa3lx02M&vet=12ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FSolang_Valley&docid=pg9w4vor_SjQ7M&w=4640&h=2610&itg=1&q=goa&ved=2ahUKEwiL38_D6fb9AhW1-XMBHSdhBuoQMygAegUIARDhAQ'
# Solang_Valley.save()

def home(request):
    global place
    if request.method=="POST":
        if 'yes' in request.POST:
            liked_destination = DESTINATIONS.objects.filter(DEST=place.DEST)[:1].get()
            liked_destination.REC=1
            liked_destination.save()
            place=recommend_more_liked_stuff(liked_destination.DEST)

        elif 'no' in request.POST:
            next_destination=DESTINATIONS.objects.filter(DEST=place)[:1].get()
            next_destination.REC=1
            next_destination.save()
            place=go_next(next_destination)

    else:
        place=DESTINATIONS.objects.filter(DEST='Leh')[:1].get()

    img_url=place.IMAGES
    name=place.DEST
    print(place.DEST,img_url)
    context={'img_url':img_url,'name':name}
    return render(request, 'mainpg.html',context)

def register(request):
    page='register'
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:     
        form = CustomUserCreationForm()
    return render(request, "base/signup.html", {"form": form})


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'base/login.html')
    # if request.method == 'POST':
    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         # log the user in and redirect to LOGIN_REDIRECT_URL
    #         user=form.get_User()
    #         login(request,user)
    #         return redirect('home')
    #     else:
    #         return HttpResponse('ERROR')
    # else:
    #     form = AuthenticationForm(request)
    # return render(request, 'base/login.html', {'form': form})

