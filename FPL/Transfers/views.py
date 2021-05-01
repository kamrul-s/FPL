from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages

def transfers(request):
    if 'user' not in request.session:
        return render(request,'index.html')
    id = request.session['user']

    cursor = connection.cursor()
    query = "SELECT USER_TEAM_ID FROM USER_TEAM WHERE USER_ID = %s"
    cursor.execute(query,[id])
    t_id = cursor.fetchone()
    cursor.close()
    team_id = (''.join(map(str,t_id)))

    cursor = connection.cursor()
    args = [0]
    result_args = cursor.callproc('GET_GAME_WEEK',args)
    cursor.close()
    gweek = int(result_args[0])

    cursor = connection.cursor()
    query = "SELECT * FROM TRANSFER WHERE USER_TEAM_ID=%s and GAMEWEEK_ID=%s"
    cursor.execute(query,[team_id,gweek])
    tans = cursor.fetchall()
    cursor.close()
    if(len(tans)>0):
        messages.warning(request,f"Can't make more transfers in this upcoming week")
        cursor = connection.cursor()
        sql = "SELECT PLAYER_ID FROM STARTING_TEAM WHERE USER_TEAM_ID = %s AND GAMEWEEK_ID = %s"
        cursor.execute(sql,[team_id,gweek])
        res = cursor.fetchall()
        cursor.close()
        starting_players = []
        for r in res:
             pl_id = r[0]
             cursor = connection.cursor()
             query3 = 'SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s'
             cursor.execute(query3,[pl_id])
             result = cursor.fetchall()
             cursor.close()
             for qr in result:
                  Name = qr[0]
                  Position = qr[1]
                  Team_name = qr[2]
                  row = {'Id':pl_id,'Name':Name,'Position':Position,'Team_name':Team_name}
                  starting_players.append(row)
        cursor = connection.cursor()
        sql = "SELECT PLAYER_ID FROM BENCHES WHERE USER_TEAM_ID = %s AND GAMEWEEK_ID = %s"
        cursor.execute(sql,[team_id,gweek])
        res = cursor.fetchall()
        cursor.close()
        bench_players = []
        for r in res:
            pl_id = r[0]
            cursor = connection.cursor()
            query3 = 'SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s'
            cursor.execute(query3,[pl_id])
            result = cursor.fetchall()
            cursor.close()
            for qr in result:               
                Name = qr[0]
                Position = qr[1]
                Team_name = qr[2]
                row = {'Id':pl_id,'Name':Name,'Position':Position,'Team_name':Team_name}
                bench_players.append(row)
        cursor = connection.cursor()
        query = "SELECT PLAYER_ID FROM CAPTAINS WHERE USER_TEAM_ID = %s AND GAMEWEEK_ID = %s"
        cursor.execute(query,[team_id,gweek])
        cap = cursor.fetchone()
        cap_id = int((''.join(map(str,cap))))
        cursor.close()
        return render(request,'myteam.html',{'Starting_players':starting_players,'Bench':bench_players,'Captain':cap_id,'Gameweek':gweek})


    cursor = connection.cursor()
    query = "SELECT PLAYER_ID FROM USER_PLAYERS WHERE USER_ID = %s"
    cursor.execute(query,[id])
    result = cursor.fetchall()
    cursor.close()
    players = []
    for r in result:
        pl_id = r[0]
        cursor = connection.cursor()
        query = "SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME,PRICE FROM PLAYER_INFO WHERE PLAYER_ID = %s"
        cursor.execute(query,[pl_id])
        qr = cursor.fetchall()
        cursor.close()
        for s in qr:
            Name = s[0]
            Position = s[1]
            Team_name = s[2]
            Price = s[3]
            row = {'Id':pl_id,'Name':Name,'Position':Position,'Team_name':Team_name,'Price':Price}
            players.append(row)
    cursor = connection.cursor()
    query = 'SELECT PLAYER_ID,LAST_NAME,PLAYING_POSITION,TEAM_NAME,PRICE FROM PLAYER_INFO WHERE PLAYER_ID NOT IN(SELECT PLAYER_ID FROM USER_PLAYERS WHERE USER_ID = %s) ORDER BY PLAYER_ID'
    cursor.execute(query,[id])
    result = cursor.fetchall()
    cursor.close()
    all_players = []
    for r in result:
        Id = r[0]
        Name = r[1]
        Position = r[2]
        Team_name = r[3]
        Price = r[4]
        row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name,'Price':Price}
        all_players.append(row)
    return render(request,'transfer.html',{'Players':players,'All_players':all_players})

