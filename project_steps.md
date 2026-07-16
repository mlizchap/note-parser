1. Endpopints
    1. create an input of all notes with note names (from Palantir)
    2. parse each row to determine primary site, output dataframe with primary site col, do not include rows without sites
    3. use dataframe to add items to DB
        - schema = MRN: { site: { notes: [{ note_date, note_name, note_text }] } }
    4. create endpoint that outputs mrn | primary_sites
        - compare to other sources
    5. create endpoint that outputs all notes per mrn / site
    6. using the vals from the endpoint - iterate thru the notes (the text) and parse fields
    7. create a new dataframe and update curr endpoint with field vals
    8. add an other sources section and update endpoint with values   
    

2. User Interface application
    - routes:
        - all: displays mrn | site | ...note fields |
            - add ability to query and visualize
        - per patient: site | ...site fields
            - create a timeline of events
