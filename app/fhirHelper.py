from fhirclient import client
import fhirclient.models.fhirsearch as fs
import fhirclient.models.humanname as hn
import fhirclient.models.codeableconcept as cp
import fhirclient.models.coding as c
import fhirclient.models.condition as con
import fhirclient.models.quantity as qn
import fhirclient.models.fhirreference as fr
import fhirclient.models.fhirsearch as fs
import fhirclient.models.fhirabstractresource as fas
import fhirclient.models.patient as p
import fhirclient.models.procedure as pro
import fhirclient.models.bundle as b
import fhirclient.models.observation as obs
import fhirclient.models.medicationadministration as ma
import fhirclient.models.medicationstatement as ms
import fhirclient.models.dosage as d
import fhirclient.models.annotation as a
import fhirclient.models.bundle as bundle
import json
import datetime
import json

class fhirHelper(object):
  def __init__(self,fhir_id):

    self.settings = {
    'app_id': 'my_web_app',
    'api_base': 'https://r4.smarthealthit.org/'
    }
  # 'api_base': 'http://hapi.fhir.org/baser4' }
    
    self.smartClient = client.FHIRClient(settings =self.settings)
    self.fhir_id = fhir_id
    self.patient = p.Patient.read(self.fhir_id, self.smartClient.server)

  def getPatient(self):
    patient = p.Patient.read('fc200fa2-12c9-4276-ba4a-e0601d424e55', self.smartClient.server)
    return self.smartClient.human_name(patient.name[0])
  def getPatientGender(self):
    patient = p.Patient.read(self.fhir_id, self.smartClient.server)
    if patient.gender == 'male':
      return 1
    else:
      return 0
  def getPatientAge(self):
    db = self.patient.birthDate
    db = db.as_json()
    db_split = db.split("-")
    db_yr = db_split[0]
    n = datetime.datetime.now()
    age = n.year - int(db_yr)
  
    return age

  def getPatientMaritalStatus(self):
    status = self.patient.maritalStatus
    return status
  
  def getPatientConditions(self):
    search = con.Condition.where(struct={'subject': self.fhir_id})
    #search = fs.FHIRSearch(pro.Procedure,{'subject': self.fhir_id})
    #print(search.construct())
    #conditions = search.perform_resources(self.smartClient.server)
    response = self.smartClient.server.request_json(search.construct())
    conditions = []
    for entry in response["entry"]:
      #print(entry)
      temp = entry["resource"]["code"]["text"]
      
      duplicate = 0
      for i in range(len(conditions)):
        if temp == conditions[i]:
          duplicate = 1
      if duplicate == 0:
        print(temp)
        conditions.append(temp)
    return conditions
    



