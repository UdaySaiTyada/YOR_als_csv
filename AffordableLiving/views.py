from django.shortcuts import render
from django.http import HttpResponse
# from django_pandas.io import read_frame
from sqlalchemy.ext.indexable import index_property

from AffordableLiving.models import Properties
# from django_pandas.io import read_frame
from django.template import loader
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from geopy.geocoders import Nominatim
import logging
from math import sin, cos, sqrt, atan2, radians
import sklearn.metrics
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import datetime
import random
import math
import sshtunnel
# import mysql.connector
#

def affordableLiving(request):
    htmlCode = "<html><h1>Affordable Living :</h1><p>This website is hosted to provide Micro Services to the Data Science Services for <a href = \"https://yourownroom.com/\">YourOwnRoom</a>, a house rental system for millinials.</p></html>"
    return HttpResponse(htmlCode)

# engine = engine = create_engine('mysql://yor_api:dev5440$@128.199.206.71:3306/yor_api')
engine = create_engine('mysql://root:1234@localhost:3306/uday')

def getVacancyAge(properties,rooms,qdata):
    print("Inside getVacancyAge()...")
    propertyIds = properties.index

    # yor_api Development server
    logsQuery = "select * from propertyusers p where p.property_id in " + qdata + " and p.pendingdeposite = 0"

    # Uday Local
    # logsQuery = "select * from propusers p where p.property_id in " + qdata + " and p.pendingdeposite = 0"

    ##################################### SQL Method ###################################
    # propertyUsers = pd.read_sql_query(logsQuery, engine, index_col='id')


    ##################################### CSV Method ####################################
    propertyUsers = pd.read_csv('propertiesUsers.csv', index_col = 'id')
    propUsercondition = propertyUsers.property_id.isin(propertyIds)
    propertyUsers = propertyUsers[propUsercondition]
    propUsercondition = propertyUsers['pendingdeposite'] == 0
    propertyUsers = propertyUsers[propUsercondition]


    propertyVacancyAge = pd.DataFrame([], index=propertyIds, columns=['vacancyAge'])
    todayDate = datetime.date.today()

    for propertyId in propertyIds:
        # print("property Id: ", propertyId)
        vacancyAge = []
        condition = propertyUsers['property_id'] == propertyId
        individualProperty = propertyUsers[condition]
        # print(propertyId)
        # print("--------------------------------")
        # print(individualProperty)

        # If the Individual property has no past tenants ---------------------------- Test case 1
        # print("Shape of this property: ",individualProperty.shape)
        if (individualProperty.shape[0] == 0):
            #         print(propertyId)
            fromDate = datetime.datetime.strptime((properties.at[propertyId, 'availfrom']), '%Y-%m-%d').date()
            propertyVacancyAge.at[propertyId, 'vacancyAge'] = (todayDate - fromDate).days
            # print(propertyVacancyAge.at[propertyId, 'vacancyAge'])
            continue

        roomIds = list(dict.fromkeys(individualProperty.room_id.tolist()))
        # print(roomIds)
        # print("roomIds:",roomIds)
        finalCase = 0
        if (0 in roomIds):
            roomIds.remove(0)

        # If the property is only listed for whole property --------------------------- Test case 3
        # exit_dates = []
        if (len(roomIds) == 0):
            finalCase = 1
            exit_dates_str = list(dict.fromkeys(individualProperty.exit_date.tolist()))
            exit_dates = []
            for exit_date in exit_dates_str:
                if(exit_date != ''):
                    if(type(exit_date) == float):
                        fromDate = todayDate
                    else:
                        fromDate = datetime.datetime.strptime(exit_date, '%Y-%m-%d').date()
                    exit_dates.append((todayDate - fromDate).days)

            if(len(exit_dates) != 0):
                vacancy_age = min(exit_dates)
            else:
                vacancy_age = 0

            propertyVacancyAge.at[propertyId, 'vacancyAge'] = vacancy_age
            # print(propertyVacancyAge.at[propertyId, 'vacancyAge'])
            continue

        for roomId in roomIds:
            # print("roomId:",roomId)
            # If there ard no available beds in a room ----------------------------- Test case 2
            # print('\t room Id: ', roomId)
            # condition = rooms.index == roomId
            # particularRoom = rooms[condition]
            # print()
            if (roomId not in rooms.index):
                # print("room not present in Rooms table")
                continue
            particularRoom = rooms.loc[roomId]
            # print(particularRoom)
            if (particularRoom.shape[0] != 0):
                if (rooms.at[roomId, 'availablebed'] == 0):
                    vacancyAge.append(0)
                else:
                    # print("roomId : ",roomId)
                    # print("Failing Case !")
                    total_beds = int(rooms.at[roomId, 'totalbed'])
                    # print("Total_beds: ",total_beds)
                    # condition = (propertyUsers['room_id'] == roomId)
                    roomDetails = propertyUsers[propertyUsers['room_id'] == roomId]
                    exitDates = list(roomDetails.exit_date)
                    # print(exitDates)

                    count = 0
                    exitDays = []
                    for x in exitDates:
                        # print(x)
                        if(type(x) == float):
                            count += 1
                            exitDays.append(0)
                            continue

                        else:
                            fromDate = datetime.datetime.strptime(x, '%Y-%m-%d').date()
                            exitDays.append((todayDate - fromDate).days)
                    # print("count is :",count)
                    # print(exitDays)
                    # if(len(exitDays) != 0):
                    vacancyAge.append(sum(exitDays) / len(exitDays))


        # print(propertyId)
        # print(vacancyAge)
        if((len(vacancyAge) == 0) and (finalCase == 1)):
            print("Dealing Final case")
            # exit_date_str = propertyUsers.at[-1,'exit_date']

        # print()
        if (len(vacancyAge) != 0):
            propertyVacancyAge.at[propertyId, 'vacancyAge'] = sum(vacancyAge) / len(vacancyAge)

    # print(propertyVacancyAge.head(propertyVacancyAge.shape[0]))
    # for i in propertyVacancyAge.index:
    #     print(propertyVacancyAge.at[i, 'vacancyAge'])
    return propertyVacancyAge