def make_transfers(request): 
    if 'user' not in request.session:
        return render(request,'index.html')   
    id = request.session['user']
    cursor = connection.cursor()
    query = "SELECT USER_TEAM_ID FROM USER_TEAM WHERE USER_ID = %s"
    cursor.execute(query,[id])
    t_id = cursor.fetchone()
    cursor.close()
    team_id = (''.join(map(str,t_id)))

    args = [0]
    cursor = connection.cursor()
    result_args = cursor.callproc('GET_GAME_WEEK',args)
    cursor.close()
    gw = int(result_args[0])

    out = []
    inp = []
    out_gkp = request.POST.getlist('out_GKP')
    if len(out_gkp) != 0:   
        for pl in out_gkp:
            out.append(pl)            
    
    out_def = request.POST.getlist('out_DEF')
    if len(out_def) != 0:   
        for pl in out_def:
            out.append(pl)            
    
    out_mid = request.POST.getlist('out_MID')
    if len(out_mid) != 0:   
        for pl in out_mid:
            out.append(pl)
            
    out_fwd = request.POST.getlist('out_FWD')
    if len(out_fwd) != 0:   
        for pl in out_fwd:
            out.append(pl)            
    
    in_gkp = request.POST.getlist('in_GKP')
    if len(in_gkp) != 0:
        for pl in in_gkp:
            inp.append(pl)
            
    in_def = request.POST.getlist('in_DEF')
    if len(in_def) != 0:
        for pl in in_def:
            inp.append(pl)            
    
    in_mid = request.POST.getlist('in_MID')
    if len(in_mid) != 0:
        for pl in in_mid:
            inp.append(pl)            
        
    in_fwd = request.POST.getlist('in_FWD')
    if len(in_fwd) != 0:
        for pl in in_fwd:
            inp.append(pl)            
    
    cost = 0
    cursor = connection.cursor()
    sql = "SELECT PLAYER_ID FROM USER_PLAYERS WHERE USER_ID = %s"
    cursor.execute(sql,[id])
    result = cursor.fetchall()
    cursor.close()
    for r in result:
        pl_id = r[0]
        cursor = connection.cursor()
        query = "SELECT PRICE FROM PLAYER_INFO WHERE PLAYER_ID = %s"
        cursor.execute(query,[pl_id])
        qr = cursor.fetchall()
        cursor.close()
        for s in qr:
            Price = s[0]
            cost=cost+Price              

    for p in out:
        cursor = connection.cursor()
        query = "SELECT PRICE FROM PLAYER_INFO WHERE PLAYER_ID = %s"
        cursor.execute(query,[p])
        qr = cursor.fetchall()
        cursor.close()
        for s in qr:
            outcost = s[0]
            cost=cost-outcost
    for p in inp:
        cursor = connection.cursor()
        query = "SELECT PRICE FROM PLAYER_INFO WHERE PLAYER_ID = %s"
        cursor.execute(query,[p])
        qr = cursor.fetchall()
        cursor.close()
        for s in qr:
            incost = s[0]
            cost=cost+incost           
    
    if cost <= 100:
        for p in out:
            out_id = p
            cursor = connection.cursor()
            sql = "DELETE FROM USER_PLAYERS WHERE USER_ID = %s AND PLAYER_ID = %s"
            cursor.execute(sql,[id,out_id])
            connection.commit()
            cursor.close()
        for p in inp:
            in_id = p
            cursor = connection.cursor()
            query = "SELECT PLAYING_POSITION FROM PLAYER_INFO WHERE PLAYER_ID = %s"
            cursor.execute(query,[in_id])
            pos = cursor.fetchone()
            cursor.close()
            pos = (''.join(map(str,pos)))

            cursor = connection.cursor()
            query = "INSERT INTO USER_PLAYERS VALUES(%s,%s,%s)"
            cursor.execute(query,[id,in_id,pos])
            connection.commit()
            cursor.close()
    
        cursor = connection.cursor()
        query1="INSERT INTO TRANSFER(USER_TEAM_ID,IN_PLAYER_ID,OUT_PLAYER_ID,GAMEWEEK_ID) VALUES(%s,%s,%s,%s)"
        cursor.execute(query1,[team_id,in_id,out_id,gw])
        connection.commit()
        cursor.close()

        cursor = connection.cursor()
        query1="DELETE FROM STARTING_TEAM WHERE USER_TEAM_ID=%s AND GAMEWEEK_ID = %s"
        cursor.execute(query1,[team_id,gw])
        cursor.close()
        
        cursor = connection.cursor()
        query2="DELETE FROM BENCHES WHERE USER_TEAM_ID=%s AND GAMEWEEK_ID = %s"
        cursor.execute(query2,[team_id,gw])
        cursor.close()

        cursor = connection.cursor()
        query3="DELETE FROM CAPTAINS WHERE USER_TEAM_ID=%s AND GAMEWEEK_ID = %s"
        cursor.execute(query3,[team_id,gw])
        cursor.close()

        cursor = connection.cursor()
        query = "SELECT PLAYER_ID FROM USER_PLAYERS WHERE USER_ID = %s"
        cursor.execute(query,[id])
        res = cursor.fetchall()
        cursor.close()
        players = []
        for r in res:
            Id = r[0]        
            cursor = connection.cursor()
            query = "SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s"
            cursor.execute(query,[Id])
            user_playerss = cursor.fetchall()
            cursor.close()
            for s in user_playerss:
                Name = s[0]
                Position = s[1]
                Team_name = s[2]
                row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name}
                players.append(row)
        
        return render(request,'pick_team.html',{'Players':players})
    
    else:
        cursor = connection.cursor()
        query = "SELECT PLAYER_ID FROM USER_PLAYERS WHERE USER_ID = %s"
        cursor.execute(query,[id])
        result = cursor.fetchall()
        cursor.close()
        players = []
        for r in result:
            pl_id = r[0]
            cursor = connection.cursor()
            query = "SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME,PRICE FROM PLAYER_INFO WHERE PLAYER_ID = %s"
            cursor.execute(query,[pl_id])
            qr = cursor.fetchall()
            cursor.close()
            for s in qr:
                Name = s[0]
                Position = s[1]
                Team_name = s[2]
                Price = s[3]
                row = {'Name':Name,'Position':Position,'Team_name':Team_name,'Price':Price}
                players.append(row)
        cursor = connection.cursor()
        query = 'SELECT PLAYER_ID,LAST_NAME,PLAYING_POSITION,TEAM_NAME,PRICE FROM PLAYER_INFO WHERE PLAYER_ID NOT IN(SELECT PLAYER_ID FROM USER_PLAYERS WHERE USER_ID = %s) ORDER BY PLAYER_ID'
        cursor.execute(query,[id])
        result = cursor.fetchall()
        cursor.close()
        all_players = []
        for r in result:
            Id = r[0]
            Name = r[1]
            Position = r[2]
            Team_name = r[3]
            Price = r[4]
            row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name,'Price':Price}
            all_players.append(row)
        return render(request,'transfer.html',{'Players':players,'All_players':all_players})

