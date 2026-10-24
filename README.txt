BANK SUPPORT AGENT  -  Author: Arfakshad
=========================================
Gemini se chalne wala AI bank support agent (Arabic + English).
Sign in karke balance, transactions, card block aur complaint jaise kaam kar sakta hai
(demo data ke saath).

SETUP SUMMARY (QUICK)
---------------------
 Kya chahiye   : Python 3.10+, internet, Gemini API key (aistudio.google.com/apikey)
 Packages      : google-genai, flask  (requirements.txt se apne aap install hote hain)
 Key kahan     : GEMINI_API_KEY (environment variable) ya is folder ki .env file
 Chalana       : Windows -> run_bank_agent.bat | Mac/Linux -> bash run_bank_agent.sh
 Address       : http://127.0.0.1:5000  (sirf usi computer par)
 Demo login    : C1001 / 1234   aur   C1002 / 5678
 Model         : gemini-2.5-flash (bank_support_agent.py mein MODEL se badal sakte hain)
 Bhashayein    : Arabic + English (interface), chat usi bhasha mein jo customer chune/likhe
 Agent ke kaam : balance, transactions, transaction status, card block, complaint
 Files         : bank_web_app.py, bank_support_agent.py, bank_tools.py, bank_db.py,
                 bank_ui.html, requirements.txt, run_bank_agent.bat/.sh, README.txt

DUSRE COMPUTER PAR CHALANE KE LIYE
----------------------------------
1. Poora "bank_agent" folder (ya bank_agent.zip) us computer par copy karein.
   Folder mein ye files honi chahiye (sab ek hi folder mein):
     bank_web_app.py   bank_support_agent.py   bank_tools.py   bank_db.py
     bank_ui.html      requirements.txt        run_bank_agent.bat / .sh
2. Python 3.10 ya naya install karein (python.org). Windows par install karte waqt
   "Add Python to PATH" tick karein.
3. Internet chalu hona chahiye (Gemini online call hota hai).
4. Chalayein:
     Windows : run_bank_agent.bat par double-click
     Mac/Linux: terminal mein   bash run_bank_agent.sh
5. Pehli baar Gemini API key paste karein (aistudio.google.com/apikey se milti hai).
   "save" par y dabayenge to key .env file mein rah jayegi aur agli baar nahi poochhega.
6. Browser http://127.0.0.1:5000 par khulega. Black window/terminal band mat karein.

DEMO LOGIN (naqli data, bank_db.py mein)
----------------------------------------
   C1001 / PIN 1234  (Ahmed Khan)       C1002 / PIN 5678  (Fatima Ali)
Try karein: "TXN1003 ka kya hua?", "card 7788 block karo", "mera balance"

MANUAL TAREEKA (agar .bat/.sh kaam na kare)
-------------------------------------------
   pip install -r requirements.txt
   Windows PowerShell:  $env:GEMINI_API_KEY="your-key"
   Mac/Linux:           export GEMINI_API_KEY="your-key"
   python bank_web_app.py

DHYAN RAKHEIN
-------------
* API key kisi ko share na karein. Zip banate ya bhejte waqt .env file hata dein.
* Ye app sirf usi computer par khulta hai (127.0.0.1). Customers ke liye server par
  deploy karna padega.
* Port 5000 busy ho to:  PORT=8080 python bank_web_app.py  (Windows: $env:PORT="8080")
* Demo data restart par reset ho jata hai. Asli bank ke liye bank_db.py ke functions
  ko bank ki API se badalna hoga, aur real PIN/OTP login lagana hoga.
* Gemini free key ki limit kam hoti hai; "quota" ka message aaye to thodi der baad try karein.
