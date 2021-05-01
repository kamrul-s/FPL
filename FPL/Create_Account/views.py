from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages

def details(request):
    if 'user' not in request.session:
        return render(request,'index.html')
    team_name = request.POST['tname']
    id = request.session['user']
    cursor = connection.cursor()
    args = [0]
    result_args = cursor.callproc('GET_USER_TEAM_ID',args)
    cursor.close()
    team_id = int(result_args[0])

    cursor = connection.cursor()
    query3 = "INSERT INTO USER_TEAM VALUES(%s,%s,%s)"
    cursor.execute(query3,[team_id,team_name,id])
    connection.commit()
    cursor.close()

    for club in request.POST.getlist('followed'):
        cursor = connection.cursor()
        query5 = "INSERT INTO TEAM_FOLLOWS VALUES(%s,%s)"
        cursor.execute(query5,[id,club])
        connection.commit()
        cursor.close()

    fav_club = request.POST['favourite']
    if fav_club != 'None':
        cursor = connection.cursor()
        query4 = "UPDATE USER_INFO SET FAV_TEAM_NAME = %s WHERE USER_ID = %s"
        cursor.execute(query4,[fav_club,id])
        connection.commit()
        cursor.close()


    cursor = connection.cursor()
    query = 'SELECT PLAYER_ID,LAST_NAME,PLAYING_POSITION,TEAM_NAME,PRICE FROM PLAYER_INFO ORDER BY PLAYER_ID'
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    players = []
    for r in result:
        Id = r[0]
        Name = r[1]
        Position = r[2]
        Team_name = r[3]
        Price = r[4]
        row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name,'Price':Price}
        players.append(row)
    return render(request,'squad_selection.html',{'Players':players})

def squad_selection(request):
    if 'user' not in request.session:
        return render(request,'index.html')
    id = request.session['user']
    cost = 0
    for player_id in request.POST.getlist('GKP'):
        cursor = connection.cursor()
        query = "SELECT PRICE FROM PLAYER_INFO WHERE PLAYER_ID = %s"
        cursor.execute(query,[player_id])
        result = cursor.fetchall()
        cursor.close()
        for r in result:
            pr = r[0]
            cost=cost+pr
    for player_id in request.POST.getlist('DEF'):
        cursor = connection.cursor()
        query = "SELECT PRICE FROM PLAYER_INFO WHERE PLAYER_ID = %s"
        cursor.execute(query,[player_id])
        result = cursor.fetchall()
        cursor.close()
        for r in result:
            pr = r[0]
            cost = cost+pr
    for player_id in request.POST.getlist('MID'):
        cursor = connection.cursor()
        query = "SELECT PRICE FROM PLAYER_INFO WHERE PLAYER_ID = %s"
        cursor.execute(query,[player_id])
        result = cursor.fetchall()
        cursor.close()
        for r in result:
            pr = r[0]
            cost=cost+pr
    for player_id in request.POST.getlist('FWD'):
        cursor = connection.cursor()
        query = "SELECT PRICE FROM PLAYER_INFO WHERE PLAYER_ID = %s"
        cursor.execute(query,[player_id])
        result = cursor.fetchall()
        cursor.close()
        for r in result:
            pr = r[0]
            cost=cost+pr
    if cost>100 :
        cursor = connection.cursor()
        query = 'SELECT PLAYER_ID,LAST_NAME,PLAYING_POSITION,TEAM_NAME,PRICE FROM PLAYER_INFO ORDER BY PLAYER_ID'
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        players = []
        for r in result:
            Id = r[0]
            Name = r[1]
            Position = r[2]
            Team_name = r[3]
            Price = r[4]
            row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name,'Price':Price}
            players.append(row)
        messages.warning(request, "Select within 100M")
        return render(request,'squad_selection.html',{'Players':players})
    players = []
    for player_id in request.POST.getlist('GKP'):
        cursor = connection.cursor()
        query = "SELECT PLAYER_ID,LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s"
        cursor.execute(query,[player_id])
        result = cursor.fetchall()
        cursor.close()
        for r in result:
            Id = r[0]
            Name = r[1]
            Position = r[2]
            Team_name = r[3]
            cursor = connection.cursor()
            query1 = "INSERT INTO USER_PLAYERS VALUES(%s,%s,%s)"
            cursor.execute(query1,[id,Id,Position])
            connection.commit()
            cursor.close()
            row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name}
            players.append(row)
    for player_id in request.POST.getlist('DEF'):
        cursor = connection.cursor()
        query2 = 'SELECT PLAYER_ID,LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s'
        cursor.execute(query2,[player_id])
        result = cursor.fetchall()
        cursor.close()
        for r in result:
            Id = r[0]
            Name = r[1]
            Position = r[2]
            Team_name = r[3]
            cursor = connection.cursor()
            query3 = "INSERT INTO USER_PLAYERS VALUES(%s,%s,%s)"
            cursor.execute(query3,[id,Id,Position])
            connection.commit()
            cursor.close()
            row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name}
            players.append(row)
    for player_id in request.POST.getlist('MID'):
        cursor = connection.cursor()
        query4 = 'SELECT PLAYER_ID,LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s'
        cursor.execute(query4,[player_id])
        result = cursor.fetchall()
        cursor.close()
        for r in result:
            Id = r[0]
            Name = r[1]
            Position = r[2]
            Team_name = r[3]
            cursor = connection.cursor()
            query5 = "INSERT INTO USER_PLAYERS VALUES(%s,%s,%s)"
            cursor.execute(query5,[id,Id,Position])
            connection.commit()
            cursor.close()
            row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name}
            players.append(row)
    for player_id in request.POST.getlist('FWD'):
        cursor = connection.cursor()
        query6 = 'SELECT PLAYER_ID,LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s'
        cursor.execute(query6,[player_id])
        result = cursor.fetchall()
        cursor.close()
        for r in result:
            Id = r[0]
            Name = r[1]
            Position = r[2]
            Team_name = r[3]
            cursor = connection.cursor()
            query7 = "INSERT INTO USER_PLAYERS VALUES(%s,%s,%s)"
            cursor.execute(query7,[id,Id,Position])
            connection.commit()
            cursor.close()
            row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name}
            players.append(row)
    return render(request,'pick_team.html',{'Players':players})