# Create your views here.

def getImages(propertyIds, qdata):
    print("Inside getImages():")

    # yor_api development sever
    query = "select * from images i where i.primaryid in " + qdata + " and i.size = 'med' and i.objecttype = 'property'"

    #  Uday Local
    # query = "select * from image i where i.primaryid in " + qdata + " and i.size = 'med' and i.objecttype = 'property'"

    ################################### SQL Method #######################################
    # images = pd.read_sql_query(query, engine, index_col='imid')

    ################################### CSV Method #######################################
    images = pd.read_csv('images.csv', index_col = 'id')
    imagesCondition = images.primaryid.isin(propertyIds)
    images = images[imagesCondition]
    imagesCondition = images['size'] == 'med'
    images = images[imagesCondition]
    imagesCondition = images['objecttype'] == 'property'
    images = images[imagesCondition]


    dataFrame = pd.DataFrame([], index=propertyIds, columns=['image'])
    for i in propertyIds:
        condition = images['primaryid'] == i
        SpecificImages = images[condition]
        JsonResponseSTR = SpecificImages.to_json(orient='records')
        JsonRes = json.loads(JsonResponseSTR)
        dataFrame.at[i, 'image'] = JsonRes
    return dataFrame


def getRoomDetails(rooms,propertyIds):
    print("Inside getRoomDetails():\ngetting Room Details .... ")
    room = pd.DataFrame([], columns=['rooms'], index=propertyIds)
    for i in propertyIds:
        condition = rooms['property_id'] == i
        SpecificRoom = rooms[condition]
        #     print(gapminder_2002)
        JsonResponseSTR = SpecificRoom.to_json(orient='records')
        JsonRes = json.loads(JsonResponseSTR)
        room.at[i, 'rooms'] = JsonRes
    return room

