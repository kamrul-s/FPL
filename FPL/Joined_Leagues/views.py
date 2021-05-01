from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages

def leagues(request):
    if 'user' not in request.session:
        return render(request,'index.html')
    id = request.session['user']
    cursor = connection.cursor()
    query1 = "SELECT USER_TEAM_ID FROM USER_TEAM WHERE USER_ID = %s"
    cursor.execute(query1,[id])
    t_id = cursor.fetchone()
    cursor.close()
    team_id = (''.join(map(str,t_id)))

    cursor = connection.cursor()
    query = "SELECT LEAGUE_ID FROM JOINED_LEAGUE WHERE USER_TEAM_ID = %s"
    cursor.execute(query,[team_id])
    leagues = cursor.fetchall()
    cursor.close()

    joined_league = []
    for l in leagues:
        l_id = l[0]
        cursor = connection.cursor()
        query = "SELECT LEAGUE_NAME FROM LEAGUE_INFO WHERE LEAGUE_ID = %s"
        cursor.execute(query,[l_id])
        league_name = cursor.fetchone()
        league_name = (''.join(map(str,league_name)))

        cursor = connection.cursor()
        query = "SELECT USER_TEAM_ID FROM JOINED_LEAGUE WHERE LEAGUE_ID = %s"
        cursor.execute(query,[l_id])
        l_team = cursor.fetchall()
        cursor.close()
        league_team = []
        for lt in l_team:
            cursor = connection.cursor()
            query = "SELECT TEAM_NAME FROM USER_TEAM WHERE USER_TEAM_ID = %s"
            cursor.execute(query,[lt[0]])
            team_name = cursor.fetchone()
            team_name = (''.join(map(str,team_name)))
            cursor.close()
            cursor = connection.cursor()
            gained_point=cursor.callfunc('TOTAL_POINTS', int, [lt[0]])
            cursor.close()
            row = (team_name,gained_point)
            league_team.append(row)
        league_team.sort(key = lambda x:(-x[1],x[0]))
        league_team_final=[]
        pos = 1
        for finteam, finpoints in league_team:
            row = {'Position':pos,'Team_name':finteam,'Points':finpoints}
            pos=pos+1
            league_team_final.append(row)
        row = {'League_name':league_name,'League_team':league_team_final}
        joined_league.append(row)

    return render(request,'leagues.html',{'Joined_league':joined_league})

def manage_leagues(request):
    if 'user' not in request.session:
        return render(request,'index.html')
    create = request.POST.get("c_league","empty")
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM LEAGUE_INFO"
    cursor.execute(query)
    count = cursor.fetchone()
    cursor.close()            
    str1 = (''.join(map(str,count)))
    league_id = int(str1) + 1
    
    id = request.session['user']
    cursor = connection.cursor()
    query1 = "SELECT USER_TEAM_ID FROM USER_TEAM WHERE USER_ID = %s"
    cursor.execute(query1,[id])
    t_id = cursor.fetchone()
    cursor.close()
    team_id = (''.join(map(str,t_id)))
    if create != 'empty':
        cursor = connection.cursor()
        query2 = "INSERT INTO LEAGUE_INFO(LEAGUE_ID,LEAGUE_NAME,STARTING_GW) VALUES(%s,%s,%s)"
        cursor.execute(query2,[league_id,create,1])
        connection.commit()
        cursor.close()

        cursor = connection.cursor()
        query3 = "INSERT INTO JOINED_LEAGUE VALUES(%s,%s)"
        cursor.execute(query3,[team_id,league_id])
        connection.commit()
        cursor.close()
        
        cursor = connection.cursor()
        query = "SELECT LEAGUE_ID FROM JOINED_LEAGUE WHERE USER_TEAM_ID = %s"
        cursor.execute(query,[team_id])
        leagues = cursor.fetchall()
        cursor.close()

        joined_league = []
        for l in leagues:
            l_id = l[0]
            cursor = connection.cursor()
            query = "SELECT LEAGUE_NAME FROM LEAGUE_INFO WHERE LEAGUE_ID = %s"
            cursor.execute(query,[l_id])
            league_name = cursor.fetchone()
            league_name = (''.join(map(str,league_name)))

            cursor = connection.cursor()
            query = "SELECT USER_TEAM_ID FROM JOINED_LEAGUE WHERE LEAGUE_ID = %s"
            cursor.execute(query,[l_id])
            l_team = cursor.fetchall()
            cursor.close()
            league_team = []
            for lt in l_team:
                cursor = connection.cursor()
                query = "SELECT TEAM_NAME FROM USER_TEAM WHERE USER_TEAM_ID = %s"
                cursor.execute(query,[lt[0]])
                team_name = cursor.fetchone()
                team_name = (''.join(map(str,team_name)))
                row = {'Team_name':team_name}
                league_team.append(row)
            row = {'League_name':league_name,'League_team':league_team}
            joined_league.append(row)

        return render(request,'leagues.html',{'Joined_league':joined_league})
    else:
        join = request.POST.get("j_league","empty")
        if join != 'empty':
            cursor = connection.cursor()
            query = "SELECT LEAGUE_ID FROM LEAGUE_INFO WHERE LEAGUE_NAME = %s"
            cursor.execute(query,[join])
            jl = cursor.fetchone()
            cursor.close()
            if jl == None:
                messages.warning(request,f"No such league exists")
                return render(request,'leagues.html')        
            jl = (''.join(map(str,jl)))
            l_id = int(jl)
                    
            cursor = connection.cursor()
            query1 = "INSERT INTO JOINED_LEAGUE VALUES(%s,%s)"
            cursor.execute(query1,[team_id,l_id])
            connection.commit()
            cursor.close()
            cursor = connection.cursor()
            query = "SELECT LEAGUE_ID FROM JOINED_LEAGUE WHERE USER_TEAM_ID = %s"
            cursor.execute(query,[team_id])
            leagues = cursor.fetchall()
            cursor.close()

            joined_league = []
            for l in leagues:
                l_id = l[0]
                cursor = connection.cursor()
                query = "SELECT LEAGUE_NAME FROM LEAGUE_INFO WHERE LEAGUE_ID = %s"
                cursor.execute(query,[l_id])
                league_name = cursor.fetchone()
                league_name = (''.join(map(str,league_name)))

                cursor = connection.cursor()
                query = "SELECT USER_TEAM_ID FROM JOINED_LEAGUE WHERE LEAGUE_ID = %s"
                cursor.execute(query,[l_id])
                l_team = cursor.fetchall()
                cursor.close()
                league_team = []
                for lt in l_team:
                    cursor = connection.cursor()
                    query = "SELECT TEAM_NAME FROM USER_TEAM WHERE USER_TEAM_ID = %s"
                    cursor.execute(query,[lt[0]])
                    team_name = cursor.fetchone()
                    team_name = (''.join(map(str,team_name)))
                    row = {'Team_name':team_name}
                    league_team.append(row)
                row = {'League_name':league_name,'League_team':league_team}
                joined_league.append(row)

            return render(request,'leagues.html',{'Joined_league':joined_league})

