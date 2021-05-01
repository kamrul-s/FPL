from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse

def pick_team(request):
     gkp = []
     defenders = []
     mid = []
     fwd = []
     if 'user' not in request.session:
          return render(request,'index.html')
     
     args = [0]
     cursor = connection.cursor()
     result_args = cursor.callproc('GET_GAME_WEEK',args)
     cursor.close()
     gw = int(result_args[0])

     id = request.session['user']
     cursor = connection.cursor()
     query = "SELECT USER_TEAM_ID FROM USER_TEAM WHERE USER_ID = %s"
     cursor.execute(query,[id])
     t_id = cursor.fetchone()
     cursor.close()
     team_id = (''.join(map(str,t_id)))
     gkp = request.POST.getlist('starting_GKP')
     defenders = request.POST.getlist('starting_DEF')
     mid = request.POST.getlist('starting_MID')
     fwd = request.POST.getlist('starting_MID')
     if len(gkp)+len(defenders)+len(mid)+len(fwd) < 11:
          cursor = connection.cursor()
          sql = "SELECT PLAYER_ID FROM USER_PLAYERS WHERE USER_ID = %s"
          cursor.execute(sql,[id])
          res = cursor.fetchall()
          cursor.close()
          players = []
          for r in res:
               Id = r[0]
               cursor = connection.cursor()
               query2 = 'SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s'
               cursor.execute(query2,[Id])
               result = cursor.fetchall()
               cursor.close()
               for rs in result:                    
                    Name = rs[0]
                    Position = rs[1]
                    Team_name = rs[2]
                    row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name}
                    players.append(row)
          return render(request,'pick_team.html',{'Players':players})
     starting_players = []
     #starting gk
     for sp in request.POST.getlist('starting_GKP'):
          cursor = connection.cursor()
          query1 = 'SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s'
          cursor.execute(query1,[sp])
          result = cursor.fetchall()
          cursor.close()         
          for r in result:               
               Name = r[0]
               Position = r[1]
               Team_name = r[2]
               row = {'Name':Name,'Position':Position,'Team_name':Team_name}
               starting_players.append(row)
               
               cursor = connection.cursor()
               sql = "SELECT GAMEWEEK_ID,FIXTURE_NO FROM FIXTURE_INFO WHERE (HOME_TEAM = %s OR AWAY_TEAM = %s) AND GAMEWEEK_ID = %s"
               cursor.execute(sql,[Team_name,Team_name,gw])
               sql_res = cursor.fetchall()
               cursor.close()
               for sr in sql_res:
                    gw_id = sr[0]
                    fix_no = sr[1]
                    cursor = connection.cursor()     
                    query2 = "INSERT INTO STARTING_TEAM VALUES(%s,%s,%s,%s)"
                    cursor.execute(query2,[team_id,sp,gw_id,fix_no])
                    connection.commit()
                    cursor.close()
     #starting def                    
     for sp in request.POST.getlist('starting_DEF'):
          cursor = connection.cursor()
          query3 = 'SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s'
          cursor.execute(query3,[sp])
          result = cursor.fetchall()
          cursor.close()
          for r in result:               
               Name = r[0]
               Position = r[1]
               Team_name = r[2]
               row = {'Name':Name,'Position':Position,'Team_name':Team_name}
               starting_players.append(row)

               cursor = connection.cursor()
               sql = "SELECT GAMEWEEK_ID,FIXTURE_NO FROM FIXTURE_INFO WHERE (HOME_TEAM = %s OR AWAY_TEAM = %s) AND GAMEWEEK_ID = %s"
               cursor.execute(sql,[Team_name,Team_name,gw])
               sql_res = cursor.fetchall()
               cursor.close()
               for sr in sql_res:
                    gw_id = sr[0]
                    fix_no = sr[1]
                    cursor = connection.cursor()     
                    query1 = "INSERT INTO STARTING_TEAM VALUES(%s,%s,%s,%s)"
                    cursor.execute(query1,[team_id,sp,gw_id,fix_no])
                    connection.commit()
                    cursor.close()
     #starting mid
     for sp in request.POST.getlist('starting_MID'):
          cursor = connection.cursor()
          query5 = 'SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s'
          cursor.execute(query5,[sp])
          result = cursor.fetchall()
          cursor.close()
          for r in result:               
               Name = r[0]
               Position = r[1]
               Team_name = r[2]
               row = {'Name':Name,'Position':Position,'Team_name':Team_name}
               starting_players.append(row)

               cursor = connection.cursor()
               sql = "SELECT GAMEWEEK_ID,FIXTURE_NO FROM FIXTURE_INFO WHERE (HOME_TEAM = %s OR AWAY_TEAM = %s) AND GAMEWEEK_ID = %s"
               cursor.execute(sql,[Team_name,Team_name,gw])
               sql_res = cursor.fetchall()
               cursor.close()
               for sr in sql_res:
                    gw_id = sr[0]
                    fix_no = sr[1]
                    cursor = connection.cursor()     
                    query1 = "INSERT INTO STARTING_TEAM VALUES(%s,%s,%s,%s)"
                    cursor.execute(query1,[team_id,sp,gw_id,fix_no])
                    connection.commit()
                    cursor.close()
     #starting fwd
     for sp in request.POST.getlist('starting_FWD'):
          cursor = connection.cursor()
          query7 = 'SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s'
          cursor.execute(query7,[sp])
          result = cursor.fetchall()
          cursor.close()
          for r in result:               
               Name = r[0]
               Position = r[1]
               Team_name = r[2]
               row = {'Name':Name,'Position':Position,'Team_name':Team_name}
               starting_players.append(row)

               cursor = connection.cursor()
               sql = "SELECT GAMEWEEK_ID,FIXTURE_NO FROM FIXTURE_INFO WHERE (HOME_TEAM = %s OR AWAY_TEAM = %s) AND GAMEWEEK_ID = %s"
               cursor.execute(sql,[Team_name,Team_name,gw])
               sql_res = cursor.fetchall()
               cursor.close()
               for sr in sql_res:
                    gw_id = sr[0]
                    fix_no = sr[1]
                    cursor = connection.cursor()     
                    query1 = "INSERT INTO STARTING_TEAM VALUES(%s,%s,%s,%s)"
                    cursor.execute(query1,[team_id,sp,gw_id,fix_no])
                    connection.commit()
                    cursor.close()

     #bench_players
     cursor = connection.cursor()
     sql = "SELECT PLAYER_ID FROM USER_PLAYERS WHERE USER_ID = %s AND PLAYER_ID NOT IN(SELECT PLAYER_ID FROM STARTING_TEAM WHERE USER_TEAM_ID = %s AND GAMEWEEK_ID = %s)"
     cursor.execute(sql,[id,team_id,gw])
     bench = cursor.fetchall()
     cursor.close()
     bench_players = []
     for bp in bench:
          pl_id = bp[0]
          cursor = connection.cursor()
          query1 = 'SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s'
          cursor.execute(query1,[pl_id])
          result = cursor.fetchall()
          cursor.close()
          for r in result:               
               Name = r[0]
               Position = r[1]
               Team_name = r[2]
               row = {'Name':Name,'Position':Position,'Team_name':Team_name}
               bench_players.append(row)

               cursor = connection.cursor()
               sql = "SELECT GAMEWEEK_ID,FIXTURE_NO FROM FIXTURE_INFO WHERE (HOME_TEAM = %s OR AWAY_TEAM = %s) AND GAMEWEEK_ID = %s"
               cursor.execute(sql,[Team_name,Team_name,gw])
               sql_res = cursor.fetchall()
               cursor.close()
               for sr in sql_res:
                    gw_id = sr[0]
                    fix_no = sr[1]
                    cursor = connection.cursor()     
                    query1 = "INSERT INTO BENCHES VALUES(%s,%s,%s,%s)"
                    cursor.execute(query1,[team_id,pl_id,gw_id,fix_no])
                    connection.commit()
                    cursor.close()
          
     request.session['gameweek'] = gw
     return render(request,'home.html',{'Starting_players':starting_players,'Bench':bench_players})

