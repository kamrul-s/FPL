from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

def home(request):
    return render(request,'index.html')

def login(request):
    email = request.POST['email']
    password = request.POST['pass']
    cursor = connection.cursor()
    if password != '':
        query = "SELECT USER_ID FROM USER_INFO WHERE EMAIL = %s"
        cursor.execute(query,[email])
        count = cursor.fetchall()
        cursor.close()
        if len(count) != 0:
            id = int(''.join(map(str,count[0])))
        else:
            return render(request,'index.html')
        cursor = connection.cursor()
        query2 = "SELECT PASSWORD FROM USER_INFO WHERE EMAIL = %s"
        cursor.execute(query2,[email])
        count = cursor.fetchall()
        cursor.close()
        user_exist = False
        if(len(count)<1) :
            return render(request,'index.html')
        encodpass=(''.join(map(str,count[0])))
        if check_password(password,encodpass):
            request.session['user'] = id
            user_exist = True
        else:
            messages.warning(request,f"Username or Password is incorrect")

        if user_exist:
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
            cap = cursor.fetchall()
            cap_id = 1
            for r in cap:
                cap_id = r[0]
            return render(request,'myteam.html',{'Starting_players':starting_players,'Bench':bench_players,'Captain':cap_id,'Gameweek':gw})
        else:
            messages.warning(request,f"No such user exists")
            return render(request,'index.html')

def signup(request):
    new_user = False
    count = []
    email = request.POST['email']
    password = request.POST['pass']
    confpass = request.POST['confpass']
    cursor = connection.cursor()
    sql = "SELECT USER_ID FROM USER_INFO WHERE EMAIL = %s"
    cursor.execute(sql,[email])
    count = cursor.fetchall()
    cursor.close()
    if len(count) == 0 or count is None:
        new_user = True
    if new_user== True:
        if(password == confpass):
            password = make_password(password)
            cursor = connection.cursor()
            id = cursor.callfunc('GET_USER_ID',int)
            query2 = "INSERT INTO USER_INFO(USER_ID,EMAIL,PASSWORD) VALUES(%s,%s,%s)"
            cursor.execute(query2,[id,email,password])
            connection.commit()
            cursor.close()
            request.session['user'] = id
            return render(request,'details.html')
        else:
            messages.warning(request,f"Username or Password is incorrect")
            return render(request,'index.html')
    else:
        messages.warning(request, f"Already has an acoount")
        return render(request,'index.html')

def loginasadmin(request):
    return render(request,'adminlogin.html')

def signout(request):
    if 'user' in request.session:
        del request.session['user']
    return render(request,'index.html')

def help(request):
    return render(request,'help.html')
