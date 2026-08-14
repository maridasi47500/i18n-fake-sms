
mkdir templates 
python3 scaffold.py language name shortname
python3 scaffold.py user username phone country_id:references email
python3 scaffold.py place name lat lon
python3 scaffold.py postcard place_id:references pic:file recipient message user_id:references language_id:references
python3 scaffold.py letter recipient language_id:references user_id:references message
python3 scaffold.py email recipient user_id:references subject body language_id:references
python3 scaffold.py sms recipient language_id:references user_id:references message
python3 scaffold.py calendar_entry date user_id:reference title description time language_id:references place_id:references
