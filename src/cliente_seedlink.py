#
# exemplos ObsPy
# https://docs.obspy.org/tutorial/code_snippets/utc_date_time.html#initialization
#
# http://moho.iag.usp.br/rq/
# https://www.facebook.com/sismoUSP/reviews/
# https://www.seiscomp3.org/doc/applications/seedlink.html
# 
from obspy.clients.earthworm import Client

client = Client("pubavo1.wr.usgs.gov", 16022)
response = client.get_availability('AV', 'ACH', channel='EHE')



