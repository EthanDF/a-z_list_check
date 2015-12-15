# a-z_list_check
checks against the serialssolutions a-z list to make sure the url is available

takes a csv file with the following values:
- aleph bib
- title
- vendor
- issn

checks against the FAU SerialsSolutions A-Z list to make sure the URL is available with the ISSN provided using the base URL by making sure the vendor's name appears on the page:
http://hx8vv5bf7j.search.serialssolutions.com/?V=1.0&N=100&L=HX8VV5BF7J&S=I_M&C=

returns a tab-delimited log with:
- aleph bib (provided)
- journal title (provided)
- issn (provided)
- URL (baseURL+issn)
- result (True/False)