def viewhistory(request):
    if 'user' not in request.session:
        return render(request,'index.html')
    id = request.session['user']
    cursor = connection.cursor()
    query = "SELECT USER_TEAM_ID FROM USER_TEAM WHERE USER_ID = %s"
    cursor.execute(query,[id])
    t_id = cursor.fetchone()
    cursor.close()
    team_id = (''.join(map(str,t_id)))    

    trans_history = []
    cursor = connection.cursor()
    sql = "SELECT GAMEWEEK_ID,IN_PLAYER_ID,OUT_PLAYER_ID FROM TRANSFER WHERE USER_TEAM_ID = %s"
    cursor.execute(sql,[team_id])
    result = cursor.fetchall()
    cursor.close()
    if result is None:
        messages.warning(request,f"You have not made any transfers yet.")
        cursor = connection.cursor()
        query = "SELECT PLAYER_ID FROM USER_PLAYERS WHERE USER_ID = %s"
        cursor.execute(query,[id])
        result = cursor.fetchall()
        cursor.close()
        players = []
        for r in result:
            pl_id = r[0]
            cursor = connection.cursor()
            query = "SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME,PRICE FROM PLAYER_INFO WHERE PLAYER_ID = %s"
            cursor.execute(query,[pl_id])
            qr = cursor.fetchall()
            cursor.close()
            for s in qr:
                Name = s[0]
                Position = s[1]
                Team_name = s[2]
                Price = s[3]
                row = {'Id':pl_id,'Name':Name,'Position':Position,'Team_name':Team_name,'Price':Price}
                players.append(row)
        cursor = connection.cursor()
        query = 'SELECT PLAYER_ID,LAST_NAME,PLAYING_POSITION,TEAM_NAME,PRICE FROM PLAYER_INFO WHERE PLAYER_ID NOT IN(SELECT PLAYER_ID FROM USER_PLAYERS WHERE USER_ID = %s) ORDER BY PLAYER_ID'
        cursor.execute(query,[id])
        result = cursor.fetchall()
        cursor.close()
        all_players = []
        for r in result:
            Id = r[0]
            Name = r[1]
            Position = r[2]
            Team_name = r[3]
            Price = r[4]
            row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name,'Price':Price}
            all_players.append(row)
        return render(request,'transfer.html',{'Players':players,'All_players':all_players})
    
    for r in result:
        gw = r[0]
        in_id = r[1]
        out_id = r[2]
        row = {'GW':gw,'In':in_id,'Out':out_id}
        trans_history.append(row)
    return render(request,'viewtransfers.html',{'Trans_history':trans_history})