@csrf_exempt
def module3(request):
    print("\n-------------- Start ----------------\n")
    # engine = create_engine('mysql://root:1234@localhost:3306/uday')
    # Getting Input Data
    print("Getting input from HttpRequest : \n")
    print(request.body)

    ################################## Post Body Input ###############################################

    received_json_data = json.loads(request.body)
    locality = received_json_data['addressl1']
    city = received_json_data['city']
    gender = str(received_json_data['gender'])
    propertyType = str(received_json_data['sharetype'])
    minBudget = int(received_json_data['minBudget'])
    maxBudget = int(received_json_data['maxBudget'])
    bhkcount = int(received_json_data['bhkCount'])

    # Getting the User's location's data
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    location = geolocator.geocode(locality + ", " + city)

    print("\nLocation's latitude: ", str(location.latitude), " Longitude: ", str(location.longitude))

    # Getting the data From the Database
    if (propertyType == '4'):
        #     query = " * from properties p where (p.status = \'available\') and (p.city = \'"+city+"\') and (p.locality = \'" + locality + "\') "
        query = "select * from properties p where p.city = 'bengaluru' and p.status = 'available'"
    elif (gender != '0'):
        query = "select * from properties p where (p.status = 'partial' or p.status = 'available') and p.city = \'" + city + "\' and p.gender = " + gender
    else:
        query = "select * from properties p where (p.status = 'partial' or p.status = 'available') and p.city = \'" + city + "\'"
    if (bhkcount != -1):
        bhkQuery = "and p.totalrooms in (" + str(bhkcount) + ", " + str(bhkcount + 1) + ")"
        query += bhkQuery
    print("\nProperties Query\n----------------\n" + query + "\n")
    # engine = create_engine('mysql://root:1234@localhost:3306/uday')
    properties = pd.read_sql_query(query, engine, index_col='id')

    # Calculating the distances with other areas
    location = geolocator.geocode(locality + ", " + city)
    R = 6373.0
    lat1 = radians(location.latitude)
    lon1 = radians(location.longitude)
    distance = pd.DataFrame(data=np.zeros(properties.shape[0], dtype=float), index=properties.index,
                            columns=['distance'])

    for i in properties.index:
        lat2 = radians(properties.at[i, 'latitude'])
        lon2 = radians(properties.at[i, 'longitude'])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = R * c
        distance.at[i, 'distance'] = d
    # print(distance)

    distanceClassify = pd.DataFrame(data=np.zeros((properties.shape[0], 3), dtype=int), index=properties.index,
                                    columns=['distanceLessThan2KM', 'distanceLessThan5KM', 'distanceLessThan10KM'])
    for i in properties.index:
        if (distance.at[i, 'distance'] <= 2.0):
            distanceClassify.at[i, 'distanceLessThan2KM'] = 20
        elif (distance.at[i, 'distance'] <= 5.0):
            distanceClassify.at[i, 'distanceLessThan5KM'] = 15
        else:
            distanceClassify.at[i, 'distanceLessThan10KM'] = 8
    # print(distanceClassify)

    #
    parking = pd.DataFrame(data=np.zeros(properties.shape[0], dtype=int), columns=['parking'], index=properties.index)
    for i in properties.index:
        parking.at[i, 'parking'] = 0 if (properties.at[i, 'parkingcharges'] == 0) else 1

    #
    minimum_property_rent = min(properties.rent)
    maximum_property_rent = max(properties.rent)

    theMinBudget = minimum_property_rent if minimum_property_rent < minBudget else minBudget
    theMaxBudget = maximum_property_rent if maximum_property_rent > maxBudget else maxBudget
    print("\nThe minimum & maximum budgets for Recommendation System are ", theMinBudget, "and", theMaxBudget,
          "respectively.\n")
    minNum = (theMinBudget // 5000) * 5000
    maxNum = (theMaxBudget // 5000) * 5000

    budgetList = []
    for i in range(minNum, maxNum + 1, 5000):
        budgetName = "rent-" + str(i) + "-" + str(i + 5000)
        budgetList.append(budgetName)

    #
    areaTypes = ['areaLessThan1000', 'areaLessThan1700', 'areaGreaterThan1700']
    area = pd.DataFrame(data=np.zeros((properties.shape[0], 3), dtype=int), index=properties.index, columns=areaTypes)
    for i in properties.index:
        if (properties.at[i, 'sqftsuper'] < 1000):
            area.at[i, 'areaLessThan1000'] = 5
        elif (properties.at[i, 'sqftsuper'] < 1700):
            area.at[i, 'areaLessThan1700'] = 6
        else:
            area.at[i, 'areaGreaterThan1700'] = 7

    bussinessTypes = ['managed', 'marketplace']
    businessType = pd.DataFrame(np.zeros((properties.shape[0], 2), dtype=int), columns=bussinessTypes,
                                index=properties.index)
    for i in properties.index:
        if (properties.at[i, 'tag_as'] == 'managed'):
            businessType.at[i, 'managed'] = 7
        else:
            businessType.at[i, 'marketplace'] = 5

    golden = pd.DataFrame(data=np.zeros((properties.shape[0]), dtype=int), index=properties.index, columns=['isGolden'])

    for i in properties.index:
        if (properties.at[i, 'golden'] == 1):
            golden.at[i, 'isGolden'] = 10

    propertyIds = properties.index
    qdata = '('
    for i in propertyIds:
        if (i != propertyIds[0]):
            qdata += ', '
        qdata += str(i)
    qdata += ')'
    roomsQuery = "select * from roomz r where r.property_id in " + qdata
    print("Rooms Query\n-----------\n" + roomsQuery + "\n")
    roomsDF = pd.read_sql_query(roomsQuery, engine, index_col='id')

    vacancyAge = getVacancyAge(properties, roomsDF, qdata)

    for va in vacancyAge.index:
        if (math.isnan(vacancyAge.at[va, 'vacancyAge'])):
            vacancyAge.at[va, 'vacancyAge'] = 0

    vacancyAgeDF = pd.DataFrame(np.zeros((properties.shape[0], 3), dtype=float),
                                columns=['vacancyAgeLessThan50', 'vacancyAgeLessThan120', 'vacancyAgeGreaterThan120'],
                                index=properties.index)

    for propertyId in vacancyAge.index:
        if (vacancyAge.at[propertyId, 'vacancyAge'] < 50):
            vacancyAgeDF.at[propertyId, 'vacancyAgeLessThan50'] = 7
        elif (vacancyAge.at[propertyId, 'vacancyAge'] < 120):
            vacancyAgeDF.at[propertyId, 'vacancyAgeLessThan50'] = 8
        else:
            vacancyAgeDF.at[propertyId, 'vacancyAgeGreaterThan120'] = 10

    # print(vacancyAge)
    # Unified Vectors
    propertiesColumns = budgetList

    print("\nCreating Properties Unified Vector and assigning wieghts to them......\n")

    propertyUnifiedVector = pd.DataFrame(np.zeros((properties.shape[0], len(propertiesColumns)), dtype=float),
                                         columns=propertiesColumns, index=properties.index)
    propertyUnifiedVector = pd.concat(
        [propertyUnifiedVector, distanceClassify, businessType, area, golden, vacancyAgeDF], axis=1)
    if(propertyType == '4'):
        for i in properties.index:
            rent = properties.at[i, 'rent']
            rent = (rent // 5000) * 5000
            budgetName = "rent-" + str(rent) + "-" + str(rent + 5000)
            propertyUnifiedVector.at[i, budgetName] = 8
    else:
        for i in properties.index:
            specific_property_condition = roomsDF['property_id'] == i
            specific_property = roomsDF[specific_property_condition]
            for roomId in specific_property.index:
                rent = specific_property.at[roomId, 'rent']
                rent = (rent // 5000) * 5000
                budgetName = "rent-" + str(rent) + "-" + str(rent + 5000)
                propertyUnifiedVector.at[i, budgetName] = 8

    budgets = (np.zeros(len(budgetList))).tolist() + [20, 15, 8, 7, 5, 5, 6, 7, 10, 7, 8, 10]
    print("\nCreating User Unified Vector and assigning wieghts to them......\n")

    userUnifiedVector = pd.DataFrame([budgets], columns=propertyUnifiedVector.columns, index=[1])

    minBud = (minBudget // 5000) * 5000
    maxBud = (maxBudget // 5000) * 5000
    # print(minBud,maxBud)
    for i in range(minBud, maxBud + 1, 5000):
        colName = "rent-" + str(i) + "-" + str(i + 5000)
        userUnifiedVector.at[1, colName] = 8
    # print(userUnifiedVector.golden[0])
    # UserPropertyDistance = sklearn.metrics.pairwise.cosine_similarity(userUnifiedVector.values,
    #                                                                   propertyUnifiedVector.values)
    UserPropertyDistance = sklearn.metrics.pairwise.cosine_similarity(userUnifiedVector.values,
                                                                      propertyUnifiedVector.values)
    UserPropertyDistance = pd.DataFrame(UserPropertyDistance, columns=propertyUnifiedVector.index)

    #
    rank = pd.DataFrame(UserPropertyDistance.loc[0,].tolist(), columns=['score'], index=properties.index)
    propertyId = pd.DataFrame(properties.index, columns=['id'], index=properties.index)
    rooms = getRoomDetails(roomsDF, properties.index)
    properties.image = getImages(properties.index, qdata)
    properties = pd.concat([propertyId, properties, rooms, rank, distance], axis=1)

    print("\n Filtering Data as per some conditionxs to improve the user's experience")
    condition = properties['distance'] <= 10.0
    SpecificProperties = properties[condition]
    print("\nConverting the data into JSON Format")
    JsonResponseSTR = SpecificProperties.to_json(orient='records')
    # JsonResponseSTR = properties.to_json(orient='records')

    jsonResp = json.loads(JsonResponseSTR)
    # print(JsonResponse)';'
    print("\nSorting the data according to the scores....")
    jsonResp = sorted(jsonResp, key=lambda k: k['score'], reverse=True)
    # print("------------------------------------------------")
    result = []
    leng = len(jsonResp)
    if (leng > 6):
        leng = 6
    for i in range(leng):
        result.append(jsonResp[i])
        result[i]['rank'] = i + 1
    print("\n-------------- End ----------------")
    return JsonResponse({'response': result})


@csrf_exempt
def getRecommendedProperties(request):

    print("\n-------------- Start ----------------\n")
    # engine = create_engine('mysql://root:1234@localhost:3306/uday')
    # Getting Input Data
    print("Getting input from HttpRequest : \n")
    print(request.body)

    ################################## Post Body Input ###############################################

    received_json_data = json.loads(request.body)
    locality = received_json_data['addressl1']
    city = received_json_data['city']
    gender = int(received_json_data['gender'])
    propertyType = str(received_json_data['sharetype'])
    minBudget = int(received_json_data['minBudget'])
    maxBudget = int(received_json_data['maxBudget'])
    bhkcount = int(received_json_data['bhkCount'])

    # Getting the User's location's data
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    location = geolocator.geocode(locality + ", " + city)

    print("\nLocation's latitude: ", str(location.latitude) ," Longitude: ",str(location.longitude))

    # Getting the data From the Database
    # if (propertyType == '4'):
    #     #     query = " * from properties p where (p.status = \'available\') and (p.city = \'"+city+"\') and (p.locality = \'" + locality + "\') "
    #     query = "select * from properties p where p.city = 'bengaluru' and p.status = 'available'"
    # elif (gender != '0'):
    #     query = "select * from properties p where (p.status = 'partial' or p.status = 'available') and p.city = \'" + city + "\' and p.gender = " + gender
    # else:
    #     query = "select * from properties p where (p.status = 'partial' or p.status = 'available') and p.city = \'" + city + "\'"
    # if(bhkcount != -1):
    #     bhkQuery = "and p.totalrooms in (" + str(bhkcount) + ", " + str(bhkcount + 1) + ")"
    #     query += bhkQuery
    # print("\nProperties Query\n----------------\n"+query+"\n")
    # # engine = create_engine('mysql://root:1234@localhost:3306/uday')

    ########################################## SQL Version ####################################################
    # properties = pd.read_sql_query(query, engine, index_col='id')

    ########################################## CSV Version ####################################################
    properties = pd.read_csv('properties.csv', index_col= 'id')
    properties = properties[properties['city'] == city]
    statuses = ['available', 'partial']
    bhkList = []
    bhkList.append(bhkcount)
    bhkList.append(bhkcount + 1)

    if (propertyType == '4'):
        properties = properties[properties['status'] == 'available']
    else:
        properties = properties[properties.status.isin(statuses)]
        if (gender != '0'):
            properties = properties[properties['gender'] == gender]
    if(bhkcount != -1):
        propertiescondition = properties.totalrooms.isin(bhkList)
        properties = properties[propertiescondition]
    # print(properties)
    # Calculating the distances with other areas
    location = geolocator.geocode(locality + ", " + city)
    R = 6373.0
    lat1 = radians(location.latitude)
    lon1 = radians(location.longitude)
    distance = pd.DataFrame(data=np.zeros(properties.shape[0], dtype=float), index=properties.index,columns=['distance'])

    for i in properties.index:
        # print(i)
        lat2 = radians(float(properties.at[i, 'latitude']))
        lon2 = radians(float(properties.at[i, 'longitude']))
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = R * c
        distance.at[i, 'distance'] = d
    # print(distance)

    distanceClassify = pd.DataFrame(data=np.zeros((properties.shape[0], 3), dtype=int), index=properties.index,
                                    columns=['distanceLessThan2KM', 'distanceLessThan5KM', 'distanceLessThan10KM'])
    for i in properties.index:
        if (distance.at[i, 'distance'] <= 2.0):
            distanceClassify.at[i, 'distanceLessThan2KM'] = 20
        elif (distance.at[i, 'distance'] <= 5.0):
            distanceClassify.at[i, 'distanceLessThan5KM'] = 15
        else:
            distanceClassify.at[i, 'distanceLessThan10KM'] = 8
    # print(distanceClassify)

    #
    # parking = pd.DataFrame(data=np.zeros(properties.shape[0], dtype=int), columns=['parking'], index=properties.index)
    # for i in properties.index:
    #     parking.at[i, 'parking'] = 0 if (properties.at[i, 'parkingcharges'] == 0) else 1

    roomsDF = pd.read_csv('rooms.csv', index_col='id')
    # print(properties.index)
    # roomsCondition = roomsDF.property_id.isin(properties.index)
    roomsDF = roomsDF[roomsDF.property_id.isin(properties.index)]

    if(propertyType == '4'):
        minimum_property_rent = min(properties.rent)
        maximum_property_rent = max(properties.rent)
    else:
        minimum_property_rent = min(roomsDF.rent)
        maximum_property_rent = max(roomsDF.rent)

    theMinBudget = minimum_property_rent if minimum_property_rent < minBudget else minBudget
    theMaxBudget = maximum_property_rent if maximum_property_rent > maxBudget else maxBudget
    print("\nThe minimum & maximum budgets for Recommendation System are ",theMinBudget,"and", theMaxBudget,"respectively.\n")
    minNum = (theMinBudget // 5000) * 5000
    maxNum = (theMaxBudget // 5000) * 5000

    budgetList = []
    for i in range(minNum, maxNum + 1, 5000):
        budgetName = "rent-" + str(i) + "-" + str(i + 5000)
        budgetList.append(budgetName)

    #
    areaTypes = ['areaLessThan1000', 'areaLessThan1700', 'areaGreaterThan1700']
    area = pd.DataFrame(data=np.zeros((properties.shape[0], 3), dtype=int), index=properties.index, columns=areaTypes)
    for i in properties.index:
        if (properties.at[i, 'sqftsuper'] < 1000):
            area.at[i, 'areaLessThan1000'] = 5
        elif (properties.at[i, 'sqftsuper'] < 1700):
            area.at[i, 'areaLessThan1700'] = 6
        else:
            area.at[i, 'areaGreaterThan1700'] = 7

    bussinessTypes = ['managed', 'marketplace']
    businessType = pd.DataFrame(np.zeros((properties.shape[0], 2), dtype=int), columns=bussinessTypes,
                                index=properties.index)
    for i in properties.index:
        if (properties.at[i, 'tag_as'] == 'managed'):
            businessType.at[i, 'managed'] = 7
        else:
            businessType.at[i, 'marketplace'] = 5

    golden = pd.DataFrame(data=np.zeros((properties.shape[0]), dtype=int), index=properties.index,columns=['isGolden'])

    for i in properties.index:
        if (properties.at[i, 'golden'] == 1):
            golden.at[i, 'isGolden'] = 10

    propertyIds = properties.index.tolist()
    qdata = '('
    for i in propertyIds:
        if (i != propertyIds[0]):
            qdata += ', '
        qdata += str(i)
    qdata += ')'
    # print(type(propertyIds))
    # yor_api development database
    roomsQuery = "select * from rooms r where r.property_id in " + qdata

    # Uday local Database
    # roomsQuery = "select * from roomz r where r.property_id in " + qdata

    print("Rooms Query\n-----------\n" + roomsQuery+"\n")
    roomsDF = pd.read_csv('rooms.csv', index_col= 'id')
    # print(propertyIds)
    roomsCondition = roomsDF.property_id.isin(propertyIds)
    roomsDF = roomsDF[roomsCondition]
    # roomsDF = roomsDF[roomsDF['property_id'] in propertyIds]
    #roomsDF = pd.read_sql_query(roomsQuery, engine, index_col='id')

    vacancyAge = getVacancyAge(properties, roomsDF, qdata)

    for va in vacancyAge.index:
        if(math.isnan(vacancyAge.at[va,'vacancyAge'])):
            vacancyAge.at[va,'vacancyAge'] = 0

    vacancyAgeDF = pd.DataFrame(np.zeros((properties.shape[0],3),dtype = float),columns = ['vacancyAgeLessThan50','vacancyAgeLessThan120','vacancyAgeGreaterThan120'], index = properties.index)

    for propertyId in vacancyAge.index:
        if(vacancyAge.at[propertyId, 'vacancyAge'] < 50):
            vacancyAgeDF.at[propertyId, 'vacancyAgeLessThan50'] = 4
        elif(vacancyAge.at[propertyId, 'vacancyAge'] < 120):
            vacancyAgeDF.at[propertyId, 'vacancyAgeLessThan120'] = 5
        else:
            vacancyAgeDF.at[propertyId, 'vacancyAgeGreaterThan120'] = 6

    # print(vacancyAge)
    # Unified Vectors
    propertiesColumns = budgetList

    print("\nCreating Properties Unified Vector and assigning wieghts to them......\n")

    propertyUnifiedVector = pd.DataFrame(np.zeros((properties.shape[0], len(propertiesColumns)), dtype=float),
                                         columns=propertiesColumns, index=properties.index)
    propertyUnifiedVector = pd.concat([propertyUnifiedVector, distanceClassify, businessType, area,golden,vacancyAgeDF], axis=1)

    # for i in properties.index:
    #     rent = properties.at[i, 'rent']
    #     rent = (rent // 5000) * 5000
    #     budgetName = "rent-" + str(rent) + "-" + str(rent + 5000)
    #     propertyUnifiedVector.at[i, budgetName] = 8
    if (propertyType == '4'):
        for i in properties.index:
            rent = properties.at[i, 'rent']
            rent = (rent // 5000) * 5000
            budgetName = "rent-" + str(rent) + "-" + str(rent + 5000)
            propertyUnifiedVector.at[i, budgetName] = 8
    else:
        for i in properties.index:
            specific_property_condition = roomsDF['property_id'] == i
            specific_property = roomsDF[specific_property_condition]
            for roomId in specific_property.index:
                rent = specific_property.at[roomId, 'rent']
                rent = (rent // 5000) * 5000
                budgetName = "rent-" + str(rent) + "-" + str(rent + 5000)
                propertyUnifiedVector.at[i, budgetName] = 8

    budgets = (np.zeros(len(budgetList))).tolist() + [20,15,8 , 7, 5, 5, 6, 7,10,4,5,6]


    print("\nCreating User Unified Vector and assigning wieghts to them......\n")
    # print(propertyUnifiedVector.columns)
    # print(budgets)
    userUnifiedVector = pd.DataFrame([budgets], columns=propertyUnifiedVector.columns, index=[1])

    minBud = (minBudget // 5000) * 5000
    maxBud = (maxBudget // 5000) * 5000
    # print(minBud,maxBud)
    for i in range(minBud, maxBud + 1, 5000):
        colName = "rent-" + str(i) + "-" + str(i + 5000)
        userUnifiedVector.at[1, colName] = 8
    # print(userUnifiedVector.golden[0])
    # UserPropertyDistance = sklearn.metrics.pairwise.cosine_similarity(userUnifiedVector.values,
    #                                                                   propertyUnifiedVector.values)
    UserPropertyDistance = sklearn.metrics.pairwise.cosine_similarity(userUnifiedVector.values,propertyUnifiedVector.values)
    UserPropertyDistance = pd.DataFrame(UserPropertyDistance, columns=propertyUnifiedVector.index)

    #
    rank = pd.DataFrame(UserPropertyDistance.loc[0,].tolist(), columns=['score'], index=properties.index)
    propertyId = pd.DataFrame(properties.index, columns=['id'], index=properties.index)
    rooms = getRoomDetails(roomsDF, properties.index)
    properties.image = getImages(properties.index,qdata)
    properties = pd.concat([propertyId, properties,rooms, rank, distance,vacancyAge], axis=1)

    print("\n Filtering Data as per some conditionxs to improve the user's experience")
    condition = properties['distance'] <= 10.0
    SpecificProperties = properties[condition]
    print("\nConverting the data into JSON Format")
    JsonResponseSTR = SpecificProperties.to_json(orient='records')
    # JsonResponseSTR = properties.to_json(orient='records')

    jsonResp = json.loads(JsonResponseSTR)
    # print(JsonResponse)';'
    print("\nSorting the data according to the scores....")
    jsonResp = sorted(jsonResp, key=lambda k: k['score'], reverse=True)
    # print("------------------------------------------------")
    result = []
    leng = len(jsonResp)
    if (leng > 6):
        leng = 6
    for i in range(leng):
        result.append(jsonResp[i])
        result[i]['rank'] = i + 1
    print("\n-------------- End ----------------")
    return JsonResponse({'response': result})

@csrf_exempt
def module2(request):
    print("-------------- Start ----------------\n")
    # cursor = ""
    # # with sshtunnel.SSHTunnelForwarder(('devfront.yourownroom.com', 22), ssh_password='y0r##rty', ssh_username='yor',remote_bind_address=('localhost', 3306)) as server:
    # #     try:
    # #         print("Inside with loop")
    # #         conn = mc.connect(host='localhost', port=server.local_bind_port, user='yor_api',passwd='dev5440$')
    # #         cursor = conn.cursor()
    # #         print(type(cursor))
    # #         print("Ending of with loop")
    # #
    # #     except:
    # #         print("Blah")
    # # print("\n--------------- End ---------------")
    # # return HttpResponse(5)
    # server = sshtunnel.SSHTunnelForwarder(('devfront.yourownroom.com', 22), ssh_password='y0r##rty', ssh_username='yor',remote_bind_address=('127.0.0.1', 3306)).start()
    # print("Inside with loop")
    # conn = mysql.connector.connect(host='128.199.206.71', port= 3306, user='yor_api',passwd='dev5440$')
    # cursor = conn.cursor()
    # print("Ending of with loop")
    #
    #
    # # engine1 = create_engine('mysql://yor_api:dev5440$@localhost:3306/yor_api')
    # #
    # # # engine1 = create_engine('mysql://yor_api:dev5440$@128.199.206.71:3306/yor_api')
    # # query = "select * from properties"
    # # properties = pd.read_sql_query(query, engine1, index_col='id')
    # #
    # # id = [157]
    # # print(properties.shape[0])
    # # id = [157]
    # # print(getVacancyAge(id))
    print("\n--------------- End ---------------")
    return HttpResponse(5)


@csrf_exempt
def report(request):

    print("_________________________________________ Start ____________________________________________")


    popular_properties = pd.read_csv('popularSiteVisits.csv', index_col = 'id')
    properties = pd.read_csv('properties.csv', index_col = 'id')
    siteVisits = pd.read_csv('siteVisits.csv', index_col = 'id')
    tempVisists = pd.DataFrame([],columns = ['Name','locality','city','golden','rent','status', 'tag_as','siteVisitCount'], index = popular_properties.index)
    print(popular_properties.index)
    results = [int(i) for i in popular_properties.index]
    for property_id in results:
        if(property_id in properties.index):
            tempVisists.at[property_id, 'Name'] = properties.at[property_id, 'name']
            tempVisists.at[property_id, 'locality'] = properties.at[property_id, 'locality']
            tempVisists.at[property_id, 'city'] = properties.at[property_id, 'city']
            tempVisists.at[property_id, 'golden'] = properties.at[property_id, 'golden']
            tempVisists.at[property_id, 'rent'] = properties.at[property_id, 'rent']
            tempVisists.at[property_id, 'status'] = properties.at[property_id, 'status']
            tempVisists.at[property_id, 'tag_as'] = properties.at[property_id, 'tag_as']
        if(property_id in siteVisits.index):
            tempVisists.at[property_id, 'siteVisitCount'] = siteVisits.at[property_id, 'count']
        else:
            tempVisists.at[property_id, 'siteVisitCount'] = 0
    popular_properties = pd.concat([popular_properties, tempVisists], axis = 1)


    print(popular_properties)
    popular_properties.to_csv('Popular_Properties_Report.csv')
    print("_________________________________________ End ____________________________________________")
    return HttpResponse(5)



