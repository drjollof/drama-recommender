from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
from rapidfuzz import process , fuzz

app = Flask(__name__)

#load the data and similarity matrix
comb_sim = joblib.load('comb_sim.pkl')
app_movie_df = joblib.load('app_movie_df.pkl')

#create series for indexing
title_reversed = pd.Series(app_movie_df['titles'].index, index = app_movie_df['titles'])

def get_recommendation_bycf_by_index(idx, country_filter='all'):
    rec_sim = list(enumerate(comb_sim[idx]))
    rec_sort = sorted(rec_sim, key=lambda x: x[1], reverse=True)
    top_n = rec_sort[0:30]
    rec_indices = [x[0] for x in top_n]
    sim = [round(x[1] * 100, 2) for x in top_n]

    rec = pd.Series(app_movie_df['titles'].iloc[rec_indices]).reset_index(drop=True).to_frame()
    country = pd.Series(app_movie_df['country'].iloc[rec_indices]).reset_index(drop=True).to_frame()
    year = pd.Series(app_movie_df['year'].iloc[rec_indices]).reset_index(drop=True).to_frame()
    sim_df = pd.Series(sim).reset_index(drop=True).to_frame()

    data = pd.concat([rec, country, year, sim_df], axis=1)
    data.columns = ['titles', 'type', 'year', 'similarity(%)']

    #apply filter if specified
    if country_filter != 'all':
        data = data[data['type'] == country_filter]

    if data.empty:
        return "<p>No recommendations found for your search.</p>"

    return data.to_html(classes='result-table', border=0)

#autocomplete endpoint using rapidfuzz
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').strip().lower()
    if not query:
        return jsonify([])
    
     #return only  7 good matches
    matches = process.extract(query, title_reversed.index, limit=7, scorer=fuzz.WRatio)
    suggestions = [match[0] for match in matches if match[1] > 50]  
    return jsonify(suggestions)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendation = None
    #check if the user already selected a specific match
    if request.method == 'POST':
        #if a specific index was chosen from the selection page
        if 'selected_index' in request.form:
            selected_index = int(request.form.get('selected_index'))
            #get the filter
            country_filter = request.form.get('country', 'all')
            recommendation = get_recommendation_bycf_by_index(selected_index, country_filter)
            return render_template('index2.html', recommendation=recommendation)
        else:
            #if user submitted the initial search form with a title.
            search_title = request.form.get('title')
            country_filter = request.form.get('country', 'all')
            
            #if user title is not in the title index
            if search_title not in title_reversed.index:
                recommendation = "<p>Title not found.</p>"
                return render_template('index2.html', recommendation=recommendation)
            #return title index
            matches = title_reversed[search_title]
            
            #if multiple indices is found, show the select page
            if isinstance(matches, pd.Series) and len(matches) > 1:
                match_indices = list(matches)
                match_info = []
                for idx in match_indices:
                    info = {
                        'index': idx,
                        'title': app_movie_df.iloc[idx]['titles'],
                        'year': app_movie_df.iloc[idx]['year'],
                        'type': app_movie_df.iloc[idx]['country']  
                    }
                    match_info.append(info)
                return render_template('select2.html', match_info=match_info, country=country_filter)
            else:
                #if only one match is found, get its index.
                if isinstance(matches, pd.Series):
                    idx = matches.iloc[0]
                else:
                    idx = matches
                recommendation = get_recommendation_bycf_by_index(idx, country_filter)
    return render_template('index2.html', recommendation=recommendation)

if __name__ == '__main__':
    app.run()