def captain(request):
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

     cap = request.POST['captain']
     cursor = connection.cursor()
     query2 = "SELECT PLAYER_ID,TEAM_NAME FROM PLAYER_INFO WHERE LAST_NAME = %s"
     cursor.execute(query2,[cap])
     res = cursor.fetchall()
     cursor.close()
     for r in res:
          pl_id = r[0]
          team_name = r[1]
          cursor = connection.cursor()
          sql = "SELECT GAMEWEEK_ID,FIXTURE_NO FROM FIXTURE_INFO WHERE (HOME_TEAM = %s OR AWAY_TEAM = %s) AND GAMEWEEK_ID = %s"
          cursor.execute(sql,[team_name,team_name,gw])
          sql_res = cursor.fetchall()
          cursor.close()
          for sr in sql_res:
               gw_id = sr[0]
               fix_no = sr[1]
               cursor = connection.cursor()     
               query1 = "INSERT INTO CAPTAINS VALUES(%s,%s,%s,%s)"
               cursor.execute(query1,[team_id,pl_id,gw_id,fix_no])
               connection.commit()
               cursor.close()
     #starting team players
     cursor = connection.cursor()
     sql = "SELECT PLAYER_ID FROM STARTING_TEAM WHERE USER_TEAM_ID = %s AND GAMEWEEK_ID = %s"
     cursor.execute(sql,[team_id,gw])
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
     
     #bench players
     cursor = connection.cursor()
     sql = "SELECT PLAYER_ID FROM BENCHES WHERE USER_TEAM_ID = %s AND GAMEWEEK_ID = %s"
     cursor.execute(sql,[team_id,gw])
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
     cursor.execute(query,[team_id,gw])
     cap = cursor.fetchone()
     cap_id = int((''.join(map(str,cap))))


     return render(request,'myteam.html',{'Starting_players':starting_players,'Bench':bench_players,'Captain':cap_id,'Gameweek':gw})

