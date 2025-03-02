from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

#load the data and similarity matrix
#cf_sim = joblib.load('cf_sim.pkl')
app_df = joblib.load('app_df.pkl')

mx = np.load('sim_matrix.npz')
matrix = mx['matrix']  # Access the array using the key 'matrix'

#create series for indexing
title_reversed = pd.Series(app_df['title'].index, index = app_df['title'])

def get_recommendation_bycf_by_index(idx, country_filter='all'):
    rec_sim = list(enumerate(matrix[idx]))
    rec_sort = sorted(rec_sim, key=lambda x: x[1], reverse=True)
    top_n = rec_sort[0:30]
    rec_indices = [x[0] for x in top_n]
    sim = [round(x[1] * 100, 2) for x in top_n]

    rec = pd.Series(app_df['title'].iloc[rec_indices]).reset_index(drop=True).to_frame()
    country = pd.Series(app_df['country'].iloc[rec_indices]).reset_index(drop=True).to_frame()
    year = pd.Series(app_df['year'].iloc[rec_indices]).reset_index(drop=True).to_frame()
    sim_df = pd.Series(sim).reset_index(drop=True).to_frame()

    data = pd.concat([rec, country, year, sim_df], axis=1)
    data.columns = ['titles', 'type', 'year', 'similarity(%)']

    #apply filter if specified
    if country_filter != 'all':
        data = data[data['type'] == country_filter]

    if data.empty:
        return "<p>No recommendations found for your search.</p>"

    return data.to_html(classes='result-table', border=0)

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
            return render_template('index.html', recommendation=recommendation)
        else:
            #if user submitted the initial search form with a title.
            search_title = request.form.get('title')
            country_filter = request.form.get('country', 'all')
            
            #get title index
            if search_title not in title_reversed.index:
                recommendation = "<p>Title not found.</p>"
                return render_template('index.html', recommendation=recommendation)
            
            matches = title_reversed[search_title]
            
            # If multiple indices found, show the select page
            if isinstance(matches, pd.Series) and len(matches) > 1:
                match_indices = list(matches)
                match_info = []
                for idx in match_indices:
                    info = {
                        'index': idx,
                        'title': app_df.iloc[idx]['title'],
                        'year': app_df.iloc[idx]['year'],
                        'type': app_df.iloc[idx]['country']  
                    }
                    match_info.append(info)
                return render_template('select.html', match_info=match_info, country=country_filter)
            else:
                # If only one match is found, get its index.
                if isinstance(matches, pd.Series):
                    idx = matches.iloc[0]
                else:
                    idx = matches
                recommendation = get_recommendation_bycf_by_index(idx, country_filter)
    return render_template('index.html', recommendation=recommendation)

if __name__ == '__main__':
    app.run()
