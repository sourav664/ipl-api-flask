from flask import Flask,jsonify,render_template
import ipl

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ipl/teams')
def teams():
    teams = ipl.teams_name()
    return jsonify(teams)


@app.route('/ipl/team/<team1>/<team2>')
def teamVsteam(team1,team2):
    headtohead = ipl.team1Vsteam2(team1,team2)
    return headtohead

@app.route('/ipl/<team>')
def team_records(team):
    t = team.title()
    record = ipl.team_record(t)
    return record

@app.route('/ipl/batsman/<batsman>')
def batsman_record(batsman):
    record = ipl.batsman_record(batsman)
    return record


@app.route('/ipl/bowler/<bowler>')
def bowler_record(bowler):
    record = ipl.bowler_records(bowler)
    return record


app.run(debug=True)