def pick_team2(request):
     if 'user' not in request.session:
          return render(request,'index.html')
     args = [0]
     cursor = connection.cursor()
     result_args = cursor.callproc('GET_GAME_WEEK',args)
     cursor.close()
     gw = int(result_args[0])
     
     id = request.session['user']
     cursor = connection.cursor()
     query = "SELECT USER_TEAM_ID FROM USER_TEAM WHERE USER_ID = %s"
     cursor.execute(query,[id])
     t_id = cursor.fetchone()
     cursor.close()
     team_id = (''.join(map(str,t_id)))

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
     query4 = "SELECT PLAYER_ID FROM USER_PLAYERS WHERE USER_ID = %s"
     cursor.execute(query4,[id])
     res = cursor.fetchall()
     cursor.close()
     players=[]
     for r in res:
          Id = r[0]
          cursor = connection.cursor()
          query5 = "SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME FROM PLAYER_INFO WHERE PLAYER_ID = %s"
          cursor.execute(query5,[Id])
          info = cursor.fetchall()
          cursor.close()
          for sr in info:
               Name = sr[0]
               Position = sr[1]
               Team_name = sr[2]
               row = {'Id':Id,'Name':Name,'Position':Position,'Team_name':Team_name}
               players.append(row)
     return render(request,'pick_team.html',{'Players':players})

def home(request):     
     return render(request,'home.html')

def myteam(request):
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

     cursor = connection.cursor()
     sql = "SELECT PLAYER_ID FROM STARTING_TEAM WHERE USER_TEAM_ID = %s AND GAMEWEEK_ID = %s"
     cursor.execute(sql,[team_id,gw])
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
     
     #bench players
     cursor = connection.cursor()
     sql = "SELECT PLAYER_ID FROM BENCHES WHERE USER_TEAM_ID = %s AND GAMEWEEK_ID = %s"
     cursor.execute(sql,[team_id,gw])
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
     cursor.execute(query,[team_id,gw])
     cap = cursor.fetchone()
     cap_id = int((''.join(map(str,cap))))

     return render(request,'myteam.html',{'Starting_players':starting_players,'Bench':bench_players,'Captain':cap_id,'Gameweek':gw})

def points(request):     
     return render(request,'points.html')

def showpoints(request):
     if 'user' not in request.session:
         return render(request,'index.html')
     id = request.session['user']
     cursor = connection.cursor()
     query = "SELECT USER_TEAM_ID FROM USER_TEAM WHERE USER_ID = %s"
     cursor.execute(query,[id])
     t_id = cursor.fetchone()
     cursor.close()
     team_id = (''.join(map(str,t_id)))
     gw = request.POST['gameweek']

     cursor = connection.cursor()
     query = "SELECT PLAYER_ID FROM CAPTAINS WHERE USER_TEAM_ID = %s AND GAMEWEEK_ID = %s"
     cursor.execute(query,[team_id,gw])
     cap = cursor.fetchone()
     cap_id = int((''.join(map(str,cap))))

     cursor = connection.cursor()
     sql = "SELECT PLAYER_ID FROM STARTING_TEAM WHERE USER_TEAM_ID = %s AND GAMEWEEK_ID = %s"
     cursor.execute(sql,[team_id,gw])
     res = cursor.fetchall()
     cursor.close()
     starting_players = []
     for r in res:
          pl_id = r[0]
          cursor = connection.cursor()
          query = 'SELECT LAST_NAME,PLAYING_POSITION,TEAM_NAME,PLAYER_POINTS(%s,%s) FROM PLAYER_INFO WHERE PLAYER_ID = %s'
          cursor.execute(query,[pl_id,gw,pl_id])
          result = cursor.fetchall()
          cursor.close()
          for qr in result:               
               Name = qr[0]
               Position = qr[1]
               Team_name = qr[2]
               Points = qr[3]
               if pl_id == cap_id:
                    p = int(Points)
                    Points = str(p*2)
               row = {'Id':pl_id,'Name':Name,'Position':Position,'Team_name':Team_name,'Points':Points}
               starting_players.append(row)
     return render(request,'showPoints.html',{'Starting_players':starting_players,'Gameweek':gw,'Captain':cap_id})