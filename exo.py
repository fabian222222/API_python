from flask import Flask, request, jsonify
import csv
import dns.resolver

app = Flask(__name__)
def settings():
    return 'settings'

@app.route("/")
def api_root():
    return ("bonjour")

@app.route("/api/test")
def api_response(): 
    API_response = {"domaine": []}
    with open("202102_OPENDATA_A-NomsDeDomaineEnPointFr.csv", encoding="latin1") as data:
        reader = csv.DictReader(data, delimiter=";")
        for i, row in enumerate(reader):
            API_response["domaine"].append(row["Nom de domaine"])
            if i > 10:
                break
        return API_response

@app.route("/api/domain/<fqdn>")
def gou(fqdn):
    API_response = {"fqdn": [], "info": [], "error": []}
    if request.method == "GET":
        with open("202102_OPENDATA_A-NomsDeDomaineEnPointFr.csv", encoding="latin1") as data:
            reader = csv.DictReader(data, delimiter=";")
            for i, row in enumerate(reader):
                if row["Nom de domaine"] == fqdn:
                    API_response["fqdn"].append(row["Nom de domaine"])
                    API_response["info"].append(row["Pays BE"])
                    API_response["info"].append(row["Departement BE"])
                    API_response["info"].append(row["Ville BE"])
                    API_response["info"].append(row["Nom BE"])
                    API_response["info"].append(row["Sous domaine"])
                    API_response["info"].append(row["Type du titulaire"])
                    API_response["info"].append(row["Pays titulaire"])
                    API_response["info"].append(row["Departement titulaire"])
                    API_response["info"].append(row["Domaine IDN"])
                    API_response["info"].append(row["Date de création"])
                    API_response["info"].append(row["Date de retrait du WHOIS"])
                    API_response['info'].append(row['/api/domain/{fqdn}/dns/'])
                # if i > 10:
                #     API_response["error"].append("Valeur non trouvee")
                #     break
            return API_response

@app.route("/api/domain/<fqdn>/dns")
def gou2(fqdn):
    DSN = [] 
    if request.method == "GET":
        answers = dns.resolver.query(fqdn, 'MX')
        for answer in answers:
            DSN.append({
                "exchange" : str(answer.exchange),
                "preference" : str(answer.preference),
                "ttl" : str(answers.ttl),
                # "values" : str(answers.values),
                "name" : fqdn,
                "type" : "MX"
                })
        answers2 = dns.resolver.query(fqdn, 'A')
        for answer in answers2:
            DSN.append({
                "adress" : str(answer.address),
                "name" : fqdn,
                "ttl" : str(answers2.ttl),
                "type" : "A"
                })
        answers3 = dns.resolver.query(fqdn, 'TXT')
        for answer in answers3:
            DSN.append({
                "adress" : [txt.decode("UTF-8") for txt in answer.strings],
                "ttl" : str(answers3.ttl),
                "name" : fqdn,
                "type" : "TXT"
                })
        answers4 = dns.resolver.query(fqdn, 'NS')
        for answer in answers4:
            DSN.append({
                "adress" : str(answer.target),
                "ttl" : str(answers3.ttl),
                "name" : fqdn,
                "type" : "NS"
                })
    return jsonify(DSN)

@app.route("/api/be/<be>", methods=['GET'])
def gou3(be):
    number_of_domain = 0
    response = {
        "pays" : [],
        "departement" : [],
        "ville" : [],
        "nom" : [],
        "number_of_domain" : []
    }
    with open("202102_OPENDATA_A-NomsDeDomaineEnPointFr.csv", encoding="latin1") as data:
        reader = csv.DictReader(data, delimiter=";")
        for i, row in enumerate(reader):
            if row["Nom BE"] == be:
                response['pays'] = (row['Pays BE']),
                response['departement'] = (row['Departement BE']),
                response['ville'] = (row['Ville BE']),
                response['nom'] = (row['Nom BE']),
                response['number_of_domain'] = number_of_domain,
                number_of_domain += 1
        return jsonify(response)