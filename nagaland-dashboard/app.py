
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, District, RegistrationStat

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nagaland.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# ── GET all districts ──────────────────────────────────────
@app.route('/api/districts', methods=['GET'])
def get_districts():
    districts = District.query.all()
    return jsonify([
        {'id': d.id, 'name': d.name}
        for d in districts
    ])


# ── GET all stats (optional filter by area_type or district) ──
@app.route('/api/stats', methods=['GET'])
def get_stats():
    area_type   = request.args.get('area_type')   # ?area_type=Rural
    district_id = request.args.get('district_id') # ?district_id=1
    year        = request.args.get('year')         # ?year=2023

    query = RegistrationStat.query

    if area_type:
        query = query.filter_by(area_type=area_type)
    if district_id:
        query = query.filter_by(district_id=int(district_id))
    if year:
        query = query.filter_by(year=int(year))

    stats = query.all()

    return jsonify([
        {
            'id'                      : s.id,
            'district'                : s.district.name,
            'area_type'               : s.area_type,
            'year'                    : s.year,
            'census_population'       : s.census_population,
            'reg_units'               : s.reg_units,
            'returns_due'             : s.returns_due,
            'returns_received'        : s.returns_received,
            'est_midyear_pop_total'   : s.est_midyear_pop_total,
            'est_midyear_pop_adjusted': s.est_midyear_pop_adjusted,
        }
        for s in stats
    ])


# ── GET one district's full stats ─────────────────────────
@app.route('/api/districts/<int:district_id>/stats', methods=['GET'])
def get_district_stats(district_id):
    district = District.query.get_or_404(district_id)
    stats    = RegistrationStat.query.filter_by(district_id=district_id).all()

    return jsonify({
        'district': district.name,
        'stats': [
            {
                'area_type'               : s.area_type,
                'year'                    : s.year,
                'census_population'       : s.census_population,
                'reg_units'               : s.reg_units,
                'returns_due'             : s.returns_due,
                'returns_received'        : s.returns_received,
                'est_midyear_pop_total'   : s.est_midyear_pop_total,
                'est_midyear_pop_adjusted': s.est_midyear_pop_adjusted,
            }
            for s in stats
        ]
    })


if __name__ == '__main__':
    app.run(debug=True)