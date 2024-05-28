from flask import Flask, render_template, request, redirect, url_for
from flask import session
import pickle
import random

app = Flask(__name__)
app.secret_key='secret'

sectors = ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail']

sector_bussiness_type=["Sole Proprietorship", "Partnership", "Limited Liability Partnership","Corporation","Cooperative"]
class Player:
    def __init__(self):
        self.name = ""
        self.sector = ""
        self.bussiness_type = ""
        self.money = 1000
        self.reputation = 100
        self.employees_salary=[]
        self.employees_productivity=[]
        self.products_investment=[]
        self.products_profit=[]
    def action(self,action):
        pass

    def money_action(self,profit,investment):
        self.money+=profit-investment
        if(self.money<0):
            self.money=0
            return False
        return True
    def reputation_action(self,productivity):
        self.reputation+=productivity
        if(self.reputation<0):
            self.reputation=0
            return False
        return True

    def employee_action(self):
        profit=0
        investment=0
        for i in range(len(self.employees_salary)):
            profit+=self.employees_productivity[i]
            investment+=self.employees_salary[i]
        
class situation:
    def __init__(self, name, description, options):
        self.name = name
        self.description = description
        self.options = options
        self.cost = 0
        self.profit = 0
        
    def action(self,player,option):
        if(self.name=="Hiring"):
            if(option=="Hire"):
                player.employees_salary.append(100)
                player.employees_productivity.append(10)
                player.money_action(0,100)
                player.reputation_action(10)
            else:
                player.money_action(0,0)
                player.reputation_action(-10)
        elif(self.name=="Productivity"):
            if(option=="Increase"):
                player.employees_productivity[0]+=10
                player.money_action(0,100)
                player.reputation_action(10)
            else:
                player.money_action(0,0)
                player.reputation_action(-10)
        elif(self.name=="Investment"):
            if(option=="Invest"):
                player.products_investment.append(100)
                player.products_profit.append(10)
                player.money_action(10,100)
                player.reputation_action(10)
            else:
                player.money_action(0,0)
                player.reputation_action(-10)
        pass
situations=[]
situations.append(situation("Hiring","You need to hire new employees",["Hire","Don't Hire"]))
situations.append(situation("Productivity","You need to increase the productivity of your employees",["Increase","Don't Increase"]))
situations.append(situation("Investment","You need to invest in your product",["Invest","Don't Invest"]))



@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/start_game', methods=['POST'])
@app.route('/next_step', methods=['POST'])
def start_game():
    player_name=""
    player_sector=""
    player_bussiness_type=""
    state= request.form.get('state')
    if(state=="after_sector"):
        player_sector = request.form.get('selectedSector')
        print(player_sector)
        return render_template('selector.html',name="business type", options=sector_bussiness_type,oncomplete="after_bussiness_type")
    if(state=="after_bussiness_type"):
        player_bussiness_type = request.form.get('selectedSector')
        print(player_bussiness_type)
        new_player=Player()
        new_player.name=player_name
        new_player.sector=player_sector
        new_player.bussiness_type=player_bussiness_type
        save_player(new_player)
        return redirect(url_for('game'))
    

    player_name = request.form.get('player_name')
    print(player_name,"entered the game")
   
    return render_template('selector.html',name="sector", options=sectors,oncomplete="after_sector")
    # N

def save_player(player):
    # Convert the player object to a byte array
    player_bytes = pickle.dumps(player)
    # Save the byte array in the session
    session['player'] = player_bytes

def get_player():
    # Get the byte array from the session
    player_bytes = session.get('player')
    # Convert the byte array back to a player object
    player = pickle.loads(player_bytes)

    return player


@app.route('/game', methods=['POST','GET'])
def game():
    player = get_player()
    # Get the current situation
    current_situation = situations[random.randint(0,len(situations)-1)]

    if request.method == 'POST':
        option = request.form.get('option')
        current_situation.action(player,option)
        save_player(player)
    return render_template('game.html', player=player,situation=current_situation)


if __name__ == '__main__':
    app.run(debug=True)