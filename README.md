# SIPPAPIFramework
**Usage**
You can test SIP functional call and Load testing using this Framework.
---

## Functional Call

curl -i -X POST --header "AUTHTOKEN: chandra" -H "Content-Type: application/json" -d '{"TO":"919980950111","REMOTEIP":"192.168.1.41","REMOTEPORT":"5060","SIPPXML":"https://raw.githubusercontent.com/cps274203/sipp_xml/master/sipp_uac_basic.xml"}' http://127.0.0.1:5000/Call/

---

## Load Test

curl -i -X POST --header "AUTHTOKEN: chandra" -H "Content-Type: application/json" -d '{"TO":"919980950111","REMOTEIP":"192.168.1.41","REMOTEPORT":"5060","SIPPXML":"https://raw.githubusercontent.com/cps274203/sipp_xml/master/sipp_uac_basic.xml"}' http://127.0.0.1:5000/Load/

---
## Status of Load test

curl -i -X POST --header "AUTHTOKEN: chandra" -H "Content-Type: application/json" -d '{"TO":"919980950111","REMOTEIP":"192.168.1.41","REMOTEPORT":"5060","SIPPXML":"https://raw.githubusercontent.com/cps274203/sipp_xml/master/sipp_uac_basic.xml"}' http://127.0.0.1:5000/Load/Stop/10125

---

## Stop the load test

curl -i -X POST --header "AUTHTOKEN: chandra" -H "Content-Type: application/json" -d '{"TO":"919980950111","REMOTEIP":"192.168.1.41","REMOTEPORT":"5060","SIPPXML":"https://raw.githubusercontent.com/cps274203/sipp_xml/master/sipp_uac_basic.xml"}' http://127.0.0.1:5000/Load/Stop/10125/

---
